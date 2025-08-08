from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import numpy as np
import mysql.connector

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

class PatientData(BaseModel):
    name: str
    age: int
    gender: str
    bmi: float
    bp: float
    glucose: float
    smoker: str

# MySQL connection — update credentials
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sanjana2005",
    database="health_platform"
)
cursor = db.cursor()

@app.post("/predict")
def predict(data: PatientData):
    smoker_flag = 1 if data.smoker.lower() == "yes" else 0
    raw_score = data.bmi + data.bp / 2 + data.glucose / 2 + 5 * smoker_flag
    risk_score = round(min(raw_score / 100, 1.0), 2)

    prompt = (
        f"You are a helpful health assistant.\n\n"
        f"Patient Profile:\n"
        f"- Age: {data.age}\n"
        f"- BMI: {data.bmi}\n"
        f"- Blood Pressure: {data.bp}\n"
        f"- Glucose Level: {data.glucose}\n"
        f"- Smoker: {data.smoker}\n\n"
        f"Risk Score: {risk_score}\n\n"
        f"Please provide short, friendly health advice."
    )

    try:
        resp = requests.post("http://localhost:11434/api/generate", json={
            "model": "gemma3",
            "prompt": prompt,
            "stream": False
        })
        resp_json = resp.json()
        print("LLM response:", resp_json)  # Debug log
        advice = resp_json.get("response", "").strip()
    except Exception as e:
        advice = f"Error generating advice: {e}"
        print("LLM error:", e)

    if not advice:
        advice = "No advice generated. Please try again."

    insert_sql = """
        INSERT INTO patient_records (
            name, age, gender, bmi, bp, glucose, smoker, risk_score, advice
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_sql, (
        data.name, data.age, data.gender, data.bmi,
        data.bp, data.glucose, data.smoker, risk_score, advice
    ))
    db.commit()

    return {"prediction": f"{risk_score * 100:.0f}%", "advice": advice}

@app.delete("/records/{record_id}", status_code=204)
def delete_record(record_id: int):
    cursor.execute("DELETE FROM patient_records WHERE id = %s", (record_id,))
    db.commit()
    return Response(status_code=204)
