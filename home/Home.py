import mysql
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets

from PyQt5.uic import loadUi

from aggiuntaservizio.AggiuntaServizio import AggiuntaServizio
from assegnamento.Assegnamento import Assegnamento
from assegnamentoturno.AssegnamentoTurno import AssegnamentoTurno
from associazionecimitero.AssociazioneCimitero import AssociazioneCimitero
from associazionelapidi.AssociazioneLapidi import AssociazioneLapidi
from bustapaga.BustaPaga import BustaPaga
from cimitero.Cimitero import Cimitero
from clienti.ClientiScreen import ClientiScreen
from defunti.DefuntiScreen import DefuntiScreen
from dipendenti.Dipendenti import Dipendenti
from emissionefattura.EmissioneFattura import EmissioneFattura
from emissionefatturaservizio.EmissioneFatturaServizio import EmissioneFatturaServizio
from eventi.Evento import Evento
from fattura.Fattura import Fattura
from home.GestioneCimiteri import GestioneCimiteri
from home.GestioneClienti import GestioneClienti
from home.GestioneDipendenti import GestioneDipendenti
from manutenzione.Manutenzione import Manutenzione
from operazioni.Operazioni import Operazioni
from servizioaggiuntivo.ServizioAggiuntivo import ServizioAggiuntivo
from telefonocliente.TelefonoCliente import TelefonoCliente
from telefonodipendente.TelefonoDipendente import TelefonoDipendente
from turno.Turno import Turno


class Home(QDialog):
    def __init__(self):
        super(Home, self).__init__()
        from login.LoginScreen import LoginScreen
        if LoginScreen.autorizzazione_accesso=="Admin":
            loadUi("home/home3.ui", self)
            self.widget = QtWidgets.QStackedWidget()

            self.clienti.clicked.connect(self.goto_gestione_clienti)
            self.dipendenti.clicked.connect(self.goto_gestione_dip)
            self.cimiteri.clicked.connect(self.goto_gestione_cimiteri)

            self.operazioni.clicked.connect(self.goto_operazioni)
            self.esci.clicked.connect(self.funz_esci)

            #self.image.setPixmap(QPixmap('sfondo.png'))
        elif LoginScreen.autorizzazione_accesso == "Dip":
            loadUi("home/home_dip2.ui", self)
            self.widget = QtWidgets.QStackedWidget()

            self.dipendenti.clicked.connect(self.goto_gestione_dip)
            self.cimiteri.clicked.connect(self.goto_gestione_cimiteri)
            self.esci.clicked.connect(self.funz_esci)

            #self.image.setPixmap(QPixmap('sfondo.png'))

     #   self.load_tables()
      #  self.listWidget.setWindowTitle('Tables in db illuminazione votiva')
       # self.listWidget.itemDoubleClicked.connect(self.goto_table)
