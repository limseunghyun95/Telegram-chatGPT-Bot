# 봇의 토근이나 초기화 관련된 코드
import openai
import telegram as tel
from configparser import ConfigParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

config = ConfigParser()
config.read("config/config.ini")


class TelegramBot:

    def __init__(self, name, token):
        self.core = tel.Bot(token)
        self.updater = Updater(token, use_context=True)
        self.name = name

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()


class ChatBot(TelegramBot):

    def __init__(self):
        self.token = config["TELEGRAM"]["ACCESS_TOKEN"]
        TelegramBot.__init__(self, "chatGPT", self.token)
        self.message = []

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def chatGPT(self, update, context):
        user_text = update.message.text
        openai.api_key = config["CHATGPT"]["API_KEY"]

        if user_text:
            self.message.append(
                {
                    "role": "user",
                    "content": user_text
                }
            )
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.message
            )
            self.message.append(completion.choices[0].message)
            response = completion.choices[0].message["content"]

            context.bot.send_message(
                chat_id=update.effective_chat.id, text=response)

    def clear_message(self):
        self.message = []

    def start(self):
        GPT_hander = MessageHandler(
            Filters.text & (~Filters.command), self.chatGPT)
        self.updater.dispatcher.add_handler(GPT_hander)
        self.updater.start_polling()
        self.updater.idle()
