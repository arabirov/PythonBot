import telebot
import os
import pathlib
import random
import logging

from telebot import types

from py.my_fibonacci import fibonacci
from py.argument import command_re, extract_arg
from py.poi_messages import poi_id_message
from py.database import Database, User
from py.constants import KEY
from py.proxy import connect as connect_to_proxy

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bot = telebot.TeleBot(KEY)  # ALWAYS REMEMBER TO ADD KEY MANUALLY
connect_to_proxy()
database = Database()

database.create()
database.connect()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hi! You sent me /start. Send /help if you want more info")


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, command_re)
    bot.send_message(message.chat.id, "List of commands:\n<b>/start</b> - basic command\n<b>/fibo</b> - sends with "
                                      "numeric argument to retrieve fibonacci sequence\n<b>/wwg</b> - sends with "
                                      "numeric to retrieve POI info\n<b>/whoami</b> - allows to add user to DB",
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
                                          f" sequence will be : {fibonacci(int(argument))} ")
    else:
        bot.send_message(message.chat.id, f"{fibonacci(int(argument))}")


@bot.message_handler(commands=['wwg'])
def wwg_message(message):
    poi_message = poi_id_message(extract_arg(message))
    try:
        bot.send_photo(message.chat.id, poi_message[1], caption=poi_message[0], parse_mode="HTML")
    except telebot.apihelper.ApiException:
        bot.send_message(message.chat.id, poi_message)


@bot.message_handler(commands=['whoami'])
def whoami(message):
    chat_id = message.chat.id
    user_check = database.check_user(chat_id)
    if user_check[0]:
        bot.reply_to(message, user_check[1])
    if not user_check[0]:
        msg = bot.reply_to(message, user_check[1])
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
    msg = bot.reply_to(message,
                       f"Nice to meet you, {user.name}, that {str(user.age)} years old. Should I remember that?",
                       reply_markup=markup)
    bot.register_next_step_handler(msg, whoami_save)


def whoami_save(message):
    chat_id = message.chat.id
    answer = message.text
    user = User.user_dict[chat_id]
    if answer == 'Yes, please':
        bot.send_message(chat_id, "Saved")
        database.add_user(chat_id, user.name, user.age)
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
    database.close_connection()
    logging.info("Bot stopped.")
