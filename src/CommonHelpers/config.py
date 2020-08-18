
def intent_config(intent_path):
    return {
        "dataset_reader": {
            "class_name": "basic_classification_reader",
            "x": "text",
            "y": "intents",
            "data_path": f"{intent_path}/"
        },
        "dataset_iterator": {
            "class_name": "basic_classification_iterator",
            "seed": 42,
            "split_seed": 23,
            "field_to_split": "train",
            "split_fields": [
                "train",
                "valid"
            ],
            "split_proportions": [
                0.9,
                0.1
            ]
        },
        "chainer": {
            "in": [
                "x"
            ],
            "in_y": [
                "y"
            ],
            "pipe": [
                {
                    "id": "classes_vocab",
                    "class_name": "simple_vocab",
                    "fit_on": [
                        "y"
                    ],
                    "save_path": f"{intent_path}/classes.dict",
                    "load_path": f"{intent_path}/classes.dict",
                    "in": "y",
                    "out": "y_ids"
                },
                {
                    "in": [
                        "x"
                    ],
                    "out": [
                        "x_vec"
                    ],
                    "fit_on": [
                        "x",
                        "y_ids"
                    ],
                    "id": "tfidf_vec",
                    "class_name": "sklearn_component",
                    "save_path": f"{intent_path}/tfidf_v1.pkl",
                    "load_path": f"{intent_path}/tfidf_v1.pkl",
                    "model_class": "sklearn.feature_extraction.text:TfidfVectorizer",
                    "infer_method": "transform"
                },
                {
                    "in": "x",
                    "out": "x_tok",
                    "id": "my_tokenizer",
                    "class_name": "nltk_moses_tokenizer",
                    "tokenizer": "wordpunct_tokenize"
                },
                {
                    "in": [
                        "x_vec"
                    ],
                    "out": [
                        "y_pred"
                    ],
                    "fit_on": [
                        "x_vec",
                        "y"
                    ],

                    "class_name": "sklearn_component",
                    "main": True,
                    "save_path": f"{intent_path}/logreg_v2.pkl",
                    "load_path": f"{intent_path}/logreg_v2.pkl",
                    "model_class": "sklearn.linear_model:LogisticRegression",
                    "infer_method": "predict",
                    "ensure_list_output": True
                },

            ],
            "out": [
                "y_pred"
            ]
        },
        "train": {
            "batch_size": 64,
            "metrics": [
                "accuracy"
            ],
            "validate_best": True,
            "test_best": True
        }
    }


def faq_config():
    return {
        "dataset_reader": {
            "class_name": "faq_reader",
            "x_col_name": "Question",
            "y_col_name": "Answer",
            "data_path": ""
        },
        "dataset_iterator": {
            "class_name": "data_learning_iterator"
        },
        "chainer": {
            "in": "q",
            "in_y": "y",
            "pipe": [
                {
                    "class_name": "stream_spacy_tokenizer",
                    "in": "q",
                    "id": "my_tokenizer",
                    "lemmas": True,
                    "out": "q_token_lemmas"
                },
                {
                    "ref": "my_tokenizer",
                    "in": "q_token_lemmas",
                    "out": "q_lem"
                },
                {
                    "in": [
                        "q_lem"
                    ],
                    "out": [
                        "q_vect"
                    ],
                    "fit_on": [
                        "q_lem"
                    ],
                    "id": "tfidf_vec",
                    "class_name": "sklearn_component",
                    "save_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/tfidf.pkl",
                    "load_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/tfidf.pkl",
                    "model_class": "sklearn.feature_extraction.text:TfidfVectorizer",
                    "infer_method": "transform"
                },
                {
                    "id": "answers_vocab",
                    "class_name": "simple_vocab",
                    "fit_on": [
                        "y"
                    ],
                    "save_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/en_mipt_answers.dict",
                    "load_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/en_mipt_answers.dict",
                    "in": "y",
                    "out": "y_ids"
                },
                {
                    "in": "q_vect",
                    "fit_on": [
                        "q_vect",
                        "y_ids"
                    ],
                    "out": [
                        "y_pred_proba"
                    ],
                    "class_name": "sklearn_component",
                    "main": True,
                    "save_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/logreg.pkl",
                    "load_path": "{MODELS_PATH}/faq/mipt/en_mipt_faq_v4/logreg.pkl",
                    "model_class": "sklearn.linear_model:LogisticRegression",
                    "infer_method": "predict_proba",
                    "C": 1000,
                    "penalty": "l2"
                },
                {
                    "in": "y_pred_proba",
                    "out": "y_pred_ids",
                    "class_name": "proba2labels",
                    "max_proba": True
                },
                {
                    "in": "y_pred_ids",
                    "out": "y_pred_answers",
                    "ref": "answers_vocab"
                }
            ],
            "out": [
                "y_pred_answers",
                "y_pred_proba"
            ]
        },
        "train": {
            "evaluation_targets": [],
            "class_name": "fit_trainer"
        },
        "metadata": {
            "variables": {
                "ROOT_PATH": "",
                "DOWNLOADS_PATH": "",
                "MODELS_PATH": ""
            },
            "requirements": [
                "{DEEPPAVLOV_PATH}/requirements/spacy.txt",
                "{DEEPPAVLOV_PATH}/requirements/en_core_web_sm.txt"
            ]
        }
    }
