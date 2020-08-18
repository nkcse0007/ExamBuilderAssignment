import json


# Responses for Actions On Google
class GoogleResponse():

    def __init__(self):
        pass

    def statement(self):
        return {
            'fulfillmentText': 'This is a response from webhook.',
            "simpleResponse": {
                "textToSpeech": 'hellllllllllllllllllllllllllllll'
            }
        }

    def question(self):
        return {
            'fulfillmentText': 'This is a response from webhook.',
            "simpleResponse": {
                "textToSpeech": 'hellllllllllllllllllllllllllllll'
            }
        }

    def base_cmp(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": False,
                    "richResponse": {
                        "items": [

                        ]
                    }
                }
            }
        }

    def button(self, value, buttons):
        buttons_data = [{"title": button} for button in buttons]

        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": value
                                }
                            }
                        ],
                        "suggestions": buttons_data
                    }
                }
            }
        }

    def basic_card(self):
        return {
            "basicCard": {
                "title": "Card Title",
                "image": {
                    "url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                    "accessibilityText": "Google Logo"
                },
                "buttons": [
                    {
                        "title": "Button Title",
                        "openUrlAction": {
                            "url": "https://www.google.com"
                        }
                    }
                ],
                "imageDisplayOptions": "WHITE"
            }
        }


    def browse_carousel(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "carouselBrowse": {
                                    "items": [
                                        {
                                            "title": "Title of item 1",
                                            "openUrlAction": {
                                                "url": "https://google.com"
                                            },
                                            "description": "Description of item 1",
                                            "footer": "Item 1 footer",
                                            "image": {
                                                "url": "https://developers.google.com/actions/assistant.png",
                                                "accessibilityText": "Google Assistant Bubbles"
                                            }
                                        },
                                        {
                                            "title": "Title of item 2",
                                            "openUrlAction": {
                                                "url": "https://google.com"
                                            },
                                            "description": "Description of item 2",
                                            "footer": "Item 2 footer",
                                            "image": {
                                                "url": "https://developers.google.com/actions/assistant.png",
                                                "accessibilityText": "Google Assistant Bubbles"
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    },
                    "userStorage": "{\"data\":{}}"
                }
            },
            "outputContexts": [
                {
                    "name": "projects/temperatureconvertersample/agent/sessions/518488a5-09f6-4a36-8950-942f595b70b8/contexts/_actions_on_google",
                    "lifespanCount": 99,
                    "parameters": {
                        "data": "{}"
                    }
                }
            ]
        }


    def carousel_response(self):
        return {
            "systemIntent": {
                "intent": "actions.intent.OPTION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                    "carouselSelect": {
                        "items": [
                            {
                                "optionInfo": {
                                    "key": "first title"
                                },
                                "description": "first description",
                                "image": {
                                    "url": "https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png",
                                    "accessibilityText": "first alt"
                                },
                                "title": "first title"
                            },
                            {
                                "optionInfo": {
                                    "key": "second"
                                },
                                "description": "second description",
                                "image": {
                                    "url": "https://lh3.googleusercontent.com/Nu3a6F80WfixUqf_ec_vgXy_c0-0r4VLJRXjVFF_X_CIilEu8B9fT35qyTEj_PEsKw",
                                    "accessibilityText": "second alt"
                                },
                                "title": "second title"
                            }
                        ]
                    }
                }
            }
        }


    def list(self):
        return {
            "systemIntent": {
                "intent": "actions.intent.OPTION",
                "data": {
                    "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                    "listSelect": {
                        "title": "Hello",
                        "items": [
                            {
                                "optionInfo": {
                                    "key": "first title key"
                                },
                                "description": "first description",
                                "image": {
                                    "url": "https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png",
                                    "accessibilityText": "first alt"
                                },
                                "title": "first title"
                            },
                            {
                                "optionInfo": {
                                    "key": "second"
                                },
                                "description": "second description",
                                "image": {
                                    "url": "https://lh3.googleusercontent.com/Nu3a6F80WfixUqf_ec_vgXy_c0-0r4VLJRXjVFF_X_CIilEu8B9fT35qyTEj_PEsKw",
                                    "accessibilityText": "second alt"
                                },
                                "title": "second title"
                            }
                        ]
                    }
                }
            }
        }


    def simple(self, value):
        return {
            "simpleResponse": {
                "textToSpeech": ' '+value
            }
        }


    def simple_sml(self):
        return {
            "simpleResponse": {
                "ssml": "<speak>Here are <say-as interpret-as=\"characters\">SSML</say-as> samples. I can pause <break time=\"3\" />. I can play a sound <audio src=\"https://actions.google.com/sounds/v1/alarms/winding_alarm_clock.ogg\">your wave file</audio>. I can speak in cardinals. Your position is <say-as interpret-as=\"cardinal\">10</say-as> in line. Or I can speak in ordinals. You are <say-as interpret-as=\"ordinal\">10</say-as> in line. Or I can even speak in digits. Your position in line is <say-as interpret-as=\"digits\">10</say-as>. I can also substitute phrases, like the <sub alias=\"World Wide Web Consortium\">W3C</sub>. Finally, I can speak a paragraph with two sentences. <p><s>This is sentence one.</s><s>This is sentence two.</s></p></speak>",
                "displayText": "This is a SSML sample. Make sure your sound is enabled to hear the demo"
            }
        }


    def simple_tts(self, value):
        return {
            "simpleResponse": {
                "textToSpeech": value,
                "displayText": value
            }
        }


    def suggestion(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Howdy! I can tell you fun facts about almost any number."
                                }
                            },
                            {
                                "simpleResponse": {
                                    "textToSpeech": "What number do you have in mind?"
                                }
                            }
                        ],
                        "suggestions": [
                            {
                                "title": "25"
                            },
                            {
                                "title": "45"
                            },
                            {
                                "title": "Never mind"
                            }
                        ],
                        "linkOutSuggestion": {
                            "destinationName": "Website",
                            "url": "https://assistant.google.com"
                        }
                    }
                }
            }
        }


    def ask_for_confirmation(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "systemIntent": {
                        "intent": "actions.intent.CONFIRMATION",
                        "data": {
                            "@type": "type.googleapis.com/google.actions.v2.ConfirmationValueSpec",
                            "dialogSpec": {
                                "requestConfirmationText": "Please confirm your order."
                            }
                        }
                    }
                }
            }
        }


    def date_time(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "systemIntent": {
                        "intent": "actions.intent.DATETIME",
                        "data": {
                            "@type": "type.googleapis.com/google.actions.v2.DateTimeValueSpec",
                            "dialogSpec": {
                                "requestDatetimeText": "When do you want to come in?",
                                "requestDateText": "What is the best date to schedule your appointment?",
                                "requestTimeText": "What time of day works best for you?"
                            }
                        }
                    }
                }
            }
        }


    def ask_for_delivery_address(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "systemIntent": {
                        "intent": "actions.intent.DELIVERY_ADDRESS",
                        "data": {}
                    }
                }
            }
        }


    def ask_for_permission(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "systemIntent": {
                        "intent": "actions.intent.PERMISSION",
                        "data": {
                            "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                            "optContext": "To deliver your order",
                            "permissions": [
                                "NAME",
                                "DEVICE_PRECISE_LOCATION"
                            ]
                        }
                    }
                }
            }
        }


    def ask_for_signin(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "systemIntent": {
                        "intent": "actions.intent.SIGN_IN",
                        "data": {}
                    }
                }
            }
        }


    def end_conversation(self):
        return {
            "payload": {
                "google": {
                    "expectUserResponse": False,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "Goodbye!"
                                }
                            }
                        ]
                    }
                }
            }
        }


    def no_input(self):
        return {
            "payload": {
                "google": {
                    "noInputPrompts": [
                        {
                            "textToSpeech": "I didn't hear you. Can you say your name?",
                            "displayText": "I did not hear you. Can you say your name?"
                        },
                        {
                            "ssml": "<speak>I didn't get that.  What is your name?</speak>",
                            "displayText": "I did not get that.  What is your name?"
                        },
                        {
                            "textToSpeech": "I seem to be having trouble. Please try again later.",
                            "displayText": "I seem to be having trouble. Please try again later."
                        }
                    ],
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "textToSpeech": "What's your name?"
                                }
                            }
                        ]
                    }
                }
            }
        }
