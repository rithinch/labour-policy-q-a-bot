import telebot
from dotenv import load_dotenv
import os
import requests


# TODO remove
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("You must set the TELEGRAM_TOKEN environment variable")


bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("Bot started...")


def fetch_llm_response(user_query, chat_id):
    endpoint = "https://labour-bot-qa-bot-demo-backend-ea4dxgw4wdljq.azurewebsites.net/api/GetConversationResponse?code=ilj42vb2smklgc19d3d7a-9c02-4490-a80b-682f0dd19aa5&clientId=clientKey"
    body = {
        "messages": [
            {
                "role": "system",
                "content": "Answer briefly and precisely. If you do not know the information, answer: I am sorry, I do not know the answer to the question",
            },
            {"role": "user", "content": user_query},
        ],
        "conversation_id": chat_id,
    }
    try:
        response = requests.post(endpoint, json=body)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)
    except Exception as e:
        print("Error fetching response", e)


def stream_response(message):
    pass


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def reverse_message(message):
    print(message.text)
    llm_res = fetch_llm_response(message.text, str(message.chat.id))
    if llm_res is None:
        return
    bot_message = llm_res["choices"][0]["messages"][1]["content"]
    print(bot_message)
    reversed = message.text[::-1]

    bot.send_message(message.chat.id, bot_message)


@bot.message_handler(commands=["help"])
def provide_help():
    pass


bot.polling()
