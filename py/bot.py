import telebot
import os
import pathlib
import random
import logging
import re

import bot_key
import my_fibonacci

bot = telebot.TeleBot(bot_key.KEY)  # ALWAYS REMEMBER TO ADD KEY MANUALLY
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fibo_regexp = re.compile(r"^\d+$")

# -------------------------- C O M M A N D S --------------------------
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hi! You sent me /start.")


@bot.message_handler(commands=['secret'])
def secret_message(message):
    if pathlib.Path("../images/").exists():
        file = (os.path.join("../images", random.choice(os.listdir("../images"))))
        image = open(file, 'rb')
        bot.send_photo(chat_id=message.chat.id, photo=image, caption="Here it is ( ͡° ͜ʖ ͡°)")
        image.close()
        logging.info("He-he ( ͡° ͜ʖ ͡°)")


@bot.message_handler(commands=['fibo'], content_types=['text'], regexp="^\d*$")
def fibo_message(message):
    if extract_arg(message) > 0:
        bot.send_message(message.chat.id, f"Hi! You sent me /fibo. For your number {extract_arg(message)}"
                                          f" sequence will be : {my_fibonacci.fibonacci(extract_arg(message))} ")
    else:
        bot.send_message(message.chat.id, f"{my_fibonacci.fibonacci(extract_arg(message))}")


def extract_arg(message):  # ----- S H I T C 0 D E -----
    argument = message.text.partition('/fibo ')
    if argument[2].lstrip('-').isdigit():
        if int(argument[2]) > 0:
            return int(argument[2])
        else:
            return 0
    else:
        return 0


# -------------------------- M E S S A G E S --------------------------
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text.lower() == "hi":
        bot.send_message(message.chat.id, "Hello!")
    elif message.text.lower() == "bye":
        bot.send_message(message.chat.id, "Goodbye!")
    else:
        bot.send_message(message.chat.id, "I don't know what does it mean :( Please use 'Hi'/'Bye' or /start")


bot.polling()
