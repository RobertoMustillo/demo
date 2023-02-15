import mysql
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaDefunto(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaDefunto, self).__init__()
        loadUi("defunti/modificadefunto.ui",self)
        self.elemento_selezionato = elemento_selezionato  #riga del cliente selezionato (che parte da 0)!!
        #print("riga cliente sel: ")
        #print(self.cliente_selezionato)
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

        self.widget = QtWidgets.QStackedWidget()

        # Test di connessione a MySQL
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )
        self.cursore = self.db.cursor()
        query = "SELECT Nome FROM `db_illuminazione_votiva`.`cimitero`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo le chiavi esterne alla comboBox
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.comboBox.addItems(self.codici)

    def modifica_elemento(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        nome = self.nome.text()
        cognome = self.cognome.text()
        dataN = self.dateN.date().toString("yyyy-MM-dd")
        dataD = self.dateD.date().toString("yyyy-MM-dd")
        luogon = self.luogon.text()
        cimitero = self.comboBox.currentText()
        ubicazione = self.ubicazione.text()

        # Generazione del cursore
        cursore = db.cursor()
        # cerco l'ID del cliente selezionato
        query = "select * from defunto"
        cursore.execute(query)
        result = cursore.fetchall()

        # creo un array di codici
        self.codici = []
        for x in result:
            self.codici.append(x[0])

        # prendo il codice cliente selezionato
        codice_sel = self.codici[self.elemento_selezionato]
        #print(codiceClienteSel)
        query2= "UPDATE `defunto` SET `Cognome` = '"+cognome+"', `Nome` = '"+nome+"', `DataNascita` = '"+dataN+"', `DataDecesso` = '"+dataD+"', `LuogoNascita` = '"+luogon+"', `Cimitero` = '"+cimitero+"', `Ubicazione` = '"+ubicazione+"' WHERE `CodDefunto` = "+codice_sel.__str__()+";"
        cursore.execute(query2)
        db.commit()
        self.funz_esci()


    def funz_esci(self):
        from defunti.DefuntiScreen import DefuntiScreen
        defunto = DefuntiScreen()
        self.window().close()
        self.widget.addWidget(defunto)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)