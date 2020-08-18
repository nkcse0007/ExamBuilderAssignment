from deeppavlov import build_model, configs, train_model
from database import db
from deeppavlov.core.common.file import read_json
import os
import json

ROOT_PATH = os.path.dirname(os.path.abspath('app.py'))
FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}/faq_files/"
TRAINED_FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}"
DOWNLOAD_FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}/downloads"


class TestFaq:
    def __init__(self, request, bot_id):
        self.user_id = user_id
        self.input_data = json.loads(request.data)

    def post(self):
        if 'question' not in self.input_data:
            return {'message': 'question is required', 'status': False}, 400
        record = db['FaqFileUpload'].find_one({'user_id': self.user_id})
        config_file = read_json(f'{ROOT_PATH}/src/Faqs/config_faq.json')
        config_file['dataset_reader']['data_path'] = FAQ_FILES_PATH + record['file']
        config_file['metadata']['variables']['ROOT_PATH'] = ROOT_PATH
        model = build_model(config_file, download=True)
        answer = model([self.input_data['question']])[0]
        return {'data': answer, 'status': True}, 200
