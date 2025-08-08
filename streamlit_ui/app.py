import streamlit as st
import requests
import mysql.connector

st.set_page_config(page_title="🩺 Intelligent Health Platform")
st.title("🧠 Intelligent Health Risk Predictor")

tab1, tab2 = st.tabs(["📝 Patient Form", "📊 Patient History"])

with tab1:
    st.subheader("Enter Patient Details")
    with st.form("patient_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120, 1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        bmi = st.number_input("BMI", format="%.2f")
        bp = st.number_input("Blood Pressure (Systolic)", format="%.1f")
        glucose = st.number_input("Glucose Level", format="%.1f")
        smoker = st.selectbox("Do you smoke?", ["Yes", "No"])
        submitted = st.form_submit_button("Submit")
    if submitted:
        payload = {
            "name": name,
            "age": age,
            "gender": gender,
            "bmi": bmi,
            "bp": bp,
            "glucose": glucose,
            "smoker": smoker
        }
        try:
            resp = requests.post("http://localhost:8000/predict", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                st.success(f"🧪 Prediction: {data['prediction']}")
                st.info(f"💡 Advice: {data['advice']}")
            else:
                st.error("Error from backend.")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")

with tab2:
    st.subheader("📜 Patient History")
    if 'load' not in st.session_state or st.session_state.load:
        st.session_state.load = False
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="sanjana2005",
                database="health_platform"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT id, name, age, gender, bmi, bp, glucose, smoker, risk_score, advice, created_at
                FROM patient_records ORDER BY created_at DESC
            """)
            st.session_state.records = cursor.fetchall()
            conn.close()
        except Exception as e:
            st.error(f"Unable to load history: {e}")
            st.session_state.records = []

    if st.session_state.records:
        for rec in st.session_state.records:
            with st.container():
                st.write(f"**{rec['name']}** | Risk: {rec['risk_score']}%")
                st.write(rec['advice'])
                if st.button("🗑️ Delete record", key=f"del_{rec['id']}"):
                    resp = requests.delete(f"http://localhost:8000/records/{rec['id']}")
                    if resp.status_code in (200, 204):
                        st.success("Deleted! Refreshing...")
                        st.session_state.load = True
                        st.rerun()
                    else:
                        st.error(f"Failed to delete: {resp.status_code}")
                st.markdown("---")
    else:
        st.info("No history found.")
