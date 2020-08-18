from uuid import uuid4
import os
from database import db
from src.CommonHelpers.com import change_file_name
from datetime import datetime, timedelta

FAQ_FILES_PATH = f"{os.environ.get('MEDIA_FOLDER')}/faq_files/"
TRAINED_FAQ_FILES_PATH = f"{os.environ.get('MEDIA_FOLDER')}/trained_faq_files"


class Files:
    def __init__(self, request, user_id):
        self.request = request
        self.bot_id = user_id

    def get(self):
        pass

    def post(self):

        if not self.request.files:
            return {'message': 'faq file is required', 'status': False}, 400
        faq_file = self.request.files['file']
        if faq_file.filename != '':
            file_name = change_file_name(faq_file.filename)
            faq_file.save(FAQ_FILES_PATH + file_name)
            data = {
                '_id': uuid4().hex,
                'user_id': self.user_id,
                    'file': file_name,
                    'created_on': datetime.now()}
            db['FaqFileUpload'].insert_one(data)
            return {'message': 'file saved successfully', 'status': True}, 200
        else:
            return {'message': 'faq file is required', 'status': False}, 400

    def put(self):
        pass

    def delete(self):
        pass
