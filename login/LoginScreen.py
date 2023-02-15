import mysql
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

import main
from home.Home import Home

class LoginScreen(QDialog):
    autorizzazione_accesso = None

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("login/login2.ui",self)

        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.login_function)
        self.login.setShortcut("Return")
        self.esci.clicked.connect(self.funz_esci)

        self.widget = QtWidgets.QStackedWidget()
        #self.image.setPixmap(QPixmap('sfondo.png'))

    def login_function(self):
        user = self.emailfield.text()
        password = self.passwordfield.text()

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )
        # Generazione del cursore
        cursore = db.cursor()
        query = "select * from dipendente"
        cursore.execute(query)
        result = cursore.fetchall()

        # creo un array di cognomi
        self.cognomi = []
        for x in result:
            self.cognomi.append(x[2])


        #if len(user)==0 or len(password)==0:
         #   self.error.setText("Please input all fields.")

        #elif user=="1" and password=="1":
        if user=="admin" and password=="admin":
            LoginScreen.autorizzazione_accesso = "Admin"

            #self.error.setText("sei dentro al bd.")

            home = Home()
            self.window().close()
            #self.widget.addWidget(clienti)
            self.widget.addWidget(home)
            self.widget.showMaximized()
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

        else:
            for c in self.cognomi:
                if user == c and password == c:
                    LoginScreen.autorizzazione_accesso = "Dip"

                    print("Hello dip: "+c)
                    home = Home()
                    self.window().close()
                    self.widget.addWidget(home)
                    self.widget.showMaximized()
                    self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
                else:
                    self.error.setText("Credenziali errate!")
                    self.emailfield.setText("")
                    self.passwordfield.setText("")


            # if len(user)==0 or len(password)==0:
            #self.error.setText("Utente o password errata.")
            #self.emailfield.setText("")
            #self.passwordfield.setText("")

    def funz_esci(self):
        self.welcome = main.WelcomeScreen()
        self.window().close()
        #self.widget.addWidget(welcome)
        #self.widget.showMaximized()
        #self.widget.setCurrentIndex(self.widget.currentIndex() + 1)