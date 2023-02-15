from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ApriCliente(QDialog):
    def __init__(self, cliente_selezionato):
        super(ApriCliente, self).__init__()
        loadUi("clienti/apricliente.ui", self)
        self.cliente_selezionato = cliente_selezionato  # riga del cliente selezionato (che parte da 0)!!
        self.annulla.clicked.connect(self.funz_esci)
        #self.modifica.clicked.connect(self.modifica_cliente)

        self.widget = QtWidgets.QStackedWidget()

        self.id.setReadOnly(True)
        self.nome.setReadOnly(True)
        self.cognome.setReadOnly(True)
        self.cf.setReadOnly(True)
        self.dateEdit.setReadOnly(True)
        self.email.setReadOnly(True)
        #self.comboBox.setReadOnly = True
        self.citta.setReadOnly(True)
        self.cap.setReadOnly(True)
        self.via.setReadOnly(True)
        self.numerocivico.setReadOnly(True)


    def funz_esci(self):
        from clienti.ClientiScreen import ClientiScreen
        clienti = ClientiScreen()
        self.window().close()
        self.widget.addWidget(clienti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
