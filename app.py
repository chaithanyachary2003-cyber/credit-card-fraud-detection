import streamlit as st
import pickle
import pandas as pd
import mysql.connector

# ---------------------------
# Load Model
# ---------------------------
with open("fraud_model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------------------------
# MySQL Connection
# ---------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="chaitu",
    password="chaitu555",
    database="fraud_detection"
)

cursor = conn.cursor()

st.set_page_config(page_title="Credit Card Fraud Detection")

st.title("💳 Credit Card Fraud Detection")

st.write("Enter transaction details below")

# ---------------------------
# User Inputs
# ---------------------------
inputs = []

feature_names = [
    "Time","V1","V2","V3","V4","V5","V6","V7","V8","V9",
    "V10","V11","V12","V13","V14","V15","V16","V17","V18",
    "V19","V20","V21","V22","V23","V24","V25","V26","V27",
    "V28","Amount"
]

for feature in feature_names:
    value = st.number_input(feature, value=0.0)
    inputs.append(value)

# ---------------------------
# Prediction
# ---------------------------
if st.button("Predict"):

    data = pd.DataFrame([inputs], columns=feature_names)

    prediction = model.predict(data)[0]
    confidence = model.predict_proba(data).max()

    if prediction == 1:
        result = "Fraud"
        st.error("⚠️ Fraud Transaction")
    else:
        result = "Normal"
        st.success("✅ Normal Transaction")

    sql = """
    INSERT INTO predictions
    (transaction_amount,prediction,confidence)
    VALUES(%s,%s,%s)
    """

    cursor.execute(
        sql,
        (
            data["Amount"][0],
            result,
            float(confidence)
        )
    )

    conn.commit()

    st.write("Confidence:", round(confidence*100,2),"%")
    st.success("Prediction Saved to MySQL")