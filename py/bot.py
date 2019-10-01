import telebot
import os
import pathlib
import random
import logging

from py import my_fibonacci
from py.argument import *
from py.poi_messages import *

from telebot import apihelper, types

try:
    apihelper.proxy = constants.PROXY
except AttributeError:
    pass
bot = telebot.TeleBot(constants.KEY)  # ALWAYS REMEMBER TO ADD KEY MANUALLY
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class User:
    user_dict = {}

    def __init__(self, name):
        self.name = name
        self.age = None

# -------------------------- C O M M A N D S --------------------------
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hi! You sent me /start. Send /help if you want more info")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, "List of commands:\n<b>/start</b> - basic command\n<b>/fibo</b> - sends with "
                                      "numeric argument to retrieve fibonacci sequence\n<b>/wwg</b> - sends with "
                                      "numeric to retrieve POI info",
                     parse_mode="HTML")


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


@bot.message_handler(commands=['wwg'])
def wwg_message(message):
    poi_message = poi_id_message(extract_arg(message))
    try:
        bot.send_photo(message.chat.id, poi_message[1], caption=poi_message[0], parse_mode="HTML")
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, poi_message)


@bot.message_handler(commands=['whoami'])
def whoami(message):
    msg = bot.reply_to(message, "Well, hi there. What is your name?")
    bot.register_next_step_handler(msg, whoami_name)


def whoami_name(message):
    chat_id = message.chat.id
    msg = bot.reply_to(message, "How old are you?")
    name = message.text
    user = User(name)
    User.user_dict[chat_id] = user
    bot.register_next_step_handler(msg, whoami_age)


def whoami_age(message):
    chat_id = message.chat.id
    age = message.text
    if not age.isdigit():
        msg = bot.reply_to(message, "Age should be a number,")
        bot.register_next_step_handler(msg, whoami_age)
        return
    user = User.user_dict[chat_id]
    user.age = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Yes, please", "No, thanks")
    msg = bot.reply_to(message, f"Nice to meet you, {user.name}, that {str(user.age)} years old. Should I remember that?", reply_markup=markup)
    bot.register_next_step_handler(msg, whoami_save)


def whoami_save(message):
    chat_id = message.chat.id
    answer = message.text
    if answer == 'Yes, please':
        bot.send_message(chat_id, "Saved")
    elif answer == 'No, thanks':
        bot.send_message(chat_id, "Ok, bye")
    else:
        msg = bot.reply_to(message, "Please, use buttons")
        bot.register_next_step_handler(msg, whoami_save)

# -------------------------- M E S S A G E S --------------------------
@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.text.lower() == "hi":
        bot.send_message(message.chat.id, "Hello!")
    elif message.text.lower() == "bye":
        bot.send_message(message.chat.id, "Goodbye!")
    else:
        bot.send_message(message.chat.id, "I don't know what does it mean :( Please use 'Hi'/'Bye' or /start")


bot.enable_save_next_step_handlers(delay=2)
try:
    bot.polling()
finally:
    logging.info("Bot stopped.")
