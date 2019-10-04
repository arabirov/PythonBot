from telebot import apihelper

from py.constants import PROXY


def connect():
    try:
        apihelper.proxy = PROXY
    except Exception:
        pass
