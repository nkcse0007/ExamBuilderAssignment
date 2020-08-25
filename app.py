from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from src.Authentication.index import auth_app
from src.Task.index import task_app
from src.Configure.index import configure_app
from src.Intent.index import intent_app
from src.GoogleAssistant.index import voice_app
from src.Conversation.index import conversation_app

# from src.Authentication.webhook import hook_route

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)
# to see the full request and response objects
# set logging level to DEBUG
import logging


config = {
  'ORIGINS': [
    'http://localhost:4200',  # Angular
    'http://127.0.0.1:4200',  # Angular
  ]
}


logging.getLogger('flask__VoiceAssistant').setLevel(logging.DEBUG)
app = Flask(__name__)
cors = CORS(app)
app.register_blueprint(auth_app)
app.register_blueprint(task_app)
app.register_blueprint(configure_app)
app.register_blueprint(intent_app)
app.register_blueprint(voice_app)
app.register_blueprint(conversation_app)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT"),
        debug=True if (os.environ.get("DEBUG") == 'on') else False
    )
