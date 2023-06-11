from flask import Flask, request, jsonify, render_template
import openai
import os
import json
from dotenv import load_dotenv


# Load the environment variables
load_dotenv()

app = Flask(__name__)

# Get the OpenAI API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])  
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])  # The URL /ask is mapped to this function 
def ask(): 
    question = request.form['question']
    print("Question:", question)

    conversation = json.loads(request.form['conversation'])  # Get the conversation from the form data

    # Convert the conversation history to the format expected by the OpenAI API
    messages = [{"role": role, "content": content} for role, content in conversation]

    # Add a system message to set the context
    messages.insert(0, {"role": "system", "content": "You are Sofy, a friendly and knowledgeable AI mentor with years of programming experience. You are patient, supportive, and always eager to share valuable insights and resources like tutorials, documentation, and best practices to help users learn software development."})

    # Add the question to the conversation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=325,
        n=1,
        stop=None,
        temperature=0,
        top_p=1,
    )
    response_text = response.choices[0].message['content'] + "\n"

    # Add the answer to the conversation
    return jsonify(response=response_text) 

if __name__ == "__main__":
    app.run(debug=True)
