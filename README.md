
# InterviewGPT Application

This application is designed to use OpenAI's GPT model to simulate an interactive job interview experience. It consists of two main components: a Streamlit app for interaction (`InterviewGPT.py`) and a Flask API server (`server.py`).

## Application Overview

The main application (`InterviewGPT.py`) is a Streamlit app where the user can interact with the AI in a chat-like interface. This application takes user inputs such as resume details, job description, the company of the interviewer, the role of the interviewer, difficulty level, and interview scope. These details are used to tailor the AI's responses to simulate an authentic job interview environment. 

The Flask API server (`server.py`) serves as an interface for the Streamlit app to interact with the OpenAI API. It handles requests to start a chat, send a message, and clear the chat history.

## Running the Application Locally

### Pre-requisites

Ensure you have the following installed:

- Python 3.7 or later
- pip (Python package installer)
- Streamlit
- Flask
- OpenAI Python package

The necessary Python packages can be installed via pip:
```bash
pip install streamlit flask openai
```

### Running the Streamlit App

In the terminal, navigate to the directory containing `InterviewGPT.py`. Run the following command to start the Streamlit app:

```bash
streamlit run InterviewGPT.py
```

This will start the Streamlit app and a new tab should open in your default web browser displaying the app. If it doesn't open automatically, you can manually navigate to the address output in your terminal (usually `http://localhost:8501`).

### Running the Flask Server 

In a separate terminal window, navigate to the directory containing `server.py`. Run the following command to start the Flask server:

```bash
python server.py
```

This will start the Flask server. By default, it will be running on `http://localhost:5000`.

## Application Flow

1. Start the Streamlit app and Flask server as described above.
2. In the Streamlit app, enter the necessary details in the sidebar. 
3. Click "Start Chat". This sends a POST request to the Flask server's `/start_chat` endpoint, initiating the AI interview.
4. The AI's first message will appear in the chat window. You can respond in the "Your message" input field and press "Submit" to continue the conversation. Each message exchange involves a POST request to the Flask server's `/send_message` endpoint.
5. To reset the conversation, click "Clear History". This sends a POST request to the Flask server's `/clear_chat` endpoint, resetting the conversation history.

## API Usage

The server provides three main API endpoints:

1. **Start Chat** (`POST /start`): This endpoint initializes a new chat session. It requires a JSON body with the following structure:

```json
{
    "resume": "your resume here",
    "job_description": "job description here",
    "interviewer_company": "company name here",
    "interviewer_role": "role here",
    "difficulty": difficulty level (1-10),
    "interview_scope": "interview scope here",
    "openai_api_key": "your OpenAI API key here"
}
```

Example usage:

```sh
curl -X POST http://localhost:5014/start -H "Content-Type: application/json" -d '{
    "resume": "Software Engineer with 5 years of experience in Python...",
    "job_description": "Looking for a Python developer...",
    "interviewer_company": "OpenAI",
    "interviewer_role": "HR Manager",
    "difficulty": 7,
    "interview_scope": "Python development",
    "openai_api_key": "your OpenAI API key"
}'
```

2. **Send Message** (`POST /send`): This endpoint is used to send a message from the user to the chatbot. It requires a JSON body with the following structure:

```json
{
    "messages": [
        {
            "role": "system",
            "content": "initial system message here"
        },
        {
            "role": "user",
            "content": "your message here"
        }
    ],
    "openai_api_key": "your OpenAI API key here"
}
```

Example usage:

```sh
curl -X POST http://localhost:5014/send -H "Content-Type: application/json" -d '{
    "messages": [
        {
            "role": "system",
            "content": "You are ChatGPT, a large language model..."
        },
        {
            "role": "user",
            "content": "Hello, ChatGPT!"
        }
    ],
    "openai_api_key": "your OpenAI API key"
}'
```

3. **Clear Chat** (`POST /clear`): This endpoint is used to clear the chat history. It does not require a request body.

Example usage:

```sh
curl -X POST http://localhost:5014/clear
```


## Note on OpenAI API Key

This application requires an OpenAI API key to function. You can enter your API key in the OpenAI API Key field in the Streamlit app sidebar. Be sure to keep your API key secure and do not expose it in shared or public code.

## Known Limitations

- The Streamlit app does not support persistent state across reruns. Therefore, the chat history will be lost if the app is rerun or refreshed.
- Currently, the Flask server does not persist chat history between different runs of the server.

## Future Improvements

- Implement chat history persistence to maintain the conversation across multiple app and server runs.
- Improve error handling and user feedback for API errors or invalid inputs.
- Enhance the UI/UX of the Streamlit app for a more engaging user experience.

## Contributing

We welcome contributions to improve this application. Please feel free to raise issues or submit pull requests.

