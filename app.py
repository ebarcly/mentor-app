from flask import Flask, request, jsonify, render_template
import openai
import os
import json
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

app = Flask(__name__)

def setup_openai_api():
    """Sets up the OpenAI API with the key from environment variables."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if openai.api_key is None:
        raise Exception("OPENAI_API_KEY not found in environment variables. Make sure to set it.")

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
    messages.insert(0, {"role": "system", "content": "You are Sofy, a genius software developer that excels at teaching others. You are going to teach me Software development step-by-step with your excellent teaching skills you are going to make sure I learn everything I need to become better everyday. You are also, learn from my questions and reformulate things in a way I can grasp it better. You can ask questions to test my knowledge and make sure I am learning."})

    # Add the question to the conversation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        max_tokens=325,
        n=1,
        stop=None,
        temperature=0,
        top_p=1,
    )
    response_text = response.choices[0].message['content']

    # Add the answer to the conversation
    return jsonify(question=question, response=response_text)

def main():
    # Setup OpenAI API
    setup_openai_api()

    # Start the Flask server
    app.run(debug=True)

if __name__ == "__main__":
    main()