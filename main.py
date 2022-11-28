import sys
import i18n
from PyQt5 import QtWidgets, QtCore, QtSvg
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QStatusBar
from datetime import datetime
from database import Database
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
        self.topBarHelpUpdates = QtWidgets.QAction(
            i18n.t("translate.checkForUpdates"), self
        )
        self.topBarHelp.addAction(self.topBarHelpUpdates)
        self.topBarHelpBug = QtWidgets.QAction(i18n.t("translate.reportABug"), self)
        self.topBarHelp.addAction(self.topBarHelpBug)
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

        self.labelForm = QtWidgets.QLabel(self)
        self.labelForm.setText(
            "<span font-size: 12pt;>" + i18n.t("translate.useCredentials") + "</span>"
        )
        self.labelForm.move(50, 154)
        self.labelForm.adjustSize()

        self.inputName = QtWidgets.QLineEdit(self)
        self.inputName.move(50, 200)
        self.inputName.setPlaceholderText(i18n.t("translate.username"))
        self.inputName.setFixedWidth(150)

        self.inputPass = QtWidgets.QLineEdit(self)
        self.inputPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPass.move(50, 240)
        self.inputPass.setPlaceholderText(i18n.t("translate.password"))
        self.inputPass.setFixedWidth(150)

        self.btnLogin = QtWidgets.QPushButton(self)
        self.btnLogin.setText(i18n.t("translate.signIn"))
        self.btnLogin.setMinimumWidth(150)
        self.btnLogin.move(50, 280)
        self.btnLogin.clicked.connect(self.btnLoginEvent)

        self.btnRegister = QtWidgets.QPushButton(self)
        self.btnRegister.setText(i18n.t("translate.createAccount"))
        self.btnRegister.setMinimumWidth(150)
        self.btnRegister.move(50, 320)
        self.btnRegister.clicked.connect(self.btnRegisterEvent)

        """
        grid.addWidget(self.btnLogin, 0, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        grid.addWidget(
            self.btnRegister, 0, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom
        )
        """

    def btnLoginEvent(self):
        self.labelForm.setText(
            "<span font-size: 12pt;>" + i18n.t("translate.useCredentials") + "</span>"
        )
        self.labelForm.adjustSize()

    def btnRegisterEvent(self):
        self.labelForm.setText(
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
        self.labelForm.adjustSize()

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


def window():
    app = QApplication(sys.argv)
    db = Database()
    win = Main(app, db.getLanguage())
    win.show()
    sys.exit(app.exec_())


window()
