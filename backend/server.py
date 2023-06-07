import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
import openai


load_dotenv("../.env")
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return "What you want?"


@app.route("/chat", methods=["POST"])
def chat():
    try:
      data = request.json
      messages = data["messages"]
      if type(messages) != list or len(messages) == 0:
        raise Exception
    except Exception:
      return {"error": "invalid request body"}, 400
    
    try:
      response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
      )['choices'][0]['message']['content']
      if not response:
        raise Exception
      return {"answer": response}, 200
    except Exception:
      return {"error": "OpenAI failure"}, 500