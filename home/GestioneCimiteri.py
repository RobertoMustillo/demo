from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets

from PyQt5.uic import loadUi

from aggiuntaservizio.AggiuntaServizio import AggiuntaServizio
from associazionecimitero.AssociazioneCimitero import AssociazioneCimitero
from associazionelapidi.AssociazioneLapidi import AssociazioneLapidi
from cimitero.Cimitero import Cimitero
from defunti.DefuntiScreen import DefuntiScreen
from manutenzione.Manutenzione import Manutenzione
from servizioaggiuntivo.ServizioAggiuntivo import ServizioAggiuntivo


class GestioneCimiteri(QDialog):
    def __init__(self):
        super(GestioneCimiteri, self).__init__()

        loadUi("home/gestione_cimitero2.ui", self)
        self.widget = QtWidgets.QStackedWidget()
        self.listWidget.itemDoubleClicked.connect(self.goto_table)
        self.apri.clicked.connect(self.goto_table)
        self.esci.clicked.connect(self.funz_esci)

        # self.image.setPixmap(QPixmap('sfondo.png'))

    def goto_defunti(self):
        defunti = DefuntiScreen()
        self.window().close()
        self.widget.addWidget(defunti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_cimitero(self):
        cimitero = Cimitero()
        self.window().close()
        self.widget.addWidget(cimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_manutenzione(self):
        manutenzione = Manutenzione()
        self.window().close()
        self.widget.addWidget(manutenzione)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_aggiuntaservizio(self):
        aggiuntaservizio = AggiuntaServizio()
        self.window().close()
        self.widget.addWidget(aggiuntaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_servizioaggiuntivo(self):
        servizioaggiuntivo = ServizioAggiuntivo()
        self.window().close()
        self.widget.addWidget(servizioaggiuntivo)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_associazionecimitero(self):
        associazionecimitero = AssociazioneCimitero()
        self.window().close()
        self.widget.addWidget(associazionecimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_associazionelapidi(self):
        associazionelapidi = AssociazioneLapidi()
        self.window().close()
        self.widget.addWidget(associazionelapidi)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # apre la tabella selezionata dalla lista
    def goto_table(self):
        try:
            if self.listWidget.currentRow() == 0:
                self.goto_cimitero()
            elif self.listWidget.currentRow() == 1:
                self.goto_defunti()
            elif self.listWidget.currentRow() == 2:
                self.goto_manutenzione()
            elif self.listWidget.currentRow() == 3:
                self.goto_associazionelapidi()
            elif self.listWidget.currentRow() == 4:
                self.goto_associazionecimitero()
            elif self.listWidget.currentRow() == 5:
                self.goto_servizioaggiuntivo()
            elif self.listWidget.currentRow() == 6:
                self.goto_aggiuntaservizio()

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una tabella da aprire.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.Home import Home
        home = Home()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
