import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaDipendente(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaDipendente, self).__init__()
        loadUi("dipendenti/modificadip.ui",self)
        self.elemento_selezionato = elemento_selezionato  #riga selezionata (che parte da 0)!!
        #print("riga cliente sel: ")
        #print(self.cliente_selezionato)
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.funz_modifica)

        self.widget = QtWidgets.QStackedWidget()

    def funz_modifica(self):
        try:
            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )

            id = self.id.text()
            nome = self.nome.text()
            cognome = self.cognome.text()
            cf = self.cf.text()
            data = self.dateEdit.date().toString("yyyy-MM-dd")
            email = self.email.text()
            iban = self.iban.text()
            citta = self.citta.text()
            cap = self.cap.text()
            via = self.via.text()
            numerocivico = self.numerocivico.text()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID selezionato
            query = "select * from dipendente"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # prendo il codice selezionato
            codiceSel = self.codici[self.elemento_selezionato]
            query2= "UPDATE `dipendente` SET `CodDipendente` = '"+id+"', `CodiceFiscale` = '"+cf+"', `Cognome` = '"+cognome+"', `Nome` = '"+nome+"', `IBAN` = '"+iban+"', `DataNascita` = '"+data+"', `Email` = '"+email+"', `Citta` = '"+citta+"', `CAP` = '"+cap+"', `Via` = '"+via+"', `NumeroCivico` = '"+numerocivico+"' WHERE CodDipendente = "+codiceSel.__str__()+";"
            cursore.execute(query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, ricontrolla i dati.', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from dipendenti.Dipendenti import Dipendenti
        dipendente = Dipendenti()
        self.window().close()
        self.widget.addWidget(dipendente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)