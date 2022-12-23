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
            self.__cur.execute("SELECT 1 FROM users where email = ?", [email])
            data = self.__cur.fetchall()
            if len(data) == 0:
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
                return True
            else:
                return False

        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR: " + e)

    def __del__(self):
        self.__db_connection.close()
