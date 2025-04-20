HealNet: AI-based Medical Assistance for War Victims
HealNet is an AI-powered application designed to assist in diagnosing and providing recommendations based on medical data, specifically targeting common injuries, infections, and blood pressure-related conditions for war victims. This application leverages machine learning and image recognition models to evaluate injuries or health issues and provide a structured diagnosis pipeline.

Features
Injury Assessment:

Detects injuries from images, such as fractures and dislocations.

Collects data from users to assess the injury severity.

Provides detailed recommendations or directs the user to seek professional medical help if necessary.

Infection Detection:

Identifies symptoms of infections from user-provided images.

Offers a structured questioning pipeline to assess the level of infection and severity.

Suggests home remedies or recommends a doctor based on severity.

Blood Pressure and Stroke Risk Detection:

Analyzes user-provided images to detect signs related to blood pressure and stroke risk.

Guides users through a diagnostic process to determine their health status.

AI-Powered Conversational Assistant:

Provides a step-by-step conversational flow for gathering data from users about their health condition.

Based on the information provided, the assistant will evaluate and generate recommendations.

How It Works
Step-by-Step Injury Assessment:
Image Upload: The user uploads an image of their injury, which is then analyzed for signs of fractures, dislocations, or other injuries.

Conversation Flow: The assistant asks a series of structured questions to gather more data (e.g., pain levels, movement limitations).

Diagnosis: Based on the responses and image analysis, the assistant determines whether the user may have a fracture or other injury and provides recommendations.

Final Recommendations: If the injury is not deemed severe, the assistant provides home remedies. If it's severe, the assistant recommends seeking a doctor.

Infection Assessment:
Image Upload: The user uploads an image showing signs of infection, such as wounds, skin conditions, or swelling.

Conversation Flow: The assistant follows a set of questions to determine the severity of the infection.

Diagnosis: Based on the analysis of the image and the user's responses, the assistant evaluates the infection risk.

Final Recommendations: Depending on the severity, the assistant either suggests home remedies or advises seeing a doctor.

Blood Pressure & Stroke Risk:
Image Upload: The user uploads a related image or data indicating possible blood pressure issues or stroke risks.

Diagnostic Questions: The assistant asks questions related to the user's medical history and symptoms.

Diagnosis: Based on the uploaded data and responses, the assistant evaluates the likelihood of stroke or high blood pressure.

Recommendations: If the risk is minimal, home remedies or lifestyle changes are suggested. If the risk is high, the assistant advises seeking professional medical attention.

AI Models
Injury Diagnosis Model:
Uses advanced deep learning models, including Vision Transformers (ViT), to analyze images for signs of fractures, dislocations, or other injuries.

The model has been trained to identify key features such as bone fractures and displacement.

Infection Diagnosis Model:
A deep learning-based image recognition model that analyzes uploaded images for signs of infection.

The assistant uses a structured pipeline to ask the user targeted questions based on the detected symptoms.

Blood Pressure & Stroke Risk Model:
A classification model that predicts the likelihood of stroke or high blood pressure based on user data and images.

Installation and Setup
Clone the Repository:

bash
Copier
Modifier
git clone https://github.com/NoorMajdoub/HealNet.git
cd HealNet
Install Dependencies: Make sure to install the necessary libraries using pip:

bash
Copier
Modifier
pip install -r requirements.txt
Set Up Environment Variables: Create a .env file to store sensitive keys like API tokens for external services. Example:

env
Copier
Modifier
GEMINI_API_KEY=your_api_key
Run the Application: Use Uvicorn to run the FastAPI application:

bash
Copier
Modifier
uvicorn main:app --reload
Access the API: The API will be accessible at http://127.0.0.1:8000.

API Endpoints
POST /injury-assessment/
This endpoint allows users to submit data related to their injury for assessment.

Request Body:

json
Copier
Modifier
{
  "conversation_history": ["previous conversation"],
  "user_input": "user response",
  "step": "initial"
}
conversation_history: A list of prior conversations.

user_input: The user's response to a question (if applicable).

step: The current step of the assessment (initial, first_assessment, physical_test, final_assessment, recommendation).

Response: Returns the next step in the diagnostic process or a recommendation.

Contributing
Feel free to fork the project and submit pull requests for any changes or improvements. Contributions are always welcome!
