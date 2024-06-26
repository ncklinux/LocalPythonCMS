import sqlite3
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
                password varchar(128) NOT NULL,
                logged_in integer(1) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS manager (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar(50) NOT NULL UNIQUE,
                protocol integer(1),
                host varchar(50),
                port integer(5),
                encryption integer(1),
                type integer(1),
                user varchar(50),
                password varchar(128)
            );
            CREATE TABLE IF NOT EXISTS global_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version varchar(50) NOT NULL,
                language varchar(7) NOT NULL
            );
            INSERT INTO global_settings VALUES (null, "v0.00.0", "us");
            """
        )

    def seeder(self):
        try:
            common_functions = Functions()
            self.__cur.execute(
                "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "System",
                    "Admin",
                    "us",
                    "sys@localpythoncms.local",
                    "admin",
                    common_functions.sha256("admin"),
                    0,
                ),
            )
            self.__db_connection.commit()
        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def get_language(self):
        self.__cur.execute("SELECT language FROM global_settings")
        return self.__cur.fetchone()[0]

    def __del__(self):
        self.__db_connection.close()
