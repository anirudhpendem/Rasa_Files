# # This files contains your custom actions which can be used to run
# # custom Python code.
# #
# # See this guide on how to implement these action:
# # https://rasa.com/docs/rasa/custom-actions


# # This is a simple example for a custom action which utters "Hello World!"

# # from typing import Any, Text, Dict, List
# #
# # from rasa_sdk import Action, Tracker
# # from rasa_sdk.executor import CollectingDispatcher
# #
# #
# # class ActionHelloWorld(Action):
# #
# #     def name(self) -> Text:
# #         return "action_hello_world"
# #
# #     def run(self, dispatcher: CollectingDispatcher,
# #             tracker: Tracker,
# #             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
# #
# #         dispatcher.utter_message(text="Hello World!")
# #
# #         return []


# import openai
# import json
# import time
# import pymysql
# from rasa_sdk import Action, Tracker
# from typing import Any, Text, Dict, List
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import SlotSet

# # OpenAI API Key
# openai.api_key = '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'

# # Chat session handling
# conversation = ["You are a helpful assistant."]
# sessions = {}

# def start_session(user_id):
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt="\n".join(conversation),
#         max_tokens=200,
#     )
#     return response['id']

# def send_user_message(session_id, message):
#     conversation.append("User: " + message)

#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt="\n".join(conversation),
#         max_tokens=200,
#         temperature=0.6,
#         n=1,
#         stop=None
#     )

#     assistant_reply = response.choices[0].text.strip()
#     conversation.append(assistant_reply)
#     return assistant_reply

# # Rasa custom action
# class OpenAiGpt(Action):
#     def name(self) -> Text:
#         return "open_ai_gpt"

#     def run(self, dispatcher: CollectingDispatcher, 
#             tracker: Tracker, 
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         if user_id not in sessions:
#             session_id = start_session(user_id)
#             sessions[user_id] = session_id
#         else:
#             session_id = sessions[user_id]

#         user_message = tracker.latest_message.get("text")
#         prompt = self.buildprompt(user_message)
#         assistant_reply = send_user_message(session_id, user_message)
#         # dispatcher.utter_message(text=assistant_reply)
#         chatgpt_response = assistant_reply
#         dispatcher.utter_message(text=chatgpt_response)

#         return []

#     @staticmethod
#     def buildprompt(user_message):
#         return (f" {user_message}")

# class ActionSessionId(Action):
#     def name(self) -> Text:
#         return "action_session_id"
#     def run(
#         self, dispatcher: CollectingDispatcher,
#         tracker: Tracker, 
#         domain: Dict[Text, Any]) -> List[Dict]:
        
#         session_id = user_id
#         # session_id = user_id
#         dispatcher.utter_message("The session id is {}".format(session_id))
#         return []
    
# class ActionImageCapture(Action):
#     def name(self) -> Text:
#         return "action_image_capture"
#     def run(
#         self, dispatcher: CollectingDispatcher,
#         tracker: Tracker, 
#         domain: Dict[Text, Any]) -> List[Dict]:
#         # user_message = tracker.latest_message.get("text")
#         # dispatcher.utter_message("Provide a image url")
#         current_state = tracker.current_state()
#         user_message = current_state["latest_message"]["text"]
#         prompt = self.buildprompt(user_message)
#         image_url = prompt
#         # description = self.describe_image(user_message)
#         # Example usage
#         description = None
#         # extracted_data = None
#         description = self.describe_image(image_url)
#         # print(description)
#         dispatcher.utter_message("Image Description:" + description)
#         # dispatcher.utter_message("Extracted Data:" + extracted_data)
#         return []
    
#     @staticmethod
#     def describe_image(image_url):
#         # Send message to the model
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant that describes images in detail."},
#                 {"role": "user", "content": image_url},
#             ],
#             max_tokens=200,  # Reduce prompt tokens to free up more space for image description
#         )
#         # Extract the model's reply
#         reply = response['choices'][0]['message']['content']
#         # Parse the reply to extract the image description
#         image_description = reply.split('\n')[0]
#         # Extract data if available
#         # data = None
#         # if len(reply.split('\n')) > 1:
#         #     data = json.loads(reply.split('\n')[1])
#         return image_description
    
#     @staticmethod
#     def buildprompt(user_message):
#         return (f" {user_message}")
# user_id = "anirudh"



# **************  ChatGPT ******************


import openai
import json
import time
from PIL import Image
import requests
from io import BytesIO
import pymysql
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

# OpenAI API Key
openai.api_key = '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'

# Chat session handling
conversation = ["You are a helpful assistant."]
sessions = {}

def start_session(user_id):
    response = openai.Completion.create(
        engine="text-babbage-001",
        prompt="\n".join(conversation),
        max_tokens=200,
    )
    return response['id']

