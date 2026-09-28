# AI Study Assistant

A beginner-friendly AI-powered study assistant built using Python, Streamlit, and Ollama.

## Features
- Generate study plans
- Create personalized plans using a local AI model
- Ask study-related questions
- Track study progress
- Save and download progress as CSV

## Technologies
- Python
- Streamlit
- Ollama
- Llama 3.2 1B
- Pandas

## Run Locally
1. Install the required packages:
   `py -3.13 -m pip install streamlit requests pandas`

2. Install Ollama and download the model:
   `ollama pull llama3.2:1b`

3. Start the app:
   `py -3.13 -m streamlit run app.py`
