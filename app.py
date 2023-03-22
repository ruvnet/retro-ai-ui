import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'

prompt_dict = {}

@app.route('/')
def index():
    return render_template('index.html', prompts=prompt_dict)

@app.route('/gpt3', methods=['POST'])
def gpt3():
    prompt = request.form['prompt']
    
    # Prepare the message history for the API
    message_history = ["User: " + prompt]
    
    def get_openai_response(user_input, message_history):
        # Convert message history to the format required by the API
        api_messages = [{"role": msg.split(': ')[0].lower(), "content": msg.split(': ')[1]} for msg in message_history]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=api_messages,
            max_tokens=200,
            temperature=0.1,
            n=1,
            stream=False
        )
        return response.choices[0].message['content']

    try:
        response_text = get_openai_response(prompt, message_history)
        return jsonify({"text": response_text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)