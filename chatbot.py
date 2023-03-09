import sys
import openai
from configparser import ConfigParser

import chatModel as cm

config = ConfigParser()
config.read("config.ini")


def proc_stop(bot, update):
    chatBot.sendMessage("Have a nice day!")
    chatBot.stop()


def get_chatGPT_response(bot, update):
    content = update.message.text
    openai.api_key = config["CHATGPT"]["API_KEY"]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    response = completion.choices[0].message


chatBot = cm.ChatBot()
chatBot.add_handler("stop", proc_stop)
chatBot.start()
