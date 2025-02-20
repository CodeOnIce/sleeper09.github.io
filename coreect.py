import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
# Updated PDF to text function
def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text
genai.configure(api_key="AIzaSyDfOtyWVEHiMLiYqMV-7y70HKddyGu_6Jw")
# Function to generate answer from the extracted text using Google's generative AI
def get_answer_from_model(question, text):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content([question+text])
    return response.text


# Streamlit App
def main():
    st.title("PDF Q&A App ")

    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file is not None:
        # Extract text from PDF
        with st.spinner("File Processed successfully!.."):
            text = extract_text_from_pdf(uploaded_file)
            st.success("File Processed successfully!")
        

            # Input question
            question = st.text_input("Ask a question about the document:")

            if st.button("Get Answer"):
                with st.spinner("Getting answer..."):
                    answer = get_answer_from_model(question, text)
                    st.success("Answer generated!")
                    st.write(answer)

if __name__ == "__main__":
    main()
