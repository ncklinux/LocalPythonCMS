import re
import sys
import webbrowser
import requests
import i18n
import glob
from PyQt5 import QtWidgets, QtCore, QtSvg
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QDesktopWidget,
    QStatusBar,
    QComboBox,
)
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from datetime import datetime
from common.functions import Functions
from common.logger_factory import LoggerFactory
from db.database import Database
from db.actions import Actions
from popup import PopUp


class Main(QMainWindow):
    def __init__(self, app, locale):
        super(Main, self).__init__()
        self.app = app
        self.locale = locale
        self.logger = LoggerFactory.CreateLogger(__name__)
        self.initUI()

    def initUI(self):
        i18n.load_path.append("locales")
        i18n.set("locale", self.locale)
        i18n.set("fallback", "us")
        screen = self.app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(50, 100, rect.width() - 200, rect.height() - 200)
        self.setWindowTitle(i18n.t("translate.software_title"))
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.set_status(i18n.t("translate.star_up_status"))

        # Logging examples
        """
        self.logger.critical("Critical output")
        self.logger.error("Error output")
        self.logger.warning("Warning output")
        self.logger.info("Info output")
        self.logger.debug("Debug output")
        """

        # Menu
        self.top_bar = self.menuBar()
        self.top_bar_file = self.top_bar.addMenu(i18n.t("translate.file"))
        self.top_bar_edit = self.top_bar.addMenu(i18n.t("translate.edit"))
        self.top_bar_help = self.top_bar.addMenu(i18n.t("translate.help"))

        # File
        self.top_bar_file_manager = QtWidgets.QAction(i18n.t("translate.manager"), self)
        self.top_bar_file.addAction(self.top_bar_file_manager)
        self.top_bar_file_import = QtWidgets.QAction(i18n.t("translate.import"), self)
        self.top_bar_file.addAction(self.top_bar_file_import)
        self.top_bar_file_export = QtWidgets.QAction(i18n.t("translate.export"), self)
        self.top_bar_file.addAction(self.top_bar_file_export)
        self.top_bar_file.addSeparator()
        self.top_bar_file_exit = QtWidgets.QAction(i18n.t("translate.quit"), self)
        self.top_bar_file.addAction(self.top_bar_file_exit)
        self.top_bar_file_exit.triggered.connect(self.top_bar_file_exit_function)
        self.top_bar_file_exit.setShortcut(QKeySequence.Quit)

        # Edit
        self.top_bar_file_settings = QtWidgets.QAction(
            i18n.t("translate.settings"), self
        )
        self.top_bar_edit.addAction(self.top_bar_file_settings)

        # Help
        self.top_bar_help_documentation = QtWidgets.QAction(
            i18n.t("translate.documentation"), self
        )
        self.top_bar_help.addAction(self.top_bar_help_documentation)
        self.top_bar_help_documentation.triggered.connect(
            lambda: self.set_browser_content(
                "https://github.com/ncklinux/LocalPythonCMS/blob/main/README.md"
            )
        )
        self.top_bar_help_updates = QtWidgets.QAction(
            i18n.t("translate.check_for_updates"), self
        )
        self.top_bar_help.addAction(self.top_bar_help_updates)
        self.top_bar_help_bug = QtWidgets.QAction(
            i18n.t("translate.report_a_bug"), self
        )
        self.top_bar_help_updates.triggered.connect(self.check_for_updates)
        self.top_bar_help.addAction(self.top_bar_help_bug)
        self.top_bar_help_bug.triggered.connect(self.top_bar_help_bug_function)
        self.top_bar_help_about = QtWidgets.QAction(i18n.t("translate.about"), self)
        self.top_bar_help.addAction(self.top_bar_help_about)
        self.top_bar_help_about.triggered.connect(self.top_bar_help_about_function)

        """
        w = QtWidgets.QWidget()
        self.setCentralWidget(w)
        grid = QtWidgets.QGridLayout(w)
        """

        self.logo = QtSvg.QSvgWidget(self)
        self.logo.load("./assets/svg/logo.svg")
        self.logo.setGeometry(QtCore.QRect(0, 0, 70, 38))
        self.logo.move(50, 50)
        self.logo.show()

        self.label = QtWidgets.QLabel(self)
        self.label.setText(
            '<span style="font-size: 14pt; font-weight: 600;">'
            + i18n.t("translate.software_name")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.software_slogan")
            + "</span>"
        )
        self.label.move(128, 50)
        self.label.adjustSize()

        # User login
        self.login_label = QtWidgets.QLabel(self)
        self.login_label.setText(
            "<span font-size: 12pt;>"
            + i18n.t("translate.use_sign_in_credentials")
            + "</span>"
        )
        self.login_label.move(50, 154)
        self.login_label.adjustSize()

        self.login_email = QtWidgets.QLineEdit(self)
        self.login_email.move(50, 200)
        self.login_email.setPlaceholderText(i18n.t("translate.email"))
        self.login_email.setFixedWidth(230)

        self.login_password = QtWidgets.QLineEdit(self)
        self.login_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login_password.move(50, 240)
        self.login_password.setPlaceholderText(i18n.t("translate.password"))
        self.login_password.setFixedWidth(230)

        self.btn_login = QtWidgets.QPushButton(self)
        self.btn_login.setText(i18n.t("translate.sign_in"))
        self.btn_login.setMinimumWidth(120)
        self.btn_login.move(50, 280)
        self.btn_login.clicked.connect(self.btn_login_event)

        self.btn_login_form_reset = QtWidgets.QPushButton(self)
        self.btn_login_form_reset.setText(i18n.t("translate.clear"))
        self.btn_login_form_reset.setMinimumWidth(100)
        self.btn_login_form_reset.move(180, 280)
        self.btn_login_form_reset.clicked.connect(
            lambda: self.reset_form_fields(self.login_password, self.login_email)
        )

        # New user registration
        self.register_label = QtWidgets.QLabel(self)
        self.register_label.setText(
            "<span font-size: 12pt;><b>"
            + i18n.t("translate.username")
            + "</b>: "
            + i18n.t("translate.username_prerequisites")
            + "<br><b>"
            + i18n.t("translate.password")
            + ":</b> "
            + i18n.t("translate.password_prerequisites")
            + "</span>"
        )
        self.register_label.move(50, 354)
        self.register_label.adjustSize()

        self.register_firstname = QtWidgets.QLineEdit(self)
        self.register_firstname.move(50, 400)
        self.register_firstname.setPlaceholderText(i18n.t("translate.firstname"))
        self.register_firstname.setFixedWidth(230)

        self.register_lastname = QtWidgets.QLineEdit(self)
        self.register_lastname.move(50, 440)
        self.register_lastname.setPlaceholderText(i18n.t("translate.lastname"))
        self.register_lastname.setFixedWidth(230)

        self.register_email = QtWidgets.QLineEdit(self)
        self.register_email.move(50, 480)
        self.register_email.setPlaceholderText(i18n.t("translate.email"))
        self.register_email.setFixedWidth(230)

        self.register_username = QtWidgets.QLineEdit(self)
        self.register_username.move(50, 520)
        self.register_username.setPlaceholderText(i18n.t("translate.username"))
        self.register_username.setFixedWidth(230)

        self.register_password = QtWidgets.QLineEdit(self)
        self.register_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_password.move(50, 560)
        self.register_password.setPlaceholderText(i18n.t("translate.password"))
        self.register_password.setFixedWidth(230)

        common_functions = Functions()
        self.register_language_list = common_functions.combo_box_data_frame(
            "language",
            "COUNTRYCODES",
            common_functions.get_country_codes_from_locales(),
            "LANGUAGES",
            i18n.t("translate.registration_select_language"),
        )
        self.register_language = QComboBox(self)
        for item in self.register_language_list.itertuples():
            self.register_language.addItem(item.LANGUAGES, item.COUNTRYCODES)
        self.register_language.move(50, 600)
        self.register_language.setFixedWidth(230)

        self.btn_register = QtWidgets.QPushButton(self)
        self.btn_register.setText(i18n.t("translate.register"))
        self.btn_register.setMinimumWidth(120)
        self.btn_register.move(50, 640)
        self.btn_register.clicked.connect(self.btn_register_event)

        self.btn_register_form_reset = QtWidgets.QPushButton(self)
        self.btn_register_form_reset.setText(i18n.t("translate.clear"))
        self.btn_register_form_reset.setMinimumWidth(100)
        self.btn_register_form_reset.move(180, 640)
        self.btn_register_form_reset.clicked.connect(
            lambda: self.reset_form_fields(
                self.register_firstname,
                self.register_lastname,
                self.register_email,
                self.register_username,
                self.register_password,
                self.register_language,
            )
        )

        """
        grid.addWidget(self.btn_login, 0, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        grid.addWidget(
            self.btn_register, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom
        )
        """

    def btn_login_event(self):
        self.login_label.setText(
            "<span font-size: 12pt;>"
            + i18n.t("translate.use_sign_in_credentials")
            + "</span>"
        )
        common_functions = Functions()
        if (
            common_functions.validate_email(self.login_email.text())
            and self.login_password.text()
        ):
            database_actions = Actions()
            if database_actions.login_user(
                self.login_email.text(),
                self.login_password.text(),
            ):
                print(
                    database_actions.login_user(
                        self.login_email.text(), self.login_password.text()
                    )
                )
                del database_actions
            else:
                self.login_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.login_failed")
                    + "</span>"
                )
        else:
            self.login_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.login_fields_required")
                + "</span>"
            )
        self.login_label.adjustSize()

    def btn_register_event(self):
        common_functions = Functions()
        if (
            self.register_firstname.text()
            and self.register_lastname.text()
            and common_functions.validate_email(self.register_email.text())
            and self.register_username.text()
            and self.register_password.text()
            and self.register_language.currentData().strip()
        ):
            self.register_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.registration_progress")
                + "</span>"
            )
            database_actions = Actions()
            if database_actions.register_new_user(
                self.register_firstname.text(),
                self.register_lastname.text(),
                self.register_email.text(),
                self.register_username.text(),
                self.register_password.text(),
                self.register_language.currentData(),
            ):
                del database_actions
                # self.btn_register.setEnabled(False)
                self.reset_form_fields(
                    self.register_firstname,
                    self.register_lastname,
                    self.register_email,
                    self.register_username,
                    self.register_password,
                    self.register_language,
                )
                self.register_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.registration_success")
                    + "</span>"
                )
            else:
                self.register_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.registration_failed")
                    + "</span>"
                )
        else:
            self.register_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.registration_fields_required")
                + "</span>"
            )

    def reset_form_fields(self, *fields):
        for item in fields:
            if re.search("QComboBox", str(item)):
                item.setCurrentIndex(0)
            else:
                item.clear()

    def top_bar_file_exit_function(self):
        self.close()

    def center(self):
        frame_geo = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def top_bar_help_about_function(self):
        self.about = PopUp(
            "About",
            '<div style="text-align: center;"><span style="font-size: 14pt; font-weight: 600;">'
            + i18n.t("translate.software_name")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.software_slogan")
            + "</span></div>",
        )
        self.about.resize(500, 200)
        self.about.show()
        self.center()

    def set_status(self, status=None):
        self.status_bar.showMessage(status)

    def top_bar_help_bug_function(self):
        webbrowser.open_new_tab("https://github.com/ncklinux/LocalPythonCMS/issues/new")

    def set_browser_content(self, url):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.browser.setWindowTitle(i18n.t("translate.documentation"))
        self.browser.resize(900, 600)
        self.browser.show()

    def check_for_updates(self):
        response = requests.get(
            "https://api.github.com/repos/ncklinux/LocalPythonCMS/releases/latest"
        )
        if response.json()["message"] == "Not Found":
            print(response.json())
            self.about = PopUp(
                i18n.t("translate.check_for_updates"),
                '<div style="text-align: center;"><span style="font-size: 14pt; font-weight: 600;">'
                + i18n.t("translate.software_name")
                + "</span><br><span font-size: 12pt;>"
                + i18n.t("translate.software_slogan")
                + "</span>"
                + "<br><br><span font-size: 12pt;>"
                + i18n.t("translate.check_for_updates_no_version_yet_error")
                + "</span>"
                + "</div>",
            )
        else:
            # TODO: Get version, compare and update
            self.logger.info("COMPARE VERSIONS")
        self.about.resize(560, 200)
        self.about.show()
        self.center()


def window():
    app = QApplication(sys.argv)
    db = Database()
    win = Main(app, db.get_language())
    del db
    win.show()
    sys.exit(app.exec_())


window()
