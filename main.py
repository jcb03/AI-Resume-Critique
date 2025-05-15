import streamlit as st
from openai import OpenAI
import os
import io
import PyPDF2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#set page configuration
st.set_page_config(page_title="AI Resume Critiquer",page_icon="📄",layout="centered")

st.title("AI Resume Critiquer")
st.markdown("Upload your resume in PDF format and get feedback on how to improve it.")

# Initialize OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    st.error("Please set your OpenAI API key in the .env file.")
    st.stop()

uploaded_file = st.file_uploader("Upload your resume (PDF | TXT)", type=["pdf","txt"]) 
job_role= st.text_input("Enter the job role you are applying for (e.g., Software Engineer, Data Scientist):")

analyze_button = st.button("Analyze Resume")

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

if analyze_button and uploaded_file:
    try:
        file_content=



