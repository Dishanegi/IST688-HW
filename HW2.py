import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
from mistralai import Mistral
from anthropic import Anthropic

# Function to read the content from a URL
def read_url_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        st.error(f"Error reading {url}: {e}")
        return None

# Function to call OpenAI API
def call_openai(api_key, document, instruction):
    try:
        openai.api_key = api_key
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {instruction}"
            }
        ]

        # Generate the summary using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )

        # Stream the response to the app
        st.write(response['choices'][0]['message']['content'].strip())

    except Exception as e:
        st.error(f"Error with OpenAI: {e}")

# Function to call Claude API
def call_claude(api_key, document, instruction):
    try:
        anthropic_client = Anthropic(api_key=api_key)
        formatted_prompt = f"Here's a document: {document} \n\n---\n\n {instruction}"

        response = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": formatted_prompt}
            ],
            temperature=0.5
        )

        # Process the response
        if hasattr(response, 'content') and isinstance(response.content, list):
            st.write(response.content[0].text)
        else:
            return "Unexpected response format from Claude API."
    except Exception as e:
        st.error(f"Error with Claude: {e}")

# Function to call Mistral API
def call_mistral(api_key, document, instruction):
    try:
        mistral_client = Mistral(api_key=api_key)
        formatted_prompt = f"Here's a document: {document} \n\n---\n\n {instruction}"

        response = mistral_client.chat.complete(
            model="mistral-large-latest",
            messages=[{"role": "user", "content": formatted_prompt}]
        )
        # Process the response
        if response.choices and len(response.choices) > 0:
            st.write(response.choices[0].message.content.strip())

    except Exception as e:
        st.error(f"Error with Mistral: {e}")

# Title with custom styling
st.markdown('<h1 class="title">HW-02: Disha Negi URL Summarization</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Enter a URL below, choose an LLM, and see how the content is summarized!</h3>', unsafe_allow_html=True)

# URL input
url = st.text_input("Enter a URL:")

# Sidebar for selecting the LLM
st.sidebar.title("LLM Selection")
llm_option = st.sidebar.selectbox(
    "Select the LLM to use:",
    ("OpenAI", "Claude", "Mistral")
)

# Sidebar for summary options
st.sidebar.title("Choose Summary Format")
summary_options = st.sidebar.radio(
    "Select a format for summarizing the document:",
    (
        "Summarize the document in 100 words",
        "Summarize the document in 2 connecting paragraphs",
        "Summarize the document in 5 bullet points"
    ),
)

# Language dropdown
language_options = st.selectbox(
    "Select the output language:",
    ("English", "French", "Spanish")
)

# Summarization button with styling
if st.button("Summarize"):
    if url:
        document = read_url_content(url)
        if document:
            instruction = f"Summarize the document in {summary_options.lower()} in {language_options.lower()}."

            if llm_option == "OpenAI":
                call_openai(st.secrets["openai_api_key"], document, instruction)
            elif llm_option == "Claude":
                call_claude(st.secrets["claude_api_key"], document, instruction)
            elif llm_option == "Mistral":
                call_mistral(st.secrets["mistral_api_key"], document, instruction)
    else:
        st.error("Please enter a valid URL.")

# Apply custom CSS to beautify the app
st.markdown("""
    <style>
    /* Change the font color of the title */
    .title {
        color: #2E86C1;
        font-family: 'Helvetica', sans-serif;
        font-size: 48px;
        font-weight: bold;
    }

    /* Style for subtitles */
    .subtitle {
        color: #117A65;
        font-family: 'Arial', sans-serif;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    /* Style for normal text */
    .normal-text {
        color: #1F618D;
        font-family: 'Verdana', sans-serif;
        font-size: 18px;
        margin-bottom: 10px;
    }

    /* Background color for the main content */
    .stApp {
        background-color: #FBFCFC;
    }

    /* Style the button */
    div.stButton > button {
        background-color: #117A65;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        font-size: 18px;
        border: none;
        transition: none; /* Disable any transition effects */
    }

    /* Explicitly remove hover effect */
    div.stButton > button:hover {
        background-color: #117A65;
        color: white;
        border: none;
        transform: none;
        transition: none;
    }

    /* Style for the sidebar */
    .css-1d391kg {
        background-color: #D4E6F1;
    }

    /* Style input boxes */
    input {
        border: 2px solid #117A65;
        border-radius: 5px;
        padding: 5px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)