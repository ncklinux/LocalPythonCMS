import sqlite3
from common.functions import Functions
from common.logger_factory import LoggerFactory


class Actions(object):

    __DB_LOCATION = "assets/sqlite/localpythoncms.sqlite"

    def __init__(self):
        self.__db_connection = sqlite3.connect(self.__DB_LOCATION)
        self.__cur = self.__db_connection.cursor()
        self.logger = LoggerFactory.CreateLogger(__name__)

    def get_language(self):
        self.__cur.execute("SELECT language FROM users")
        return self.__cur.fetchone()[0]

    def register_new_user(
        self, firstname, lastname, email, username, password, language
    ):
        try:
            self.__cur.execute("SELECT 1 FROM users WHERE email = ?", [email])
            data = self.__cur.fetchall()
            if len(data) == 0:
                common_functions = Functions()
                self.__cur.execute(
                    "INSERT INTO users VALUES (null, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        firstname,
                        lastname,
                        language,
                        email,
                        username,
                        common_functions.sha256(password),
                        0,
                    ),
                )
                self.__db_connection.commit()
                return True
            else:
                return False

        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def login_user(self, email, password):
        try:
            self.__cur.execute("SELECT 1 FROM users WHERE email = ?", [email])
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
                user_matching = self.__cur.fetchall()
                if user_matching:
                    self.__cur.execute(
                        "UPDATE users SET logged_in = 1 WHERE email = ?", [email]
                    )
                    self.__db_connection.commit()
                    return True
                else:
                    return False
            else:
                return False
        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def logout_user(self):
        self.__cur.execute("UPDATE users SET logged_in = 0")
        self.__db_connection.commit()
        if self.__cur.rowcount > 1:
            return True
        else:
            return False

    def manager_add(self, name):
        try:
            self.__cur.execute("SELECT 1 FROM manager WHERE name = ?", [name])
            data = self.__cur.fetchall()
            if len(data) == 0:
                self.__cur.execute(
                    "INSERT INTO manager (id, name) VALUES (null, ?)",
                    (name,),
                )
                self.__db_connection.commit()
                return True
            else:
                return False
        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def manager_get(self):
        try:
            self.__cur.execute("SELECT name FROM manager")
            rows = self.__cur.fetchall()
            return rows
        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def manager_delete(self, name):
        try:
            self.__cur.execute("SELECT 1 FROM manager WHERE name = ?", [name])
            data = self.__cur.fetchall()
            if len(data) == 1:
                self.__cur.execute("DELETE FROM manager WHERE name = ?", [name])
                self.__db_connection.commit()
                return True
            else:
                return False
        except sqlite3.IntegrityError as e:
            self.logger.error("Exception: {}".format(type(e)))

    def __del__(self):
        self.__db_connection.close()
