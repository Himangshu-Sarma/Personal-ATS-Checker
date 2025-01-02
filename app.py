from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import base64
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(prompt, pdf_content, input_text):
    ## generating content based upon the input_text and prompt
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([prompt, pdf_content[0], input_text])
    return response

def input_pdf_convert(uploaded_file):
    ## converting the pdf to image
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        print(images)

        first_page = images[0]

        ## converting to bytes
        image_byte_arr = io.BytesIO()
        first_page.save(image_byte_arr, format = 'JPEG')
        image_byte_arr = image_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image_byte_arr).decode()
            }
        ]

        return pdf_parts

    else:
        raise FileNotFoundError("No file uploaded")

## streamlit application

st.set_page_config(page_title = "Personal ATS Checker")
st.header("Personal ATS Checker")

input_text = st.text_area("Paste the Job Desciption: ", key = "input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type = ["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise my skills ?")

submit3 = st.button("What Are The Keywords That Are Missing ?")

submit4 = st.button("Percentage Match")

prompt1 = """
    You are an experienced Technical Human Resource Manager, your task is to review my provided resume against the job description. 
    Please share your professional evaluation on whether my profile aligns with the role higlighting the strengths and weaknesses about me.
"""

prompt2 = """
    You are an experienced Technical Human Resource Manager, your task is to provide the ways to improvise my skills against the job description.
"""

prompt3 = """
    You are an advanced ATS(Applicant Tracking System) scanner with deep understanding of IT Jobs and their requirements and deep ATS functionality. Your task is to evaluate my resume against the job description by highlighting the keywords that are missing in the resume.
"""

prompt4 = """
    You are an advanced ATS(Applicant Tracking System) scanner with deep understanding of IT Jobs and their requirements and deep ATS functionality. Your task is to evaluate my resume against the job description by highlighting the percentage match and also share the final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_convert(uploaded_file)
        response = get_gemini_response(prompt1, pdf_content, input_text)
        st.subheader("The response is : ")
        st.write(response.text)

    else:
        st.write("Please upload the resume !!!")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_convert(uploaded_file)
        response = get_gemini_response(prompt2, pdf_content, input_text)
        st.subheader("The response is : ")
        st.write(response.text)

    else:
        st.write("Please upload the resume !!!")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_convert(uploaded_file)
        response = get_gemini_response(prompt3, pdf_content, input_text)
        st.subheader("The response is : ")
        st.write(response.text)

    else:
        st.write("Please upload the resume !!!")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_convert(uploaded_file)
        response = get_gemini_response(prompt4, pdf_content, input_text)
        st.subheader("The response is : ")
        st.write(response.text)

    else:
        st.write("Please upload the resume !!!")