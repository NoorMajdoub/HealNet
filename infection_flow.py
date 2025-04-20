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
@app.post("/infection-assessment/")
async def infection_assessment(data: InjuryRequest):
    conversation = data.conversation_history
    step = data.step
    user_input = data.user_input

    try:
        if user_input:
            conversation.append(f"A: {user_input}\n")

        if step == "initial":
            q_prompt = (
                "You're a helpful infection assessment assistant.\n"
                "The user is experiencing symptoms of a possible infection, and you're trying to evaluate its severity.\n"
                f"So far, this is the conversation:\n{''.join(conversation)}\n\n"
                "What is the next **different** question you would ask the user to help assess the infection?\n"
                "Ask just one question. Avoid repeating any previous questions."
            )
            q_response = await model.generate_content_async(q_prompt)
            question = q_response.text.strip()
            conversation.append(f"Q: {question}\n")
            return {"response": question, "conversation_history": conversation}

        elif step == "first_assessment":
            q_prompt = (
                "You're a helpful infection assessment assistant.\n"
                f"Based on this conversation:\n{''.join(conversation)}\n\n"
                "Do you think the user might be dealing with a serious infection? Give a short, clear reasoning."
            )
            q_response = await model.generate_content_async(q_prompt)
            result = q_response.text.strip()
            return {"response": result, "conversation_history": conversation}

        elif step == "physical_test":
            q_prompt = (
                "You're a helpful infection assessment assistant.\n"
                f"So far, this is the conversation:\n{''.join(conversation)}\n\n"
                "What is a simple physical check or observation the user can perform to help determine the infection's severity?\n"
                "Ask just one question and focus on something observable like swelling, redness, or fever."
            )
            q_response = await model.generate_content_async(q_prompt)
            question = q_response.text.strip()
            conversation.append(f"Q: {question}\n")
            return {"response": question, "conversation_history": conversation}

        elif step == "final_assessment":
            q_prompt = (
                "You're a helpful infection assessment assistant.\n"
                f"Based on this updated conversation:\n{''.join(conversation)}\n\n"
                "Do you think the user might be dealing with a dangerous infection? Give a short, clear reasoning."
            )
            q_response = await model.generate_content_async(q_prompt)
            result = q_response.text.strip()
            return {"response": result, "conversation_history": conversation}

        elif step == "recommendation":
            final_prompt = (
                "You are a medical assistant analyzing the following infection case:\n"
                f"{''.join(conversation)}\n\n"
                "Please provide recommendations and home remedies if you think this infection is not dangerous.\n"
                "Otherwise, recommend seeing a doctor. Keep the answer short, no more than 3 lines."
            )
            q_response = await model.generate_content_async(final_prompt)
            final = q_response.text.strip()
            write_data(final)
            return {"response": final, "conversation_history": conversation}

        return {"response": "Step not recognized", "conversation_history": conversation}

    except Exception as e:
        return {"response": f"Error: {e}", "conversation_history": conversation}

