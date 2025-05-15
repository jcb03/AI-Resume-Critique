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

st.title("AI Resume Critiquer") # Set the title of the app
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
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
    
# Function to extract text from uploaded file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read())) # Read PDF file
    return uploaded_file.read().decode("utf-8") # Checking if the file is a text file

if analyze_button and uploaded_file:
    try:
        file_content= extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("The uploaded file is empty or not readable.")
            st.stop()

        # Initialize prompt
        prompt = f"""Please analyze this resume and provide constructive feedback according to the job role if mentioned.
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Formatting and layout
        5. Specific improvements for {job_role if job_role else 'general job applications'}

        resume content:
        {file_content}
        """
        client = OpenAI(api_key=OPENAI_API_KEY) # Initialize OpenAI client to access the API
        # Call OpenAI API to get feedback
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer, Analyze the resume and provide feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500, # Adjust max tokens based on your needs
            temperature=0.7 # Adjust temperature for creativity
        )
        st.markdown("### Feedback:") # Display feedback header
        st.markdown(response.choices[0].message['content']) # Display the feedback
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
# Add a footer
st.markdown("Made with ❤️ by Jai Chaudhary")
# Add a link to the GitHub repository
st.markdown("Checkout my github repository [Github-jcb03](https://github.com/jcb03/AI-Resume-Critique)")
# Add a link to the LinkedIn profile
st.markdown("Connect with me on [LinkedIn-Jai Chaudhary](https://www.linkedin.com/in/jai-chaudhary-54bb86221/)")