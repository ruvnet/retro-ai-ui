import openai
import os
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from datetime import datetime, timedelta

openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

prompt_dict = {}

@app.route('/')
def index():
    return render_template('index.html', prompts=prompt_dict)

@app.route('/add', methods=['POST'])
def add_prompt():
    prompt = request.form['prompt'].strip()
    response = request.form['response'].strip()
    if prompt and response:
        prompt_dict[prompt] = response
        flash('Prompt added successfully.')
    else:
        flash('Prompt or response cannot be empty.')
    return redirect(url_for('index'))

@app.route('/gpt3', methods=['POST'])
def gpt3():
    prompt = request.form['prompt']

    # Initialize message_history in session if it doesn't exist
    if 'message_history' not in session:
        session['message_history'] = []

    # Append the user input to message_history
    session['message_history'].append("User: " + prompt)

    def get_openai_response(user_input, message_history):
        # Convert message history to the format required by the API
        api_messages = [{"role": msg.split(': ')[0].lower(), "content": msg.split(': ')[1]} for msg in message_history]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            max_tokens=1200,
            temperature=0.85,
            n=1,
            stream=False
        )
        return response.choices[0].message['content']

    try:
        response_text = get_openai_response(prompt, session['message_history'])
        # Append the assistant's response to message_history
        session['message_history'].append("Assistant: " + response_text.strip())
        session.modified = True  # Ensure the session is saved after modification
        return jsonify({"text": response_text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})

import json

@app.route('/clear_session', methods=['GET'])
def clear_session():
    session.clear()
    return jsonify({"result": "Session cleared"})

@app.route('/history')
def history():
    if 'message_history' in session:
        message_history = session['message_history']
        # Convert the message history array to a JSON string
        history_str = json.dumps(message_history)
        return jsonify({"history": history_str})
    else:
        return jsonify({"history": "No message history found in the current session."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
