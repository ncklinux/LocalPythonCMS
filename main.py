import re
import sys
import i18n
import requests
import webbrowser
from typing import Any
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QMessageBox,
    QListWidget,
    QStatusBar,
    QComboBox,
    QLineEdit,
    QLabel,
)
from PyQt6.QtGui import QAction, QPixmap
from common.functions import Functions
from common.logger_factory import LoggerFactory
from db.database import Database
from db.actions import Actions
from popup import PopUp


class Main(QMainWindow):
    def __init__(self, app, locale) -> None:
        super(Main, self).__init__()
        self.app = app
        self.locale = locale
        self.status_bar: Any = None
        self.tb: Any = None
        self.tb_file: Any = None
        self.tb_file_manager: Any = None
        self.tb_file_import: Any = None
        self.tb_file_export: Any = None
        self.tb_file_quit: Any = None
        self.tb_edit: Any = None
        self.tb_edit_settings: Any = None
        self.tb_help: Any = None
        self.tb_help_documentation: Any = None
        self.tb_help_updates: Any = None
        self.tb_help_bug: Any = None
        self.tb_help_about: Any = None
        self.about_popup: Any = None
        self.login_email: Any = None
        self.login_password: Any = None
        self.register_label: Any = None
        self.register_firstname: Any = None
        self.register_lastname: Any = None
        self.register_email: Any = None
        self.register_username: Any = None
        self.register_password: Any = None
        self.register_language: Any = None
        self.register_language_list: Any = None
        self.manager_label: Any = None
        self.manager_connections: Any = None
        self.manager_input_name: Any = None
        self.btn_manager_add: Any = None
        self.btn_manager_remove: Any = None
        self.image: Any = None
        self.logger = LoggerFactory.CreateLogger(__name__)
        self.init_ui()

    def init_ui(self) -> None:
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

        # Logo
        self.logo = QLabel(self)
        pixmap = QPixmap("assets/images/logo.png")
        self.logo.setPixmap(pixmap)
        self.logo.move(44, 44)
        self.logo.resize(pixmap.width(), pixmap.height())
        self.label = QLabel(self)
        self.label.setText(
            '<span style="font-size: 14pt; font-weight: 600;">'
            + i18n.t("translate.software_name")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.software_slogan")
            + "</span>"
        )
        self.label.move(120, 56)
        self.label.adjustSize()

        # Top menubar
        self.tb = self.menuBar()
        self.tb_file = self.tb.addMenu(i18n.t("translate.file"))
        self.tb_edit = self.tb.addMenu(i18n.t("translate.edit"))
        self.tb_help = self.tb.addMenu(i18n.t("translate.help"))
        self.tb_file_manager = QAction(i18n.t("translate.manager"), self)
        self.tb_file_import = QAction(i18n.t("translate.import"), self)
        self.tb_file_export = QAction(i18n.t("translate.export"), self)
        self.tb_file_quit = QAction(i18n.t("translate.quit"), self)
        self.tb_edit_settings = QAction(i18n.t("translate.settings"), self)
        self.tb_help_documentation = QAction(i18n.t("translate.documentation"), self)
        self.tb_help_updates = QAction(i18n.t("translate.check_for_updates"), self)
        self.tb_help_bug = QAction(i18n.t("translate.report_a_bug"), self)
        self.tb_help_about = QAction(i18n.t("translate.about"), self)
        self.tb_file.addAction(self.tb_file_quit)
        self.tb_help.addAction(self.tb_help_documentation)
        self.tb_help.addAction(self.tb_help_updates)
        self.tb_help.addAction(self.tb_help_bug)
        self.tb_help.addAction(self.tb_help_about)
        self.tb_file_manager.triggered.connect(self.manager)
        # self.tb_file_import.triggered.connect(self.onMyToolBarButtonClick)
        # self.tb_file_export.triggered.connect(self.onMyToolBarButtonClick)
        self.tb_file_quit.triggered.connect(self.quit_app)
        # self.tb_edit_settings.triggered.connect(self.onMyToolBarButtonClick)
        self.tb_help_documentation.triggered.connect(
            lambda: self.open_url(
                "https://github.com/ncklinux/LocalPythonCMS/blob/main/README.md"
            )
        )
        self.tb_help_updates.triggered.connect(self.about)
        self.tb_help_bug.triggered.connect(
            lambda: self.open_url(
                "https://github.com/ncklinux/LocalPythonCMS/issues/new"
            )
        )
        self.tb_help_about.triggered.connect(self.about)

        # User login
        self.login_label = QLabel(self)
        self.login_label.setText(
            "<span font-size: 12pt;>"
            + i18n.t("translate.use_login_credentials")
            + "</span>"
        )
        self.login_label.move(50, 154)
        self.login_label.adjustSize()

        self.login_email = QLineEdit(self)
        self.login_email.move(50, 200)
        self.login_email.setPlaceholderText(i18n.t("translate.email"))
        self.login_email.setFixedWidth(230)
        self.login_email.returnPressed.connect(self.btn_login_event)

        self.login_password = QLineEdit(self)
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.move(50, 240)
        self.login_password.setPlaceholderText(i18n.t("translate.password"))
        self.login_password.setFixedWidth(230)
        self.login_password.returnPressed.connect(self.btn_login_event)

        self.btn_login = QPushButton(self)
        self.btn_login.setText(i18n.t("translate.login"))
        self.btn_login.setMinimumWidth(120)
        self.btn_login.move(50, 280)
        self.btn_login.clicked.connect(self.btn_login_event)

        self.btn_logout = QPushButton(self)
        self.btn_logout.setText(i18n.t("translate.logout"))
        self.btn_logout.setMinimumWidth(120)
        self.btn_logout.move(50, 200)
        self.btn_logout.clicked.connect(self.btn_logout_event)
        self.btn_logout.hide()

        self.btn_login_form_reset = QPushButton(self)
        self.btn_login_form_reset.setText(i18n.t("translate.clear"))
        self.btn_login_form_reset.setMinimumWidth(100)
        self.btn_login_form_reset.move(180, 280)
        self.btn_login_form_reset.clicked.connect(
            lambda: self.reset_form_fields(self.login_password, self.login_email)
        )

        # New user registration
        self.register_label = QLabel(self)
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

        self.register_firstname = QLineEdit(self)
        self.register_firstname.move(50, 400)
        self.register_firstname.setPlaceholderText(i18n.t("translate.firstname"))
        self.register_firstname.setFixedWidth(230)
        self.register_firstname.returnPressed.connect(self.btn_register_event)

        self.register_lastname = QLineEdit(self)
        self.register_lastname.move(50, 440)
        self.register_lastname.setPlaceholderText(i18n.t("translate.lastname"))
        self.register_lastname.setFixedWidth(230)
        self.register_lastname.returnPressed.connect(self.btn_register_event)

        self.register_email = QLineEdit(self)
        self.register_email.move(50, 480)
        self.register_email.setPlaceholderText(i18n.t("translate.email"))
        self.register_email.setFixedWidth(230)
        self.register_email.returnPressed.connect(self.btn_register_event)

        self.register_username = QLineEdit(self)
        self.register_username.move(50, 520)
        self.register_username.setPlaceholderText(i18n.t("translate.username"))
        self.register_username.setFixedWidth(230)
        self.register_username.returnPressed.connect(self.btn_register_event)

        self.register_password = QLineEdit(self)
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.move(50, 560)
        self.register_password.setPlaceholderText(i18n.t("translate.password"))
        self.register_password.setFixedWidth(230)
        self.register_password.returnPressed.connect(self.btn_register_event)

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

        self.btn_register = QPushButton(self)
        self.btn_register.setText(i18n.t("translate.register"))
        self.btn_register.setMinimumWidth(120)
        self.btn_register.move(50, 640)
        self.btn_register.clicked.connect(self.btn_register_event)

        self.btn_register_form_reset = QPushButton(self)
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

    def set_status(self, status: str) -> None:
        self.status_bar.showMessage(status)

    @staticmethod
    def open_url(self, url: str) -> None:
        webbrowser.open(url)

    def about(self):
        self.about_popup = PopUp(
            "About",
            '<div style="text-align: center;">'
            + '<span style="font-size: 14pt; font-weight: 600;">'
            + i18n.t("translate.software_name")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.software_slogan")
            + "</span></div>",
        )
        self.about_popup.resize(500, 200)
        self.about_popup.show()

    def updates(self) -> None:
        response = requests.get(
            "https://api.github.com/repos/ncklinux/LocalPythonCMS/releases/latest"
        )
        if response.json()["message"] == "Not Found":
            print(response.json())
            self.about_popup = PopUp(
                i18n.t("translate.check_for_updates"),
                '<div style="text-align: center;">'
                + '<span style="font-size: 14pt; font-weight: 600;">'
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
        self.about_popup.resize(500, 200)
        self.about_popup.show()

    def quit_app(self) -> None:
        database_actions = Actions()
        if database_actions.logout_user():
            del database_actions
            self.close()

    def btn_login_event(self) -> None:
        self.login_label.setText(
            "<span font-size: 12pt;>"
            + i18n.t("translate.use_login_credentials")
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
                self.btn_logout.show()
                self.login_email.hide()
                self.login_password.hide()
                self.btn_login.hide()
                self.btn_login_form_reset.hide()
                self.register_label.hide()
                self.register_firstname.hide()
                self.register_lastname.hide()
                self.register_email.hide()
                self.register_username.hide()
                self.register_password.hide()
                self.register_language.hide()
                self.btn_register.hide()
                self.btn_register_form_reset.hide()
                self.reset_form_fields(self.login_password, self.login_email)
                self.tb_file.removeAction(self.tb_file_quit)
                self.tb_file.addAction(self.tb_file_manager)
                self.tb_file.addAction(self.tb_file_import)
                self.tb_file.addAction(self.tb_file_export)
                self.tb_edit.addAction(self.tb_edit_settings)
                self.login_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.login_success")
                    + "</span>"
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

    def btn_logout_event(self) -> None:
        database_actions = Actions()
        if database_actions.logout_user():
            self.btn_logout.hide()
            self.login_email.show()
            self.login_password.show()
            self.btn_login.show()
            self.btn_login_form_reset.show()
            self.register_label.show()
            self.register_firstname.show()
            self.register_lastname.show()
            self.register_email.show()
            self.register_username.show()
            self.register_password.show()
            self.register_language.show()
            self.btn_register.show()
            self.btn_register_form_reset.show()
            self.tb_file.removeAction(self.tb_file_manager)
            self.tb_file.removeAction(self.tb_file_import)
            self.tb_file.removeAction(self.tb_file_export)
            self.tb_file.addAction(self.tb_file_quit)
            self.tb_edit.removeAction(self.tb_edit_settings)
            if self.manager_label:
                self.manager_label.hide()
                self.manager_connections.hide()
                self.manager_input_name.hide()
                self.btn_manager_add.hide()
                self.btn_manager_remove.hide()

            self.login_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.use_login_credentials")
                + "</span>"
            )
            del database_actions
        else:
            self.login_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.logout_failed")
                + "</span>"
            )

    def btn_register_event(self) -> None:
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

    def reset_form_fields(self, *fields) -> None:
        for item in fields:
            if re.search("QComboBox", str(item)):
                item.setCurrentIndex(0)
            else:
                item.clear()

    def manager(self) -> None:
        self.manager_label = QLabel(self)
        self.manager_label.setText(
            "<span font-size: 12pt;>" + i18n.t("translate.manager_title") + "</span>"
        )
        self.manager_label.move(50, 260)
        self.manager_label.adjustSize()
        self.manager_label.show()
        self.manager_input_name = QLineEdit(self)
        self.manager_input_name.move(50, 290)
        self.manager_input_name.setPlaceholderText(
            i18n.t("translate.manager_new_site_input_placeholder")
        )
        self.manager_input_name.setFixedWidth(200)
        self.manager_input_name.show()
        self.btn_manager_add = QPushButton(self)
        self.btn_manager_add.setText("+")
        self.btn_manager_add.setMinimumWidth(30)
        self.btn_manager_add.move(254, 290)
        self.btn_manager_add.clicked.connect(self.manager_add_site)
        self.btn_manager_add.show()
        self.btn_manager_remove = QPushButton(self)
        self.btn_manager_remove.setText("-")
        self.btn_manager_remove.setMinimumWidth(30)
        self.btn_manager_remove.move(358, 290)
        self.btn_manager_remove.clicked.connect(self.manager_delete_site)
        self.btn_manager_remove.show()
        database_actions = Actions()
        self.manager_connections = QListWidget(self)
        for row in database_actions.manager_get():
            self.manager_connections.addItem(row[0])
        self.manager_connections.setMinimumWidth(408)
        self.manager_connections.setMinimumHeight(130)
        self.manager_connections.move(50, 330)
        self.manager_connections.show()

    def manager_add_site(self) -> None:
        if self.manager_input_name.text():
            database_actions = Actions()
            if database_actions.manager_add(self.manager_input_name.text()):
                self.manager_input_name.clear()
                self.manager_connections.clear()
                for row in database_actions.manager_get():
                    self.manager_connections.addItem(row[0])
                del database_actions
            else:
                self.manager_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.manager_new_site_failed")
                    + "</span>"
                )
                self.manager_label.adjustSize()
        else:
            self.manager_label.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.manager_new_site_input_empty")
                + "</span>"
            )
            self.manager_label.adjustSize()

    def manager_delete_site(self) -> None:
        if self.manager_connections.currentItem():
            dlg = QMessageBox(self)
            dlg.setWindowTitle(i18n.t("translate.manager_delete_title"))
            dlg.setText(i18n.t("translate.manager_delete_confirmation"))
            dlg.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            button = dlg.exec()
            if button == QMessageBox.StandardButton.Yes:
                database_actions = Actions()
                if database_actions.manager_delete(
                    self.manager_connections.currentItem().text()
                ):
                    self.manager_connections.clear()
                    for row in database_actions.manager_get():
                        self.manager_connections.addItem(row[0])
                    del database_actions
                else:
                    self.manager_label.setText(
                        "<span font-size: 12pt;>"
                        + i18n.t("translate.manager_delete_site_failed")
                        + "</span>"
                    )
                    self.manager_label.adjustSize()
            else:
                self.manager_label.setText(
                    "<span font-size: 12pt;>"
                    + i18n.t("translate.manager_delete_site_select_error")
                    + "</span>"
                )
                self.manager_label.adjustSize()


def window():
    app = QApplication(sys.argv)
    db = Database()
    win = Main(app, db.get_language())
    del db
    win.show()
    sys.exit(app.exec())


window()
