from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from src.ExamBuilder.index import exam_app

env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

app = Flask(__name__)
app.register_blueprint(exam_app)

if __name__ == "__main__":
    app.run(
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT"),
        debug=True if (os.environ.get("DEBUG") == 'on') else False
    )
