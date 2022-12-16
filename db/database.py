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
        self.__cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname varchar(50) NOT NULL,
            lastname varchar(50) NOT NULL,
            language varchar(7) NOT NULL,
            email varchar(100) NOT NULL UNIQUE,
            username varchar(50) NOT NULL UNIQUE,
            password varchar(128) NOT NULL);
            CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version varchar(50) NOT NULL UNIQUE);
            """
        )

    def seeder(self):
        try:
            self.__cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?)",
                (
                    "Firstname",
                    "Lastname",
                    "en",
                    "test@localpythoncms.local",
                    "test",
                    self.sha256("test"),
                ),
            )
            self.__cur.executescript(
                """
                INSERT INTO updates VALUES (null, "v0.00.0");
                """
            )
            self.__db_connection.commit()
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR")
            # print(traceback.print_exc())

    def getLanguage(self):
        self.__cur.execute("SELECT language FROM users")
        return self.__cur.fetchone()[0]

    def sha256(self, string):
        return hashlib.sha256(string.encode("utf-8"), usedforsecurity=True).hexdigest()

    def registerNewUser(self, email, username, password):
        try:
            print(email + " " + username + " " + password)
        except sqlite3.IntegrityError as e:
            print("INTEGRITY ERROR: " + e)

        """
        self.__cur.execute("SELECT 1 FROM users where username = %s", [x])
        if self.__cur.rowcount:
            print("Username already exists")
        else:
            print("Username doesn't exist")
        """

    def __del__(self):
        self.__db_connection.close()
