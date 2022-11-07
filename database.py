import sqlite3
import sys, traceback
import hashlib


class Database(object):

    __DB_LOCATION = "localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()
        self.createTable()
        self.seeder()

    def createTable(self):
        self.__cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname varchar(50) NOT NULL,
            lastname varchar(50) NOT NULL,
            email varchar(100) NOT NULL UNIQUE,
            username varchar(50) NOT NULL UNIQUE,
            password varchar(128) NOT NULL)"""
        )

    def seeder(self):
        try:
            self.__cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?)",
                (
                    "test_firstname",
                    "test_lastname",
                    "test@localpythoncms.local",
                    "test",
                    self.sha256("123User."),
                ),
            )
            self.__db_connection.commit()
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR")
            # print(traceback.print_exc())

    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def __del__(self):
        self.__db_connection.close()
