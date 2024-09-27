import os
import google.generativeai as genai
from textblob import TextBlob
import time
from dotenv import load_dotenv

class DC_chat ():

    def __init__(self, api_key, generation_config, model_name):
        genai.configure(api_key=api_key)
        self.generation_config=generation_config
        safety_settings={
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH":"BLOCK_NONE",
            "HARM_CATEGORY_HARASSMENT":"BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT":"BLOCK_NONE"
            }
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings = safety_settings
            # See https://ai.google.dev/gemini-api/docs/safety-settings
        )
        self.chat_session = self.model.start_chat()

def test():
    test_questions = [
        "How are you?",
        "Why is the sky blue?",
        "I feel sad today...",
        "Tell me a joke.",
        "Everything is awful.",
        "I'm happy with my work.",
        "Life is meaningless.",
        "I love my new car!",
        "I hate Mondays.",
        "It's a beautiful day!"
    ]

    api_key = api_key = os.getenv("gemini_API")
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
        }
    model_name="gemini-1.5-flash"
    for question in test_questions:
        print(f"Question - '{question}'")
        analysis = TextBlob(question)
        if analysis.sentiment.polarity >= 0:
            print ("This question is positive!", end='')
            sentiment = 'Positive'
        else:
            print ("This question is negative!", end='')
            sentiment = 'Negative'
        model_chat = DC_chat(api_key=api_key,generation_config=generation_config, model_name=model_name)
        chat = model_chat.chat_session
        if sentiment == 'Positive':
            mood_setting = "\tAnswer like Batman"
        else:
            mood_setting = "\tAnswer like Joker"
        print (mood_setting)
        response = chat.send_message(f"{mood_setting} and ask question back\n{question}")
        print (f"\t{response.text}")
        time.sleep(5)

def main(call):
    api_key = os.getenv("gemini_API")
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
        }
    model_name="gemini-1.5-flash"
    while True:
        analysis = TextBlob(call)
        if analysis.sentiment.polarity >= 0:
            sentiment = 'Positive'
            mood_setting = "Answer like Batman"
        else:
            sentiment = 'Negative'
            mood_setting = "Answer like Joker"
        model_chat = DC_chat(api_key=api_key,generation_config=generation_config, model_name=model_name)
        chat = model_chat.chat_session
        response = chat.send_message_async(f"{mood_setting} and ask question back\n{call}")
        time.sleep(5)
        yield response.text

if __name__=="__main__":
    load_dotenv()
    test()