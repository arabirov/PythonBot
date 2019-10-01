import telebot
import os
import pathlib
import random
import logging

from py import my_fibonacci
from py.argument import *
from py.poi_messages import *

from telebot import apihelper

try:
    apihelper.proxy = constants.PROXY
except AttributeError:
    pass
bot = telebot.TeleBot(constants.KEY)  # ALWAYS REMEMBER TO ADD KEY MANUALLY
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    else:
        bot.send_message(message.chat.it, r"Sorry, out of images ¯\_(ツ)_/¯")


@bot.message_handler(commands=['fibo'], content_types=['text'])
def fibo_message(message):
    argument = extract_arg(message)
    if int(argument) > 0:
        bot.send_message(message.chat.id, f"Hi! You sent me /fibo. For your number {int(argument)}"
                                          f" sequence will be : {my_fibonacci.fibonacci(int(argument))} ")
    else:
        bot.send_message(message.chat.id, f"{my_fibonacci.fibonacci(int(argument))}")


@bot.message_handler(commands=["wwg"])
def wwg_message(message):
    poi_message = poi_id_message(extract_arg(message))
    try:
        bot.send_photo(message.chat.id, poi_message[1], caption=poi_message[0], parse_mode="HTML")
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, poi_message)


# -------------------------- M E S S A G E S --------------------------
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text.lower() == "hi":
        bot.send_message(message.chat.id, "Hello!")
    elif message.text.lower() == "bye":
        bot.send_message(message.chat.id, "Goodbye!")
    else:
        bot.send_message(message.chat.id, "I don't know what does it mean :( Please use 'Hi'/'Bye' or /start")


try:
    bot.polling()
finally:
    logging.info("Bot stopped.")
