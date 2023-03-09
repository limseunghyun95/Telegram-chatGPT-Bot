# 봇의 토근이나 초기화 관련된 코드
import json
import openai
import requests
import telegram as tel
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

config = ConfigParser()
config.read("config.ini")


class TelegramBot:

    def __init__(self, name, token):
        self.core = tel.Bot(token)
        self.updater = Updater(token, use_context=True)
        self.id = self.find_chat_id(token)
        self.name = name

    def find_chat_id(self, token):
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        res = requests.get(url)
        res = json.loads(res.text)

        return res["result"][0]["message"]["chat"]["id"]

    def sendMessage(self, text):
        self.core.sendMessage(chat_id=self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()


class ChatBot(TelegramBot):

    def __init__(self):
        self.token = config["TELEGRAM"]["ACCESS_TOKEN"] # Telegram Access Token
        TelegramBot.__init__(self, "chatGPT", self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def chatGPT(self, update, context):
        user_text = update.message.text
        openai.api_key = config["CHATGPT"]["API_KEY"] # ChatGPT API Key
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )
        response = completion.choices[0].message["content"]
        self.sendMessage(response)

    def start(self):
        self.sendMessage("안녕하세요. OpenAI의 ChatGPT 기반 봇입니다.")
        GPT_hander = MessageHandler(Filters.text & (~Filters.command), self.chatGPT)
        self.updater.dispatcher.add_handler(GPT_hander)
        self.updater.start_polling()
        self.updater.idle()
