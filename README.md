# Sofy - Ai Mentor App

Sofy AI is a Flask-based web application that uses OpenAI's GPT-4 to provide software development mentorship.

## Features

- User can ask questions and get responses from an AI mentor.
- Chat history is saved in the browser's local storage.
- Responsive design with Bootstrap.

## Prerequisites

- Python 3.6 or higher

## Setup

- Clone the repository: `git clone https://github.com/curiousprogrammer/mentor-app.git`
- Change to the project directory: `cd mentor-app`
- Create a virtual environment: `python -m venv venv`
- Activate the virtual environment:
  - On Windows: `venv\Scripts\activate`
  - On macOS and Linux: `source venv/bin/activate`
- Install the dependencies: `pip install -r requirements.txt`
- Set the Flask app: `export FLASK_APP=app.py`
- Run the app: `flask run`

## Deployment

To deploy the application, you can use platforms like Heroku. Ensure you have the `Procfile` and the necessary environment variables set up.

## License

This project is licensed under the MIT License.
