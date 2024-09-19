import streamlit as st
from openai import OpenAI
import fitz  # PyMuPDF for reading PDFs

# Show title and description.
st.title("Disha Negi📄 Document Question Answering")
st.write(
    "Upload a document below (PDF or TXT) and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader("Upload a document (.txt or .pdf)", type=("txt", "pdf"))

    # Function to read PDF file using PyMuPDF (fitz)
    def read_pdf(file):
        try:
            # Using PyMuPDF (fitz)
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()
            return text
        except Exception as e:
            st.error(f"Error reading PDF: {e}")
            return None

    # Function to handle the uploaded file based on its type.
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        document = None
        if file_extension == 'txt':
            document = uploaded_file.read().decode()
        elif file_extension == 'pdf':
            document = read_pdf(uploaded_file)

        # Ask the user for a question via `st.text_area`.
        question = st.text_area(
            "Now ask a question about the document!",
            placeholder="Can you give me a short summary?",
            disabled=not document,
        )

        if document and question:
            messages = [
                {
                    "role": "user",
                    "content": f"Here's a document: {document} \n\n---\n\n {question}",
                }
            ]

            # Generate an answer using the OpenAI API.
            response = client.chat.completions.create(
                model="gpt-4",  # Use a valid model like "gpt-4"
                messages=messages
            )

            # Extract and display the answer
            answer = response.choices[0].message.content
            st.write("Answer:")
            st.write(answer)

    # If the file is removed from the UI, clear the document data.
    if not uploaded_file:
        document = None