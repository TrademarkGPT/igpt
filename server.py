from flask import Flask, request, jsonify
import interviewgpt

app = Flask(__name__)

@app.route('/start_chat', methods=['POST'])
def start_chat():
    # Extract parameters from the request
    resume = request.json['resume']
    job_description = request.json['job_description']
    interviewer_company = request.json['interviewer_company']
    interviewer_role = request.json['interviewer_role']
    difficulty = request.json['difficulty']
    interview_scope = request.json['interview_scope']
    openai_api_key = request.json['openai_api_key']

    # Use the function from interviewgpt to start the chat
    message = interviewgpt.start_chat(openai_api_key, resume, job_description, interviewer_company, interviewer_role, difficulty, interview_scope)

    # Return the first AI message
    return jsonify({"message": message})

@app.route('/send_message', methods=['POST'])
def send_message():
    # Extract parameters from the request
    openai_api_key = request.json['openai_api_key']
    messages = request.json['messages']

    # Use the function from interviewgpt to send a message
    message = interviewgpt.send_message(openai_api_key, messages)

    # Return the AI's response
    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)
