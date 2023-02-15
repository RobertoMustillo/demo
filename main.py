import sys

from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("welcomescreen2.ui",self)
        self.login.clicked.connect(self.goto_login)
        self.chiudi.clicked.connect(exit)
        self.widget = QtWidgets.QStackedWidget()
        #fornisce uno stack di widget in cui è visibile un solo widget alla volta

        #self.image.setPixmap(QPixmap('sfondo.png'))
        self.widget.addWidget(self)
        self.widget.setFixedSize(1440, 760)
        self.widget.show()

        #self.widget.showMaximized()

    #def aggiungi_ui(self):
     #   self.widget.addWidget(self)
      #  self.widget.showMaximized()

    def goto_login(self):
        from login.LoginScreen import LoginScreen
        login = LoginScreen()
        self.widget.addWidget(login)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    welcome = WelcomeScreen()
    #widget = QtWidgets.QStackedWidget()
    #widget.addWidget(welcome)
    #widget.showMaximized()
    # welcome.aggiungi_ui()

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")

