
from deeppavlov import train_model
from src.CommonHelpers.config import *
import os
from database import db
import pandas as pd
ROOT_PATH = os.path.dirname(os.path.abspath('app.py'))
MEDIA_PATH = f"{ROOT_PATH}/{os.environ.get('MEDIA_FOLDER')}"


def train_intents(user_id):
    config_file = intent_config(f"{MEDIA_PATH}/task_files/user_{user_id}")
    import pdb;
    pdb.set_trace()
    if not os.path.isdir(f"{MEDIA_PATH}/task_files/user_{user_id}"):
        os.mkdir(f"{MEDIA_PATH}/task_files/user_{user_id}")

    training_data = list()
    data = list(db['Task'].find({'_user': user_id},{'utterances.label': 1, '_id': 1}))
    for i in data:
        for j in i['utterances']:
            training_data.append({
                'text': j['label'],
                'intents': i['_id']
            })

    df = pd.DataFrame(training_data)
    df.to_csv(f"{MEDIA_PATH}/task_files/user_{user_id}/train.csv")
    try:
        import pdb;
        pdb.set_trace()
        model = train_model(config_file, download=True)
    except Exception as e:
        print(e)
        return {'message': 'error!' + str(e), 'data': {}, 'status': False}, 400
    return {'message': 'training done', 'data': {}, 'status': True}, 200
