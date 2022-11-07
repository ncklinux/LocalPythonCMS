import sqlite3
import sys, traceback


class Database(object):

    __DB_LOCATION = "localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.cur = self.__db_connection.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname varchar(50) NOT NULL,
            lastname varchar(50) NOT NULL,
            email varchar(100) NOT NULL UNIQUE,
            username varchar(50) NOT NULL UNIQUE,
            password varchar(128) NOT NULL)"""
        )

        try:
            self.cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?)",
                (
                    "test_firstname",
                    "test_lastname",
                    "test@localpythoncms.local",
                    "test",
                    "123User.",
                ),
            )
            self.__db_connection.commit()
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR")
            # print(traceback.print_exc())

    def __del__(self):
        self.__db_connection.close()