def send_user_message(session_id, message):
    conversation.append("User: " + message)

    response = openai.Completion.create(
        engine="text-babbage-001",
        prompt="\n".join(conversation),
        max_tokens=200,
        temperature=0.6,
        n=1,
        stop=None
    )

    assistant_reply = response.choices[0].text.strip()
    conversation.append(assistant_reply)
    return assistant_reply

# Rasa custom action
class OpenAiGpt(Action):
    def name(self) -> Text:
        return "open_ai_gpt"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Database connectivity
        db = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            database="chatgpt"
        )
        cursor = db.cursor()

        # Get the user ID from tracker
        # user_id = tracker.sender_id
        # session_id = start_session(user_id)
        # Start session if it doesn't exist for the user ID
        if user_id not in sessions:
            session_id = start_session(user_id)
            sessions[user_id] = session_id
            # Insert the user ID into the database
            insert_query = "INSERT INTO user_ids (User_ID) VALUES (%s)"
            insert_values = (user_id,)
            cursor.execute(insert_query, insert_values)
            db.commit()

        else:
            session_id = sessions[user_id]

        user_message = tracker.latest_message.get("text")
        prompt = self.buildprompt(user_message)
        column1 = prompt
        assistant_reply = send_user_message(session_id, user_message)
        # dispatcher.utter_message(text=assistant_reply)
        chatgpt_response = assistant_reply

        query = "SELECT Response FROM responses WHERE Message = %s AND User_ID = %s"
        values = (column1,user_id)
        cursor.execute(query, values)
        result = cursor.fetchall()

        if len(result) > 0:
            column2 = result[0][0]
            # print(column2)
            dispatcher.utter_message(text=column2)
        else:
            # Insert the conversation into the database along with the user ID
            # insert_query = "INSERT INTO responses (Message, Response, User_ID) VALUES (%s, %s, %s)"
            # insert_values = (column1, chatgpt_response, user_id)
            # cursor.execute(insert_query, insert_values)
            # print("Conversation stored in the database.")
            dispatcher.utter_message(text=chatgpt_response)

        db.commit()
        cursor.close()
        db.close()

        return []

    @staticmethod
    def buildprompt(user_message):
        return (f" {user_message}")

class ActionSessionId(Action):
    def name(self) -> Text:
        return "action_session_id"
    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]) -> List[Dict]:
        
        session_id = user_id
        # session_id = user_id
        dispatcher.utter_message("The session id is {}".format(session_id))
        
        return []
    
    
# class ActionImageUrl(Action):
#     def name(self) -> Text:
#         return "action_image_url"
#     def run(
#         self, dispatcher: CollectingDispatcher,
#         tracker: Tracker, 
#         domain: Dict[Text, Any]) -> List[Dict]:

#         user_message = tracker.latest_message.get("text")
#         prompt = self.buildprompt(user_message)
#         response = openai.Image.create(
#         prompt=prompt,
#         n=1,
#         size="1024x1024"
#         )
#         image_url = response['data'][0]['url']

#         # # response = requests.get(image_url)
#         # # img = Image.open(BytesIO(response.content))
#         # im = Image.open(requests.get(image_url, stream=True).raw)
#         dispatcher.utter_message(image_url)

#         return []
    
#     @staticmethod
#     def buildprompt(user_message):
#         return (f" {user_message}")
    
    
class ActionImageCapture(Action):
    def name(self) -> Text:
        return "action_image_capture"
    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker, 
        domain: Dict[Text, Any]) -> List[Dict]:
        # user_message = tracker.latest_message.get("text")
        # dispatcher.utter_message("Provide a image url")
        current_state = tracker.current_state()
        user_message = current_state["latest_message"]["text"]
        prompt = self.buildprompt(user_message)
        image_url = prompt
        # description = self.describe_image(user_message)
        # Example usage
        description = None
        # extracted_data = None
        description = self.describe_image(image_url)
        # print(description)
        dispatcher.utter_message("Image Description:" + description)
        # dispatcher.utter_message("Extracted Data:" + extracted_data)
        return []
    
    @staticmethod
    def describe_image(image_url):
        # Send message to the model
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that describes images in detail."},
                {"role": "user", "content": image_url},
            ],
            max_tokens=100,  # Reduce prompt tokens to free up more space for image description
        )
        # Extract the model's reply
        reply = response['choices'][0]['message']['content']
        # Parse the reply to extract the image description
        image_description = reply.split('\n')[0]
        # Extract data if available
        # data = None
        # if len(reply.split('\n')) > 1:
        #     data = json.loads(reply.split('\n')[1])

        return image_description
    
    @staticmethod
    def buildprompt(user_message):
        return (f" {user_message}")

user_id = "entersoft_123"
