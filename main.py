import sys
from PyQt5 import QtWidgets, QtCore, QtSvg
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from database import Database
from popup import PopUp


class Main(QMainWindow):
    def __init__(self, app):
        super(Main, self).__init__()
        self.app = app
        self.initUI()

    def initUI(self):
        screen = self.app.primaryScreen()
        rect = screen.availableGeometry()
        self.setGeometry(50, 100, rect.width() - 200, rect.height() - 200)
        self.setWindowTitle("LocalPythonCMS - Create, edit, and publish web content!")

        self.db = Database()

        # Menu
        self.topBar = self.menuBar()
        self.topBarFile = self.topBar.addMenu("File")
        self.topBarEdit = self.topBar.addMenu("Edit")
        self.topBarHelp = self.topBar.addMenu("Help")

        # File
        self.topBarFileManager = QtWidgets.QAction("Manager", self)
        self.topBarFile.addAction(self.topBarFileManager)
        self.topBarFileImport = QtWidgets.QAction("Import", self)
        self.topBarFile.addAction(self.topBarFileImport)
        self.topBarFileExport = QtWidgets.QAction("Export", self)
        self.topBarFile.addAction(self.topBarFileExport)
        self.topBarFile.addSeparator()
        self.topBarFileExit = QtWidgets.QAction("Quit", self)
        self.topBarFile.addAction(self.topBarFileExit)
        self.topBarFileExit.triggered.connect(self.topBarFileExitFunction)
        self.topBarFileExit.setShortcut(QKeySequence.Quit)

        # Edit
        self.topBarFileSettings = QtWidgets.QAction("Settings", self)
        self.topBarEdit.addAction(self.topBarFileSettings)

        # Help
        self.topBarHelpDocumentation = QtWidgets.QAction("Documentation", self)
        self.topBarHelp.addAction(self.topBarHelpDocumentation)
        self.topBarHelpUpdates = QtWidgets.QAction("Check for updates", self)
        self.topBarHelp.addAction(self.topBarHelpUpdates)
        self.topBarHelpBug = QtWidgets.QAction("Report a bug", self)
        self.topBarHelp.addAction(self.topBarHelpBug)
        self.topBarHelpAbout = QtWidgets.QAction("About", self)
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
            '<span style="font-size: 14pt; font-weight: 600;">LocalPythonCMS</span><br><span font-size: 12pt;>Create, edit, and publish web content!</span>'
        )
        self.label.move(128, 50)
        self.label.adjustSize()

        self.labelForm = QtWidgets.QLabel(self)
        self.labelForm.setText(
            "<span font-size: 12pt;>Use your sign in credentials</span>"
        )
        self.labelForm.move(50, 154)
        self.labelForm.adjustSize()

        self.inputName = QtWidgets.QLineEdit(self)
        self.inputName.move(50, 200)
        self.inputName.setPlaceholderText("Username")
        self.inputName.setFixedWidth(150)

        self.inputPass = QtWidgets.QLineEdit(self)
        self.inputPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPass.move(50, 240)
        self.inputPass.setPlaceholderText("Password")
        self.inputPass.setFixedWidth(150)

        self.btnLogin = QtWidgets.QPushButton(self)
        self.btnLogin.setText("Sign in")
        self.btnLogin.setMinimumWidth(150)
        self.btnLogin.move(50, 280)
        self.btnLogin.clicked.connect(self.btnLoginEvent)

        self.btnRegister = QtWidgets.QPushButton(self)
        self.btnRegister.setText("Create account")
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
            "<span font-size: 12pt;>Use your sign in credentials</span>"
        )
        self.labelForm.adjustSize()

    def btnRegisterEvent(self):
        self.labelForm.setText(
            "<span font-size: 12pt;><b>Username</b>: You can use letters, numbers & periods<br><b>Password:</b> Use 8 or more characters with a mix of letters, numbers & symbols)</span>"
        )
        self.labelForm.adjustSize()

    def topBarFileExitFunction(self):
        self.close()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def topBarHelpAboutFunction(self):
        self.about = PopUp(
            "About",
            '<div style="text-align: center;"><span style="font-size: 14pt; font-weight: 600;">LocalPythonCMS</span><br><span font-size: 12pt;>Create, edit, and publish web content!</span></div>',
        )
        self.about.resize(500, 200)
        self.about.show()
        self.center()


def window():
    app = QApplication(sys.argv)
    win = Main(app)
    win.show()
    sys.exit(app.exec_())


window()
