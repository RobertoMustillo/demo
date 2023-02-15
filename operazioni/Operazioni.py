from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QHeaderView

import mysql.connector



class Operazioni(QDialog):
    def __init__(self):
        super(Operazioni, self).__init__()
        loadUi("operazioni/vista_operazioni2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        #self.tableWidget.setHorizontalHeaderLabels(["CodDipendente","Cognome", "Nome", "Ore"])
        self.tableWidget.setColumnWidth(0, 130)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.image.setPixmap(QPixmap('sfondo.png'))


        #self.tableWidget.resizeColumnsToContents()
        self.carica.clicked.connect(self.loaddata)
        self.listWidget.itemDoubleClicked.connect(self.loaddata)
        self.btnCancella.clicked.connect(self.cancella)
        self.btnEsci.clicked.connect(self.funz_esci)

        self.widget = QtWidgets.QStackedWidget()

    def loaddata(self):
        try:
            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )

            #non lho fatta
           # q35 = "SELECT c.Nome, count(d.CodDefunto) as NumDefunti, (SELECT COUNT(defunto.CodDefunto) FROM defunto WHERE Cimitero=c.Nome) as PostiTotali" \
            #      "FROM cimitero c, defunto d" \
             #     "WHERE d.Cimitero = c.Nome and d.LuogoNascita=d.Cimitero GROUP BY c.Nome;"
            # Generazione del cursore
            cursore = db.cursor()
            if self.listWidget.currentRow() == 0:

                self.cancella()
                self.tableWidget.setColumnCount(4)
                self.tableWidget.setHorizontalHeaderLabels(["CodDipendente","Cognome", "Nome", "Ore"])
                query21 = "SELECT d.CodDipendente, d.Cognome, d.Nome, sum(TIMESTAMPDIFF(Hour, t.OraInizio, t.OraFine)) " \
                        "FROM dipendente d, turno t, assegnamentoturno ast " \
                        "WHERE d.CodDipendente = ast.Dipendente and ast.Turno = t.CodTurno and t.Data between '2020-01-01' and '2020-01-03'" \
                        "group by d.CodDipendente;"
                cursore.execute(query21)
                result = cursore.fetchall()
                tablerow = 0
                # results = cursore.execute(query)
                self.tableWidget.setRowCount(len(result))

                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                    tablerow += 1
               # self.tableWidget.resizeColumnsTo()
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


            elif self.listWidget.currentRow() == 1:

                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["Anno","Entrate Annuali"])
                query24 ="SELECT YEAR(f.DataEmissione) as Anno , SUM(f.TotaleFattura) as EntrateAnnuali FROM fattura f " \
                         "WHERE f.DataPagamento IS NOT null " \
                         "GROUP BY YEAR(f.DataEmissione);"
                cursore.execute(query24)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1
                    self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


            elif self.listWidget.currentRow() == 2:

                query29 = "SELECT d.Cimitero, em.CanoneAnnuo, YEAR(f.DataEmissione) as Anno " \
                          "FROM emissionefattura em , evento e, defunto d, fattura f " \
                          "WHERE em.Evento=e.CodEvento and e.Defunto=d.CodDefunto and em.Fattura=f.NumeroFattura ORDER BY d.Cimitero, Anno;"
                self.cancella()
                self.tableWidget.setColumnCount(3)

                self.tableWidget.setHorizontalHeaderLabels(["Cimitero", "Canone Annuo", "Anno "])
                cursore.execute(query29)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


            elif self.listWidget.currentRow() == 3:

                q30 ="SELECT COUNT(CodDefunto) as NumeroDefunti, year(DataDecesso) as Anno FROM defunto " \
                     "GROUP BY year(DataDecesso);"
                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["NumeroDefunti", "Anno"])
                cursore.execute(q30)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1

                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 4:
                q31 ="SELECT year(DataDecesso) as AnnoDecesso, COUNT(d.CodDefunto) as NumeroDefunti, avg((TIMESTAMPDIFF(YEAR, d.DataNascita, d.DataDecesso))) as EtaMediaDiMorte " \
                     "FROM defunto d " \
                     "GROUP BY year(DataDecesso);"

                self.cancella()
                self.tableWidget.setColumnCount(3)

                self.tableWidget.setHorizontalHeaderLabels(["Anno Decesso", "Numero Defunti", "Eta Media Di Morte"])
                cursore.execute(q31)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(int(row[2]))))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 5:
                q32="SELECT year(DataAllaccio) as Anno, COUNT(CodEvento) as NumAllacci FROM evento " \
                    "GROUP BY year(DataAllaccio);"
                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["Anno", "Numero Allacci"])
                cursore.execute(q32)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 6:
                q33="SELECT year(DataDistacco) as Anno, COUNT(CodEvento) as NumDistacchi FROM evento " \
                    "WHERE DataDistacco is not null " \
                    "GROUP BY year(DataDistacco);"
                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["Anno", "Numero Distacchi"])
                cursore.execute(q33)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 7:
                q34 ="SELECT COUNT(CodEvento) as NumAllacciTot, COUNT(DataDistacco) as NumDistacchiTot FROM evento;"
                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["Numero Allacci Totali", "Numero Distacchi Totali"])
                cursore.execute(q34)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 8:
                q37="SELECT CodDefunto, Nome, Cognome " \
                    "FROM defunto " \
                    "WHERE CodDefunto not in(SELECT CodDefunto " \
                        "FROM defunto d join evento e WHERE d.CodDefunto = e.Defunto and e.DataDistacco is null);"
                self.cancella()
                self.tableWidget.setColumnCount(3)

                self.tableWidget.setHorizontalHeaderLabels(["CodDefunto", "Nome", "Cognome"])
                cursore.execute(q37)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 9:
                q40="SELECT year(DataPianificazione) AS Anno,COUNT(CodManutenzione) as NumeroManutenzioni, Tipo " \
                    "FROM manutenzione m" \
                    " GROUP BY Tipo, year(DataPianificazione)" \
                    " ORDER BY year(DataPianificazione);"
                self.cancella()
                self.tableWidget.setColumnCount(3)

                self.tableWidget.setHorizontalHeaderLabels(["Anno", "NumeroManutenzioni", "Tipo"])
                cursore.execute(q40)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 10:
                q41="SELECT SUM(s.Prezzo) as PrezzoTotaleServizi, s.Tipo FROM aggiuntaservizio a, servizioaggiuntivo s WHERE a.ServizioAggiuntivo = s.Tipo" \
                    " GROUP BY s.Tipo;"
                self.cancella()
                self.tableWidget.setColumnCount(2)

                self.tableWidget.setHorizontalHeaderLabels(["Ricavi dei Servizi", "Tipo"])
                cursore.execute(q41)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 11:
                q42="SELECT DISTINCT c.CodCliente,c.Cognome, f.NumeroFattura,f.DataScadenza,f.TotaleFattura" \
                    " FROM fattura f, emissionefattura em, evento e, cliente c" \
                    " WHERE f.DataPagamento is null and f.NumeroFattura=em.Fattura and e.CodEvento=em.Evento and e.Cliente = c.CodCliente;"
                self.cancella()
                self.tableWidget.setColumnCount(5)

                self.tableWidget.setHorizontalHeaderLabels(["CodCliente", "Cognome","Num Fattura","Data Scadenza","Importo"])
                cursore.execute(q42)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3].strftime('%d/%m/%Y')))
                    self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            elif self.listWidget.currentRow() == 12:
                q43="SELECT d.CodDefunto, d.Cognome, d.Nome, e.DataAllaccio, e.DataDistacco, e1.DataAllaccio as DataRiallaccio" \
                    " FROM defunto d, evento e, evento e1" \
                    " WHERE e.Defunto=d.CodDefunto and e.DataDistacco IS NOT null and e1.DataDistacco is null and e1.Defunto=d.CodDefunto" \
                    " ORDER BY CodDefunto;"
                self.cancella()
                self.tableWidget.setColumnCount(6)

                self.tableWidget.setHorizontalHeaderLabels(["CodDefunto", "Cognome", "Num Fattura", "DataAllaccio", "DataDistacco", "DataRiallaccio"])
                cursore.execute(q43)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                    self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                    self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3].strftime('%d/%m/%Y')))
                    self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4].strftime('%d/%m/%Y')))
                    self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5].strftime('%d/%m/%Y')))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


            elif self.listWidget.currentRow() == 13:
                q44="SELECT SUM(fattura.TotaleFattura) as EntrateTotali FROM fattura;"
                self.cancella()
                self.tableWidget.setColumnCount(1)

                self.tableWidget.setHorizontalHeaderLabels(["EntrateTotali"])
                cursore.execute(q44)
                result = cursore.fetchall()
                tablerow = 0
                self.tableWidget.setRowCount(len(result))
                for row in result:
                    self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                    tablerow += 1
                self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            else:
                QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un operazione.', QMessageBox.Ok,
                                     QMessageBox.Ok)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un operazione.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def cancella(self):
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

    def funz_esci(self):
        from home.Home import Home
        home = Home()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)