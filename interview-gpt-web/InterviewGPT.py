import openai
import streamlit as st
from openai import ChatCompletion

def generate_system_prompt(resume, job_description, interviewer_company, interviewer_role, difficulty, interview_scope):
    system_prompt = f"""
    You are AI-interviewer, an AI designed to act out the persona of a specific custom interviewer that interviews a user in this app. The specific context of the interview is below. 

    As the AI-interviewer your position is "{interviewer_role}" at the company, "{interviewer_company}", you can extrapolate on what that company does based on your knowledge cutoff of 2021, and if you don't know you can just act as the title you are given. You should ask questions one at a time continuously that someone with your position in the company at {interviewer_company} would likely ask. Every response you have should have a question at some point.  
    
    You are interviewing a candidate with this job description, "{job_description}". The interviewee's resume is "{resume}". Ask the interviewee specific questions based off of their resume, "{resume}" with consideration for the person's individual background and expiriences in their Job Description, "{job_description}". 

    The interview difficulty is how hard the questions are, and how disagreeable the AI interviewer persona you are acting out on a scale of 0-10. Your difficulty setting is set to difficulty{difficulty}. If you are given a interview difficulty that is closer to 10, then you should tend to disagree with most answers or challenge the interviewee by asking more follow up questions. If the difficulty is closer to 1 in the scale, you will not challenge very much and give easier questions. 

    Your AI interview questions should specifically pertain to the interview scope of "{interview_scope}", if interview scope is not provided here, you can ignore this sentence.
    
    """
    return system_prompt

# Sidebar inputs
with st.sidebar:
    st.title("Details for InterviewGPT")
    resume = st.text_area("Input Resume (JSON Format)")
    job_description = st.text_area("Input Job Description")
    interviewer_company = st.text_input("AI Interviewer Company")
    interviewer_role = st.text_input("Role of AI Interviewer")
    difficulty = st.slider("Difficulty", min_value=1, max_value=10)
    interview_scope = st.text_input("Custom Interview Scope", value="")
    openai_api_key = st.text_input("OpenAI API Key", type="password")

# Main application
st.title("💬 Chatbot")

# Initialize messages if not done yet
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Start chat when button is pressed
start_button, clear_button = st.columns(2)
if start_button.button("Start Chat"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    openai.api_key = openai_api_key

    system_prompt = generate_system_prompt(resume, job_description, interviewer_company, interviewer_role, difficulty, interview_scope)

    # Initialize the chat with the system prompt
    chat = ChatCompletion.create(
        model="gpt-4-0613",  # You may need to adjust this depending on which model you're using
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ""}
        ],
        temperature=0.6,  # Adjust this value to control randomness
    )

    # Add the first message from the AI to the chat
    st.session_state["messages"].append({"role": "assistant", "content": chat['choices'][0]['message']['content']})

if clear_button.button("Clear History"):
    st.session_state["messages"] = []

# Display the chat messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# User input
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""
user_input = st.text_input("Your message:", value=st.session_state["user_input"])

submit_button = st.button("Submit")

if submit_button and user_input:
    # Add user's message to the chat
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Send the user's message to the AI
    chat = ChatCompletion.create(
        model="gpt-4-0613",
        messages=st.session_state["messages"],
        temperature=0.2,  # Adjust this value to control randomness
    )

    # Add the AI's response to the chat
    st.session_state["messages"].append({"role": "assistant", "content": chat['choices'][0]['message']['content']})

    # Clear the text input box for the next user input
    st.session_state.user_input = ""
    st.experimental_rerun()
