import sqlite3
import sys


class Actions(object):

    __DB_LOCATION = "localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()

    def registerNewUser(self, firstname, lastname, email, username, password):
        print(
            firstname + " " + lastname + " " + email + " " + username + " " + password
        )

    def __del__(self):
        self.__db_connection.close()
