# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jayma\OneDrive\Documents\GitHub\JugglingGUI\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from bs4 import BeautifulSoup
import webbrowser
import requests

links = {}
tricks = list()
htmllinks = list()
number_of_tricks = 177
menu_choice = 0
web = requests.get("http://libraryofjuggling.com/Home.html")
soup = BeautifulSoup(web.text,"html.parser")
def loadTricks(soup,web):
    unwanted_menu = 0
    counter = 0
    #Loop through anchor tags in website, limited to 177 to stop from including extraneous links
    #Starts at 3 for this reason also
    for names in soup.find_all('a',limit = number_of_tricks):
        unwanted_menu += 1
        if(unwanted_menu > 3):
        #Can use these lists later
         tricks.append(names.string)
         htmllinks.append(names.get('href'))
         links.update({tricks[counter] : htmllinks[counter]})
         counter += 1
        else:
            continue

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(635, 514)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addTo = QtWidgets.QPushButton(self.centralwidget)
        self.addTo.setGeometry(QtCore.QRect(190, 250, 141, 41))
        self.addTo.setObjectName("addTo")
        self.removefrom = QtWidgets.QPushButton(self.centralwidget)
        self.removefrom.setGeometry(QtCore.QRect(190, 310, 141, 41))
        self.removefrom.setObjectName("removefrom")
        self.goTo = QtWidgets.QPushButton(self.centralwidget)
        self.goTo.setGeometry(QtCore.QRect(190, 370, 141, 41))
        self.goTo.setObjectName("goTo")
        self.catalog = QtWidgets.QListWidget(self.centralwidget)
        self.catalog.setGeometry(QtCore.QRect(350, 250, 261, 221))
        self.catalog.setObjectName("catalog")
        self.trickList = QtWidgets.QListWidget(self.centralwidget)
        self.trickList.setGeometry(QtCore.QRect(20, 30, 151, 441))
        self.trickList.setObjectName("trickList")
        self.jugglingGif = QtWidgets.QLabel(self.centralwidget)
        self.jugglingGif.setGeometry(QtCore.QRect(250, 30, 361, 181))
        self.jugglingGif.setFrameShape(QtWidgets.QFrame.Box)
        self.jugglingGif.setText("")
        self.jugglingGif.setObjectName("jugglingGif")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 635, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.addTo.clicked.connect(self.add_to_catalog)
        self.removefrom.clicked.connect(self.remove_from_catalog)
        self.goTo.clicked.connect(self.go_to_webpage)
         
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addTo.setText(_translate("MainWindow", "Add to Catalog"))
        self.goTo.setText(_translate("MainWindow", "View trick in browser"))
        self.removefrom.setText(_translate("MainWindow", "Remove from Catalog"))
    def loadList(self):
        loadTricks(soup,web)
        for i in range(len(tricks)):
            self.trickList.addItem(tricks[i])

    def add_to_catalog(self,item):
        value = self.trickList.currentItem()
        try:
            text = value.text()
        except AttributeError:
            print('Please select an item to add to the catalog!')
            return
        self.catalog.addItem(text)
        with open("catalog.txt","a+") as stored:
            stored.writelines('%s\n'%text)

    def remove_from_catalog(self):
        value = self.catalog.selectedItems()
        #if not value: return
        for item in value:
            self.catalog.takeItem(self.catalog.row(item))
        with open('catalog.txt','w+') as stored:
            for x in range(self.catalog.count()):
                word = self.catalog.item(x)
                newtext = str(word.text())
                stored.write('%s\n'%(newtext))
                    
    def loadCatalog(self):
        with open('catalog.txt','r') as stored:
            self.catalog.addItems(stored)

    def go_to_webpage(self):
        value = self.catalog.currentItem()
        try:
            text = value.text()
        except AttributeError:
            print('Select an item from the catalog to view in your browser!')
            return
        website = links.get(text.replace('\n',''))
        webbrowser.open_new('http://libraryofjuggling.com/%s'%website)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.loadList()
    ui.loadCatalog()
    MainWindow.show()
    sys.exit(app.exec_())
