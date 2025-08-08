# 🧠 Intelligent Health Risk Predictor

A full-stack AI-powered web application that predicts patient health risk using vital stats like BMI, blood pressure, glucose level, and smoking habits. The backend uses FastAPI and a local LLM, while the frontend is built with Streamlit. Patient data and predictions are stored in a MySQL database.

---

## 📁 Project Structure
intelligent-health-risk-predictor/
├── backend/
│ └── main.py # FastAPI backend
├── streamlit_ui/
│ └── app.py # Streamlit frontend
├── requirements.txt
├── venv/ # Virtual environment (excluded from Git)
└── README.md


---

## ⚙️ Tech Stack

- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **Database:** MySQL  
- **LLM:** Gemma3 (via Ollama or local service)  
- **Lang:** Python 3.10+

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
bash
git clone https://github.com/your-username/intelligent-health-risk-predictor.git
cd intelligent-health-risk-predictor

 ## 🖥️ Backend Setup (FastAPI)
📌 Requirements
Python 3.10+
MySQL running locally
Ollama / LLM service running on http://localhost:11434

Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install backend requirements
pip install -r requirements.txt

Start the FastAPI server
cd backend
uvicorn main:app --reload --port 8000

## 🌐 Frontend Setup (Streamlit UI)

Activate virtual environment if not already active
source venv/bin/activate  # Or venv\Scripts\activate on Windows

Run Streamlit app
cd streamlit_ui
streamlit run app.py

## 🛠️ MySQL Database Setup
Create the patient_records table:
CREATE DATABASE IF NOT EXISTS health_platform;

USE health_platform;

CREATE TABLE patient_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    bmi FLOAT,
    bp FLOAT,
    glucose FLOAT,
    smoker VARCHAR(10),
    risk_score FLOAT,
    advice TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




