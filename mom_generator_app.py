import streamlit as st
import requests
import base64
import json

API_URL = "https://wokzr5w6s9.execute-api.ap-south-1.amazonaws.com/momgenerator/upload-mom"

def send_mom(file, email_id):
    file_content = base64.b64encode(file.read()).decode("ascii")
    payload = json.dumps({
        "isBase64Encoded": True,
        "body": file_content,
        "headers": {"Content-Type": "multipart/form-data"},
        "queryStringParameters": {"email_id": email_id}
    })
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, data=payload, headers=headers)
    return response.json()

st.set_page_config(layout="wide")
st.title("MOM Generator")

email_id = st.text_input("Enter your email:")

if email_id and not email_id.endswith("@ganitinc.com"):
    st.error("Only emails from ganitinc.com domain are allowed.")
    st.stop()

st.write("You can upload a **Teams meeting transcription** for best results. If unavailable, you may upload rough meeting notes with all tasks discussed, including owners and dates (no specific format required).")

uploaded_file = st.file_uploader("Upload MOM Document", type=["docx"])

if uploaded_file and st.button("Upload & Send MOM", use_container_width=True):
    with st.spinner("Uploading..."):
        response = send_mom(uploaded_file, email_id)
    st.success(f"MOM has been sent to {email_id}")