#        self.apri.clicked.connect(self.goto_table)



    def getItem(self, lstItem):
        #   print(self.listWidget.currentItem().text())
        print(lstItem.text())
        print(self.listWidget.currentRow())
        QMessageBox.information(self, "ListWidget", "You clicked: " + lstItem.text())

    def load_tables(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        # Generazione del cursore
        cursore = db.cursor()
        query = "show tables"
        cursore.execute(query)
        result = cursore.fetchall()

        for row in result:
            self.listWidget.addItem(row[0])

    def goto_operazioni(self):
        op = Operazioni()
        self.window().close()
        self.widget.addWidget(op)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_gestione_clienti(self):
        gestione_clienti = GestioneClienti()
        self.window().close()
        self.widget.addWidget(gestione_clienti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_gestione_dip(self):
        gestione_dip = GestioneDipendenti()
        self.window().close()
        self.widget.addWidget(gestione_dip)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_gestione_cimiteri(self):
        gestione_cimiteri = GestioneCimiteri()
        self.window().close()
        self.widget.addWidget(gestione_cimiteri)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_clienti(self):
        clienti = ClientiScreen()
        self.window().close()
        self.widget.addWidget(clienti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_defunti(self):
        defunti = DefuntiScreen()
        self.window().close()
        self.widget.addWidget(defunti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_dip(self):
        dip = Dipendenti()
        self.window().close()
        self.widget.addWidget(dip)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_cimitero(self):
        cimitero = Cimitero()
        self.window().close()
        self.widget.addWidget(cimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_evento(self):
        evento = Evento()
        self.window().close()
        self.widget.addWidget(evento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_fattura(self):
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
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

    def goto_assegnamento(self):
        assegnamento = Assegnamento()
        self.window().close()
        self.widget.addWidget(assegnamento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_servizioaggiuntivo(self):
        servizioaggiuntivo = ServizioAggiuntivo()
        self.window().close()
        self.widget.addWidget(servizioaggiuntivo)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_bustapaga(self):
        bustapaga = BustaPaga()
        self.window().close()
        self.widget.addWidget(bustapaga)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_turno(self):
        turno = Turno()
        self.window().close()
        self.widget.addWidget(turno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_assegnamentoturno(self):
        assegnamentoturno = AssegnamentoTurno()
        self.window().close()
        self.widget.addWidget(assegnamentoturno)
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

    def goto_telefonocliente(self):
        telefonocliente = TelefonoCliente()
        self.window().close()
        self.widget.addWidget(telefonocliente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_telefonodipendente(self):
        telefonodipendente = TelefonoDipendente()
        self.window().close()
        self.widget.addWidget(telefonodipendente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_emissionefattura(self):
        emissionefattura = EmissioneFattura()
        self.window().close()
        self.widget.addWidget(emissionefattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_emissionefatturaservizio(self):
        emissionefatturaservizio = EmissioneFatturaServizio()
        self.window().close()
        self.widget.addWidget(emissionefatturaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # apre la tabella selezionata dalla lista
    def goto_table(self):
        try:
            if self.listWidget.currentItem().text() == "cliente":
                self.goto_clienti()
            elif self.listWidget.currentItem().text() == "defunto":
                self.goto_defunti()
            elif self.listWidget.currentItem().text() == "dipendente":
                self.goto_dip()
            elif self.listWidget.currentItem().text() == "cimitero":
                self.goto_cimitero()
            elif self.listWidget.currentItem().text() == "evento":
                self.goto_evento()
            elif self.listWidget.currentItem().text() == "fattura":
                self.goto_fattura()
            elif self.listWidget.currentItem().text() == "manutenzione":
                self.goto_manutenzione()
            elif self.listWidget.currentItem().text() == "aggiuntaservizio":
                self.goto_aggiuntaservizio()
            elif self.listWidget.currentItem().text() == "assegnamento":
                self.goto_assegnamento()
            elif self.listWidget.currentItem().text() == "bustapaga":
                self.goto_bustapaga()
            elif self.listWidget.currentItem().text() == "servizioaggiuntivo":
                self.goto_servizioaggiuntivo()
            elif self.listWidget.currentItem().text() == "turno":
                self.goto_turno()
            elif self.listWidget.currentItem().text() == "assegnamentoturno":
                self.goto_assegnamentoturno()
            elif self.listWidget.currentItem().text() == "associazionecimitero":
                self.goto_associazionecimitero()
            elif self.listWidget.currentItem().text() == "associazionelapidi":
                self.goto_associazionelapidi()
            elif self.listWidget.currentItem().text() == "telefonocliente":
                self.goto_telefonocliente()
            elif self.listWidget.currentItem().text() == "telefonodipendente":
                self.goto_telefonodipendente()
            elif self.listWidget.currentItem().text() == "emissionefattura":
                self.goto_emissionefattura()
            elif self.listWidget.currentItem().text() == "emissionefatturaservizio":
                self.goto_emissionefatturaservizio()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una tabella da aprire.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from login.LoginScreen import LoginScreen
        login = LoginScreen()
        self.window().close()
        self.widget.addWidget(login)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)


