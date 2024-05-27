from flask import Flask, request, jsonify, render_template
import openai
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def setup_openai_api():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise Exception("OPENAI_API_KEY not found in environment variables. Make sure to set it.")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        question = request.form['question']
        conversation = json.loads(request.form['conversation'])

        messages = [{"role": role, "content": content} for role, content in conversation]

        messages.insert(0, {"role": "system", "content": "You are Sofy, a genius software developer..."})

        messages.append({"role": "user", "content": question})

        response_generator = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0,
            max_tokens=325,
            
        )
        response_text = response_generator.choices[0].message['content']
    except openai.error.OpenAIError as e:
        response_text = f"An error occurred: {str(e)}"

    return jsonify(question=question, response=response_text)

def main():
    # Setup OpenAI API
    setup_openai_api()

    # Start the Flask server
    app.run(debug=True)

if __name__ == "__main__":
    main()
