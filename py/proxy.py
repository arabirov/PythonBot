import logging

from telebot import apihelper

from py.constants import PROXY


def connect():
    try:
        apihelper.proxy = PROXY
        logging.info("Connected to proxy!")
    except AttributeError:
        logging.info("Not connected to proxy!")
        pass
