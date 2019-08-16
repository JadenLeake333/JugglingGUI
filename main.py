# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\jayma\OneDrive\Documents\GitHub\JugglingGUI\GUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QMovie
import regex as re
from tricks import listing as lists
import os
import webbrowser
import requests

links = {}
tricks = list()
updating_list = list()
updating_tricklist = list()
number_of_tricks = 177
menu_choice = 0
alist = lists.tricks_list
alist.sort()
updating_tricklist = lists.tricks_list
updating_tricklist.sort()
blist = lists.tricks_dict

    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(635, 635)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addTo = QtWidgets.QPushButton(self.centralwidget)
        self.addTo.setGeometry(QtCore.QRect(195, 390, 141, 41))
        self.addTo.setObjectName("addTo")
        self.removefrom = QtWidgets.QPushButton(self.centralwidget)
        self.removefrom.setGeometry(QtCore.QRect(195, 460, 141, 41))
        self.removefrom.setObjectName("removefrom")
        self.goTo = QtWidgets.QPushButton(self.centralwidget)
        self.goTo.setGeometry(QtCore.QRect(195, 530, 141, 41))
        self.goTo.setObjectName("goTo")
        self.catalog = QtWidgets.QListWidget(self.centralwidget)
        self.catalog.setGeometry(QtCore.QRect(350, 380, 261, 231))
        self.catalog.setObjectName("catalog")
        self.trickList = QtWidgets.QListWidget(self.centralwidget)
        self.trickList.setGeometry(QtCore.QRect(20, 10, 161, 601))
        self.trickList.setObjectName("trickList")
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(20, 590, 161, 21))
        self.searchBar.setObjectName("searchBar")
        self.jugglingGif = QtWidgets.QLabel(self.centralwidget)
        self.jugglingGif.setGeometry(QtCore.QRect(235, 10, 375, 360))
        self.jugglingGif.setFrameShape(QtWidgets.QFrame.Box)
        self.jugglingGif.setText("")
        self.jugglingGif.setObjectName("jugglingGif")
        self.movie = QMovie('JugglingGIF.gif')
        self.jugglingGif.setMovie(self.movie)
        self.movie.start()
        self.searchBar.textChanged.connect(self.search)
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

    def search(self):
          current_text = self.searchBar.text()
          self.trickList.clear()
          for i in updating_tricklist:
               if re.search(current_text.upper(),i.upper()):
                    self.trickList.addItem(i)
               if current_text == "":
                    self.loadList()

    def loadList(self):
        updating_tricklist.sort()
        self.trickList.clear()
        self.trickList.addItems(updating_tricklist)

    def add_to_catalog(self,item):
        value = self.trickList.currentItem()
        remove = self.trickList.selectedItems()
        try:
            text = value.text()
        except AttributeError:
            popup = QMessageBox()
            popup.setText('Please select a value to add to the catalog!')
            popup.exec()
            return
        if text not in updating_list:
            self.catalog.addItem(text)
            self.write_to_txt(text)
            updating_list.append(text.replace('\n',""))
            updating_tricklist.remove(text.replace('\n',''))
        #Removes the selected item from the tricklist while adding it to the catalog
        for i in remove:
            self.trickList.takeItem(self.trickList.row(i))
        self.loadList()
    #Funtction to remove any items from the catalog#     
    def remove_from_catalog(self):
        value = self.catalog.selectedItems()
        #if not value: return
        for items in value:
            updating_list.remove(items.text().replace('\n',''))
            updating_tricklist.append(items.text().replace('\n',''))
            print(updating_list)
            print(updating_tricklist)
        for item in value:
            self.catalog.takeItem(self.catalog.row(item))
        self.loadList()
        with open('catalog.txt','w+') as stored:
            for x in range(self.catalog.count()):
                word = self.catalog.item(x)
                text = (str(word.text()))
                self.write_to_txt(text)    
                  
    def loadCatalog(self):
        updating_list.sort()
        self.catalog.addItems(updating_list)

    def load_saved_list(self):
        with open('catalog.txt','r') as stored:
            text = stored.readlines()
            for i in text:
                updating_list.append(i.replace('\n',''))
                updating_tricklist.remove(i.replace('\n',''))        
        print(updating_list)
        print(updating_tricklist)

    def write_to_txt(self,text):
        with open('catalog.txt','a+') as files:
            files.writelines('%s\n'%text)
            
    def create_catalog(self):
        if os.path.exists('catalog.txt'):
            return
        else:
            catalogs = open('catalog.txt','w+')
            print('created')
 
    def go_to_webpage(self):
        value = self.trickList.currentItem()
        try:
            text = value.text()
        except AttributeError as err:
            if err:
                try:
                    value = self.catalog.currentItem()
                    text = value.text()
                except AttributeError:
                    popup = QMessageBox()
                    popup.setText('Please select an item!')
                    popup.exec()
                    return
        website = blist.get(text.replace('\n',''))
        webbrowser.open_new('http://libraryofjuggling.com/%s'%website)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    ui.create_catalog()
    ui.load_saved_list()
    ui.loadList()
    ui.loadCatalog()
    MainWindow.show()
    sys.exit(app.exec_())
   
                