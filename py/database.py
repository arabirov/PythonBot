import os
import pathlib
import logging
import sqlite3

from py.constants import DB_FOLDER, DB_PATH


class User:
    user_dict = {}

    def __init__(self, name):
        self.name = name
        self.age = None


class Database:
    db_cursor = ''
    db_conn = ''

    def create(self):
        if not pathlib.Path(DB_PATH).exists():
            if not pathlib.Path(DB_FOLDER).exists():
                os.mkdir(DB_FOLDER)
                logging.info("DB directory created.")
            try:
                logging.info("DB does not exist, creating...")
                self.db_conn = sqlite3.connect(DB_PATH)
                self.db_cursor = self.db_conn.cursor()
                logging.info("Creating tables...")
                self.db_conn.execute("""CREATE TABLE "users" (
        "chat_id"	INTEGER NOT NULL UNIQUE,
        "name"	TEXT NOT NULL,
        "age"	INTEGER)
        ;""")
                self.db_conn.commit()
                logging.info("Done!")
                self.db_cursor.close()
                self.db_conn.close()
            except sqlite3.OperationalError:
                logging.info("Can't create DB! Check your permissions and existence of ../db/ folder.")

    def connect(self):
        if pathlib.Path(DB_PATH).exists():
            logging.info("DB exists, trying to connect...")
            self.db_conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            logging.info("Connected!") if self.db_conn else logging.info("Error occurred while connecting to DB!")
            self.db_cursor = self.db_conn.cursor()
        else:
            logging.info("Can't connect to db.")

    def check_user(self, chat_id):
        try:
            check_acq = self.db_cursor.execute("SELECT * FROM users WHERE chat_id=?", (chat_id,)).fetchall()
        except NameError:
            return False, "Well, hi there. What is your name?"
        else:
            try:
                user_db_id = check_acq[0][0]
                user_db_name = check_acq[0][1]
                user_db_age = check_acq[0][2]
                if user_db_id == chat_id:
                    return True, f"Hey, I remember you! You are {user_db_name} that {user_db_age} years old."
            except IndexError:
                return False, "Well, hi there. What is your name?"

    def add_user(self, chat_id, name, age):
        try:
            user_insert = "INSERT INTO 'users' ('chat_id', 'name', 'age') VALUES (?, ?, ?);"
            user_data = (chat_id, name, age)
            self.db_cursor.execute(user_insert, user_data)
            self.db_conn.commit()
        except NameError:
            logging.info("Someone tried to save his information, but DB is down, sadly :(")
            pass

    def close_connection(self):
        try:
            self.db_cursor.close()
            self.db_conn.close()
            logging.info("Connection closed.")
        except NameError:
            logging.info("Can't close connection, because it does not exist.")
