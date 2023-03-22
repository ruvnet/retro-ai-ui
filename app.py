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
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return jsonify({"text": response.choices[0].text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)