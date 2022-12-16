import sys
import webbrowser
import requests
import i18n
from PyQt5 import QtWidgets, QtCore, QtSvg
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QStatusBar
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from datetime import datetime
from db.database import Database
from db.actions import Actions
from popup import PopUp


class Main(QMainWindow):
    def __init__(self, app, locale):
        super(Main, self).__init__()
        self.app = app
        self.locale = locale
        self.initUI()

    def initUI(self):
        i18n.load_path.append("locales")
        i18n.set("locale", self.locale)
        i18n.set("fallback", "en")
        screen = self.app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(50, 100, rect.width() - 200, rect.height() - 200)
        self.setWindowTitle(i18n.t("translate.softwareTitle"))
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.setStatus(i18n.t("translate.starUpStatus"))

        # Menu
        self.topBar = self.menuBar()
        self.topBarFile = self.topBar.addMenu(i18n.t("translate.file"))
        self.topBarEdit = self.topBar.addMenu(i18n.t("translate.edit"))
        self.topBarHelp = self.topBar.addMenu(i18n.t("translate.help"))

        # File
        self.topBarFileManager = QtWidgets.QAction(i18n.t("translate.manager"), self)
        self.topBarFile.addAction(self.topBarFileManager)
        self.topBarFileImport = QtWidgets.QAction(i18n.t("translate.import"), self)
        self.topBarFile.addAction(self.topBarFileImport)
        self.topBarFileExport = QtWidgets.QAction(i18n.t("translate.export"), self)
        self.topBarFile.addAction(self.topBarFileExport)
        self.topBarFile.addSeparator()
        self.topBarFileExit = QtWidgets.QAction(i18n.t("translate.quit"), self)
        self.topBarFile.addAction(self.topBarFileExit)
        self.topBarFileExit.triggered.connect(self.topBarFileExitFunction)
        self.topBarFileExit.setShortcut(QKeySequence.Quit)

        # Edit
        self.topBarFileSettings = QtWidgets.QAction(i18n.t("translate.settings"), self)
        self.topBarEdit.addAction(self.topBarFileSettings)

        # Help
        self.topBarHelpDocumentation = QtWidgets.QAction(
            i18n.t("translate.documentation"), self
        )
        self.topBarHelp.addAction(self.topBarHelpDocumentation)
        self.topBarHelpDocumentation.triggered.connect(
            lambda: self.setBrowserContent(
                "https://github.com/ncklinux/LocalPythonCMS/blob/main/README.md"
            )
        )
        self.topBarHelpUpdates = QtWidgets.QAction(
            i18n.t("translate.checkForUpdates"), self
        )
        self.topBarHelp.addAction(self.topBarHelpUpdates)
        self.topBarHelpBug = QtWidgets.QAction(i18n.t("translate.reportABug"), self)
        self.topBarHelpUpdates.triggered.connect(self.checkForUpdates)
        self.topBarHelp.addAction(self.topBarHelpBug)
        self.topBarHelpBug.triggered.connect(self.topBarHelpBugFunction)
        self.topBarHelpAbout = QtWidgets.QAction(i18n.t("translate.about"), self)
        self.topBarHelp.addAction(self.topBarHelpAbout)
        self.topBarHelpAbout.triggered.connect(self.topBarHelpAboutFunction)

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
            + i18n.t("translate.softwareName")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.softwareSlogan")
            + "</span>"
        )
        self.label.move(128, 50)
        self.label.adjustSize()

        # User login
        self.loginLabel = QtWidgets.QLabel(self)
        self.loginLabel.setText(
            "<span font-size: 12pt;>" + i18n.t("translate.useCredentials") + "</span>"
        )
        self.loginLabel.move(50, 154)
        self.loginLabel.adjustSize()

        self.loginUsername = QtWidgets.QLineEdit(self)
        self.loginUsername.move(50, 200)
        self.loginUsername.setPlaceholderText(i18n.t("translate.username"))
        self.loginUsername.setFixedWidth(150)

        self.loginPassword = QtWidgets.QLineEdit(self)
        self.loginPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginPassword.move(50, 240)
        self.loginPassword.setPlaceholderText(i18n.t("translate.password"))
        self.loginPassword.setFixedWidth(150)

        self.btnLogin = QtWidgets.QPushButton(self)
        self.btnLogin.setText(i18n.t("translate.signIn"))
        self.btnLogin.setMinimumWidth(150)
        self.btnLogin.move(50, 280)
        self.btnLogin.clicked.connect(self.btnLoginEvent)

        # New user registration
        self.registerLabel = QtWidgets.QLabel(self)
        self.registerLabel.setText(
            "<span font-size: 12pt;><b>"
            + i18n.t("translate.username")
            + "</b>: "
            + i18n.t("translate.usernameDPrerequisites")
            + "<br><b>"
            + i18n.t("translate.password")
            + ":</b> "
            + i18n.t("translate.passwordPrerequisites")
            + "</span>"
        )
        self.registerLabel.move(50, 354)
        self.registerLabel.adjustSize()

        self.registerFirstname = QtWidgets.QLineEdit(self)
        self.registerFirstname.move(50, 400)
        self.registerFirstname.setPlaceholderText(i18n.t("translate.firstname"))
        self.registerFirstname.setFixedWidth(150)

        self.registerLastname = QtWidgets.QLineEdit(self)
        self.registerLastname.move(50, 440)
        self.registerLastname.setPlaceholderText(i18n.t("translate.lastname"))
        self.registerLastname.setFixedWidth(150)

        self.registerEmail = QtWidgets.QLineEdit(self)
        self.registerEmail.move(50, 480)
        self.registerEmail.setPlaceholderText(i18n.t("translate.email"))
        self.registerEmail.setFixedWidth(150)

        self.registerUsername = QtWidgets.QLineEdit(self)
        self.registerUsername.move(50, 520)
        self.registerUsername.setPlaceholderText(i18n.t("translate.username"))
        self.registerUsername.setFixedWidth(150)

        self.registerPassword = QtWidgets.QLineEdit(self)
        self.registerPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.registerPassword.move(50, 560)
        self.registerPassword.setPlaceholderText(i18n.t("translate.password"))
        self.registerPassword.setFixedWidth(150)

        self.btnRegister = QtWidgets.QPushButton(self)
        self.btnRegister.setText(i18n.t("translate.createAccount"))
        self.btnRegister.setMinimumWidth(150)
        self.btnRegister.move(50, 600)
        self.btnRegister.clicked.connect(self.btnRegisterEvent)

        """
        grid.addWidget(self.btnLogin, 0, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        grid.addWidget(
            self.btnRegister, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom
        )
        """

    def btnLoginEvent(self):
        self.loginLabel.setText(
            "<span font-size: 12pt;>" + i18n.t("translate.useCredentials") + "</span>"
        )
        self.loginLabel.adjustSize()
        # print(self.loginUsername.text())
        # print(self.loginPassword.text())

    def btnRegisterEvent(self):
        if (
            self.registerFirstname.text()
            and self.registerLastname.text()
            and self.registerEmail.text()
            and self.registerUsername.text()
            and self.registerPassword.text()
        ):
            dba = Actions()
            dba.registerNewUser(
                self.registerFirstname.text(),
                self.registerLastname.text(),
                self.registerEmail.text(),
                self.registerUsername.text(),
                self.registerPassword.text(),
            )
            self.registerLabel.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.registrationProgress")
                + "</span>"
            )
        else:
            self.registerLabel.setText(
                "<span font-size: 12pt;>"
                + i18n.t("translate.registrationFieldsRequired")
                + "</span>"
            )

    def topBarFileExitFunction(self):
        self.close()

    def center(self):
        frameGeo = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        frameGeo.moveCenter(centerPoint)
        self.move(frameGeo.topLeft())

    def topBarHelpAboutFunction(self):
        self.about = PopUp(
            "About",
            '<div style="text-align: center;"><span style="font-size: 14pt; font-weight: 600;">'
            + i18n.t("translate.softwareName")
            + "</span><br><span font-size: 12pt;>"
            + i18n.t("translate.softwareSlogan")
            + "</span></div>",
        )
        self.about.resize(500, 200)
        self.about.show()
        self.center()

    def setStatus(self, status=None):
        self.statusBar.showMessage(status)

    def topBarHelpBugFunction(self):
        webbrowser.open_new_tab("https://github.com/ncklinux/LocalPythonCMS/issues/new")

    def setBrowserContent(self, url):
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(url))
        self.browser.setWindowTitle(i18n.t("translate.documentation"))
        self.browser.resize(900, 600)
        self.browser.show()

    def checkForUpdates(self):
        response = requests.get(
            "https://api.github.com/repos/ncklinux/LocalPythonCMS/releases/latest"
        )
        if response.json()["message"] == "Not Found":
            print(response.json())
            self.about = PopUp(
                i18n.t("translate.checkForUpdates"),
                '<div style="text-align: center;"><span style="font-size: 14pt; font-weight: 600;">'
                + i18n.t("translate.softwareName")
                + "</span><br><span font-size: 12pt;>"
                + i18n.t("translate.softwareSlogan")
                + "</span>"
                + "<br><br><span font-size: 12pt;>"
                + i18n.t("translate.checkForUpdatesNoVersionYetError")
                + "</span>"
                + "</div>",
            )
        else:
            # TODO: Get version, compare and update
            print("COMPARE VERSIONS")
        self.about.resize(560, 200)
        self.about.show()
        self.center()


def window():
    app = QApplication(sys.argv)
    db = Database()
    win = Main(app, db.getLanguage())
    win.show()
    sys.exit(app.exec_())


window()
