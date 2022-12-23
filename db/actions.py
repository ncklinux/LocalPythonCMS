import sqlite3
import sys
from common.functions import Functions


class Actions(object):

    __DB_LOCATION = "assets/sqlite/localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()

    def registerNewUser(self, firstname, lastname, email, username, password):
        try:
            commonFun = Functions()
            self.__cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?)",
                (
                    firstname,
                    lastname,
                    "en",
                    email,
                    username,
                    commonFun.sha256(password),
                ),
            )
            self.__db_connection.commit()
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR: " + e)

    def __del__(self):
        self.__db_connection.close()
