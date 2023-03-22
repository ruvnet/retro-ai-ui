import openai
import os

openai.api_key = os.environ.get("OPENAI_API_KEY")

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

from flask import jsonify

@app.route('/gpt3', methods=['POST'])
def gpt3():
    prompt = request.form['prompt']
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return jsonify(response.choices[0].text)
