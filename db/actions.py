import sqlite3
import sys
from common.functions import Functions
from common.logger_factory import LoggerFactory


class Actions(object):

    __DB_LOCATION = "assets/sqlite/localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()
        self.logger = LoggerFactory.CreateLogger(__name__)

    def register_new_user(
        self, firstname, lastname, email, username, password, language
    ):
        try:
            self.__cur.execute("SELECT 1 FROM users where email = ?", [email])
            data = self.__cur.fetchall()
            if len(data) == 0:
                common_functions = Functions()
                self.__cur.execute(
                    "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?)",
                    (
                        firstname,
                        lastname,
                        language,
                        email,
                        username,
                        common_functions.sha256(password),
                    ),
                )
                self.__db_connection.commit()
                return True
            else:
                return False

        except sqlite3.IntegrityError as e:
            self.logger.error("INTEGRITY ERROR")

    def login_user(self, email, password):
        try:
            self.__cur.execute("SELECT 1 FROM users where email = ?", [email])
            data = self.__cur.fetchall()
            if len(data) == 1:
                common_functions = Functions()
                self.__cur.execute(
                    "SELECT * FROM users WHERE email = ? AND password = ?",
                    (
                        email,
                        common_functions.sha256(password),
                    ),
                )
                self.__db_connection.commit()
                if self.__cur.fetchall():
                    return True
                else:
                    return False
            else:
                return False
        except sqlite3.IntegrityError as e:
            self.logger.error("INTEGRITY ERROR")

    def __del__(self):
        self.__db_connection.close()
