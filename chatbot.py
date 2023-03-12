import sys
import openai

import chatModel as cm


def proc_stop(bot, update):
    chatBot.stop()


def clear_message(bot, update):
    chatBot.clear_message()


chatBot = cm.ChatBot()
chatBot.add_handler("stop", proc_stop)
chatBot.add_handler("clear", clear_message)
chatBot.start()
