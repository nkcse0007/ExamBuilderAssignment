from deeppavlov import build_model, configs, train_model
from database import db
from deeppavlov.core.common.file import read_json
import os

ROOT_PATH = os.path.dirname(os.path.abspath('app.py'))
FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}/faq_files/"
TRAINED_FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}"
DOWNLOAD_FAQ_FILES_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}/downloads"


def train_faq(user_id):
    record = db['FaqFileUpload'].find_one({'user_id': user_id})
    config_file =  read_json(f'{ROOT_PATH}/src/Faqs/config_faq.json')
    config_file['dataset_reader']['data_path'] = FAQ_FILES_PATH+record['file']
    config_file['metadata']['variables']['ROOT_PATH'] = ROOT_PATH
    model = train_model(config_file, download=True)

    return {'message': 'successfully trained', 'status': True}, 200

