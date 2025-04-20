from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import torch
from PIL import Image
import io
from fastapi.responses import JSONResponse
from transformers import ViTForImageClassification, ViTImageProcessor
from datetime import datetime, timedelta
import mysql.connector
import mysql.connector.pooling
import os
import time
import hashlib
import uuid
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyCVLhXdYF9AGA9YDP2EBqGrN1IT9WHs1CE"
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "models/gemini-1.5-pro"



db_config = {
    "host": "localhost",
    "user":  "root",
    "password": "root",
    "database": "health",
}

pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    **db_config
)

def get_db_connection():
    """Get a connection from the pool."""
    return pool.get_connection()


def write_data(data: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "INSERT INTO injuries_dataset (info) VALUES (%s)",
            (data,)
        )
        conn.commit()
        inserted_id = cursor.lastrowid  # Get the auto-generated id
        return {"message": "Data inserted", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


def get_data(id: int):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM injuries_dataset WHERE id = %s",
            (id,)
        )
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    finally:
        cursor.close()
        conn.close()


app = FastAPI(title="Health Support App API")
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224", num_labels=8)
model.load_state_dict(torch.load("vit_model.pth", map_location=device))
model.to(device)
model.eval()
@app.post("/injury-assessment/")
async def injury_assessment(file: UploadFile = File(...)):
    try:
        # Read image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Preprocess image
        inputs = processor(images=image, return_tensors="pt").to(device)

        # Get predictions
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class = torch.argmax(logits, dim=1).item()

        return JSONResponse(content={
            "filename": file.filename,
            "predicted_class": predicted_class,
            "logits": logits.tolist()
        })

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

class InjuryRequest(BaseModel):
    conversation_history: List[str]
    user_input: str = None  # optional, only needed for response steps
    step: str
model = genai.GenerativeModel(MODEL_NAME)
@app.post("/injury-assessment/")
async def injury_assessment(data: InjuryRequest):
    conversation = data.conversation_history
    step = data.step
    user_input = data.user_input

    try:
        if user_input:
            conversation.append(f"A: {user_input}\n")

        if step == "initial":
            q_prompt = (
                "You're a helpful injury assessment assistant.\n"
                "The user has a bruise or injury and you're trying to evaluate if it could be a fracture.\n"
                f"So far, this is the conversation:\n{''.join(conversation)}\n\n"
                "What is the next **different** question you would ask the user to help assess the injury?\n"
                "Ask just one question. Avoid repeating any previous questions."
            )
            q_response = await model.generate_content_async(q_prompt)
            question = q_response.text.strip()
            conversation.append(f"Q: {question}\n")
            return {"response": question, "conversation_history": conversation}

        elif step == "first_assessment":
            q_prompt = (
                "You're a helpful injury assessment assistant.\n"
                f"Based on this conversation:\n{''.join(conversation)}\n\n"
                "Do you think the user might be dealing with a fracture? Give a short, clear reasoning."
            )
            q_response = await model.generate_content_async(q_prompt)
            result = q_response.text.strip()
            return {"response": result, "conversation_history": conversation}

        elif step == "physical_test":
            q_prompt = (
                "You're a helpful injury assessment assistant.\n"
                "The user has a bruise or injury and you're trying to evaluate if it could be a fracture.\n"
                f"So far, this is the conversation:\n{''.join(conversation)}\n\n"
                "What is the physical test you would ask the user to do to confirm if there is a fracture?\n"
                "Ask just one question. Ask the user to evaluate the pain."
            )
            q_response = await model.generate_content_async(q_prompt)
            question = q_response.text.strip()
            conversation.append(f"Q: {question}\n")
            return {"response": question, "conversation_history": conversation}

        elif step == "final_assessment":
            q_prompt = (
                "You're a helpful injury assessment assistant.\n"
                f"Based on this updated conversation:\n{''.join(conversation)}\n\n"
                "Do you think the user might be dealing with a fracture? Give a short, clear reasoning."
            )
            q_response = await model.generate_content_async(q_prompt)
            result = q_response.text.strip()
            return {"response": result, "conversation_history": conversation}

        elif step == "recommendation":
            final_prompt = (
                "You are a medical assistant analyzing the following injury case:\n"
                f"{''.join(conversation)}\n\n"
                "Please provide recommendations and home remedies if you think this injury is not dangerous. \n"
                "Otherwise, recommend seeing a doctor..keep the answer short no more than 3 lignes"
            )
            q_response = await model.generate_content_async(final_prompt)
            final = q_response.text.strip()
            write_data(final)
            return {"response": final, "conversation_history": conversation}

        return {"response": "Step not recognized", "conversation_history": conversation}

    except Exception as e:
        return {"response": f"Error: {e}", "conversation_history": conversation}








if __name__ == "__main__":
    import uvicorn
    #print(GEMINI_API_KEY)
    uvicorn.run(app, host="0.0.0.0", port=8001)
