

# HealNet: AI-based Medical Assistance for War Victims

HealNet is an AI-powered application designed to assist in diagnosing and providing recommendations based on medical data, specifically targeting common injuries, infections, and blood pressure-related conditions for war victims. This application leverages machine learning and image recognition models to evaluate injuries or health issues and provide a structured diagnosis pipeline.

## Features

- **Injury Assessment:**
  - Detects injuries from images, such as fractures and dislocations.
  - Collects data from users to assess the injury severity.
  - Provides detailed recommendations or directs the user to seek professional medical help if necessary.

- **Infection Detection:**
  - Identifies symptoms of infections from user-provided images.
  - Offers a structured questioning pipeline to assess the level of infection and severity.
  - Suggests home remedies or recommends a doctor based on severity.

- **Blood Pressure and Stroke Risk Detection:**
  - Analyzes user-provided images to detect signs related to blood pressure and stroke risk.
  - Guides users through a diagnostic process to determine their health status.

- **AI-Powered Conversational Assistant:**
  - Provides a step-by-step conversational flow for gathering data from users about their health condition.
  - Based on the information provided, the assistant will evaluate and generate recommendations.

- **Medical Folder Database:**
  - All user interactions are stored in a **MySQL database**, creating a unique medical folder for each patient.
  - Medical data and diagnosis history are stored in real-time to provide a comprehensive view of the patient's medical history.
  - Each patient can access their medical information at any time via a global patient portal.

## How It Works

### Step-by-Step Injury Assessment:
1. **Image Upload:** 
   - The user uploads an image of their injury, which is then analyzed for signs of fractures, dislocations, or other injuries.
   
2. **Conversation Flow:** 
   - The assistant asks a series of structured questions to gather more data (e.g., pain levels, movement limitations).
   
3. **Diagnosis:** 
   - Based on the responses and image analysis, the assistant determines whether the user may have a fracture or other injury and provides recommendations.

4. **Final Recommendations:** 
   - If the injury is not deemed severe, the assistant provides home remedies. If it's severe, the assistant recommends seeking a doctor.

### Infection Assessment:
1. **Image Upload:** 
   - The user uploads an image showing signs of infection, such as wounds, skin conditions, or swelling.

2. **Conversation Flow:** 
   - The assistant follows a set of questions to determine the severity of the infection.
   
3. **Diagnosis:** 
   - Based on the analysis of the image and the user's responses, the assistant evaluates the infection risk.

4. **Final Recommendations:** 
   - Depending on the severity, the assistant either suggests home remedies or advises seeing a doctor.

### Blood Pressure & Stroke Risk:
1. **Image Upload:** 
   - The user uploads a related image or data indicating possible blood pressure issues or stroke risks.

2. **Diagnostic Questions:** 
   - The assistant asks questions related to the user's medical history and symptoms.

3. **Diagnosis:** 
   - Based on the uploaded data and responses, the assistant evaluates the likelihood of stroke or high blood pressure.

4. **Recommendations:** 
   - If the risk is minimal, home remedies or lifestyle changes are suggested. If the risk is high, the assistant advises seeking professional medical attention.

## AI Models

### **Injury Diagnosis Model:**
- Uses advanced deep learning models, including **Vision Transformers (ViT)**, to analyze images for signs of fractures, dislocations, or other injuries.
- The model has been trained to identify key features such as bone fractures and displacement.

### **Infection Diagnosis Model:**
- A deep learning-based image recognition model that analyzes uploaded images for signs of infection.
- The assistant uses a structured pipeline to ask the user targeted questions based on the detected symptoms.

### **Blood Pressure & Stroke Risk Model:**
- A classification model that predicts the likelihood of stroke or high blood pressure based on user data and images.

## MySQL Database: Storing Patient Medical Folders

### Overview:
HealNet utilizes a **MySQL database** to store patient information in real-time as the user interacts with the medical assistant. This ensures that each user’s medical history is automatically updated as they progress through the conversation. The system also provides the patient with the ability to access their medical data at any time.

### **Database Schema:**

The database stores patient medical data in a table structure, where each entry corresponds to a **unique user**. The schema is as follows:

```sql
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    dob DATE,
    medical_history TEXT,
    diagnosis TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE injuries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    injury_description TEXT,
    injury_type VARCHAR(100),
    injury_severity VARCHAR(50),
    diagnosis TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);

CREATE TABLE infections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    infection_description TEXT,
    infection_type VARCHAR(100),
    severity VARCHAR(50),
    treatment_recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

### **Real-Time Data Storage:**
- As patients engage with the medical assistant, their responses and diagnosis history are stored in real-time.
- The assistant continuously updates the database with each new assessment and recommendation.

### **Access to Medical Folders:**
- Each patient is assigned a unique medical folder in the database.
- The medical folder stores all interactions, diagnosis, and recommendations for easy access at any time.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/NoorMajdoub/HealNet.git
   cd HealNet
   ```

2. **Install Dependencies:**
   Make sure to install the necessary libraries using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MySQL Database:**
   - Create a MySQL database and tables based on the schema provided above.
   - Ensure the database connection credentials are correctly configured in the `.env` file.

4. **Set Up Environment Variables:**
   Create a `.env` file to store sensitive keys like database credentials.
   Example:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=healnet
   GEMINI_API_KEY=your_api_key
   ```

5. **Run the Application:**
   Use Uvicorn to run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API:**
   The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### **POST /injury-assessment/**
- This endpoint allows users to submit data related to their injury for assessment.
- **Request Body:**
  ```json
  {
    "conversation_history": ["previous conversation"],
    "user_input": "user response",
    "step": "initial"
  }
  ```
  - **conversation_history:** A list of prior conversations.
  - **user_input:** The user's response to a question (if applicable).
  - **step:** The current step of the assessment (`initial`, `first_assessment`, `physical_test`, `final_assessment`, `recommendation`).

- **Response:**
  Returns the next step in the diagnostic process or a recommendation.

### **POST /infection-assessment/**
- This endpoint allows users to submit data related to an infection for assessment.
- **Request Body:** Similar to the injury assessment.

- **Response:**
  Returns the recommendation based on infection severity.

## Contributing

Feel free to fork the project and submit pull requests for any changes or improvements. Contributions are always welcome!

