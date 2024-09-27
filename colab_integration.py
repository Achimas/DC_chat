import ipywidgets as widgets
from IPython.display import display
import os
import google.generativeai as genai
from textblob import TextBlob
import time

class DC_chat ():
    def __init__(self, api_key, generation_config, model_name, history):
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
        self.chat_session = self.model.start_chat(history=history)

def chat(call):
    api_key = "AIzaSyCawI5BbNLfJkD9bytR1Md8oniEw0aMj4Q"
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
        }
    model_name="gemini-1.5-flash"
    while True:
        response = _analyse_and_answer(call, api_key=api_key,generation_config=generation_config, model_name=model_name)
        yield response.text

def test_chat(call):
    api_key = "AIzaSyCawI5BbNLfJkD9bytR1Md8oniEw0aMj4Q"
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 100,
        "response_mime_type": "text/plain",
        }
    model_name="gemini-1.5-flash"
    return _analyse_and_answer(call, api_key=api_key,generation_config=generation_config, model_name=model_name)

def _analyse_and_answer(call, api_key=None,generation_config=None, model_name=None):
    analysis = TextBlob(call)
    if analysis.sentiment.polarity >= 0:
        sentiment = 'Positive'
        mood_setting = "Answer like Batman"
    else:
        sentiment = 'Negative'
        mood_setting = "Answer like Joker"
    model_chat = DC_chat(api_key=api_key,generation_config=generation_config, model_name=model_name, history=history)
    chat = model_chat.chat_session
    prompt = f"{mood_setting} and ask question back\n{call}"
    response = chat.send_message(prompt)
    print (history)
    history.append({
        "role": "user", "parts": [{"text":prompt}]
        })
    history.append({
        "role": "model", "parts": [{"text":response.text}]
        })
    time.sleep(5)
    return response


# Ваш код для генерации ответа
def generate_response(user_input):
    response = chat(user_input)
    return f"{next(response)}"

def main():
    # Создаем поле для ввода запроса пользователя
    user_input_widget = widgets.Text(
        value='',
        placeholder='Введите ваш запрос',
        description='',
        disabled=False
    )

    # Кнопка для генерации ответа
    generate_button = widgets.Button(description="Сгенерировать ответ")

    # Текстовое поле для отображения ответа
    response_output = widgets.Output()

    # Функция для обработки нажатия кнопки
    def on_generate_button_clicked(b):
        # Получаем текст из виджета ввода
        user_input = user_input_widget.value
        
        # Генерируем ответ
        response = generate_response(user_input)
        
        # Отображаем ответ
        with response_output:
            print (f'""{user_input}""')
            # response_output.clear_output()  # очищаем старый вывод
            print(f"{response}")

    # Привязываем функцию к кнопке
    generate_button.on_click(on_generate_button_clicked)

    # Отображаем виджеты
    display(user_input_widget, generate_button, response_output)

if __name__ == "__main__":
    history = []
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
    for question in test_questions:
        response = test_chat(question)
        print ('""', question, '""')
        print (response.text)
    history = []
    main()