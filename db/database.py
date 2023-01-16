import sqlite3
import sys
import traceback
from common.functions import Functions
from common.logger_factory import LoggerFactory


class Database(object):

    __DB_LOCATION = "assets/sqlite/localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()
        self.logger = LoggerFactory.CreateLogger(__name__)
        self.create_table()
        self.seeder()

    def create_table(self):
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
        self.logger.info("Info database output")

    def seeder(self):
        try:
            common_functions = Functions()
            self.__cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?)",
                (
                    "Firstname",
                    "Lastname",
                    "us",
                    "test@localpythoncms.local",
                    "test",
                    common_functions.sha256("test"),
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

    def get_language(self):
        self.__cur.execute("SELECT language FROM users")
        return self.__cur.fetchone()[0]

    def __del__(self):
        self.__db_connection.close()
