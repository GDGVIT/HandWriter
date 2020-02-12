# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parser.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


import sys
import os
import re

sys.path.insert(1, os.path.join('.', 'src'))
from document_parser import DocumentParser

from PyQt5 import QtCore, QtGui, QtWidgets
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import joblib

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("Handwriting Parser")
        self.MainWindow.setStyleSheet("QMainWindow {background: 'white'}")
        self.MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        self.gridLayout.setContentsMargins(100, 10, 100, 10)
        DSC_logo = QtWidgets.QLabel(self.centralwidget)
        DSC_logo.setPixmap(QtGui.QPixmap(os.path.join('assets', 'dsc_logo.png')).scaled(100, 50, QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation))
        DSC_logo.setFixedSize(100, 50)
        DSC_logo.setObjectName("DSC_logo")
        
        self.gridLayout.addWidget(DSC_logo, 1, 1, 1, 7, QtCore.Qt.AlignHCenter)
        
        self.stylesheet_select = "color: white; background-color: #2866FF; border: 0; border-radius: 7px;"
        self.stylesheet_inactive = "opacity: 0.3; color: grey; background-color: #e7e7e7; border: 0; border-radius: 7px;"
        self.stylesheet_active = "color: white; background-color: #4CCF40; border: 0; border-radius: 7px;"
        
        self.font_asleep = QtGui.QFont()
        self.font_asleep.setPointSize(12)
        self.font_asleep.setFamily('Roboto')

        self.font_awake = QtGui.QFont('Roboto', 12)
        self.font_awake.setBold(True)
        
        font_select = QtGui.QFont()
        font_select.setPointSize(11)
        font_select.setFamily('Roboto')
        font_select.setBold(True)

        self.btn_select_document = QtWidgets.QPushButton('Select Document', self.centralwidget)
        self.btn_select_document.setStyleSheet(self.stylesheet_select)
        self.btn_select_document.setEnabled(True)
        self.btn_select_document.setFixedSize(150, 50)
        self.btn_select_document.setFont(font_select)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.btn_select_document.sizePolicy().hasHeightForWidth())
        #self.btn_select_document.setSizePolicy(sizePolicy)
        #self.btn_select_document.setCheckable(False)
        #self.btn_select_document.setAutoRepeat(False)
        #self.btn_select_document.setAutoExclusive(False)
        #self.btn_select_document.setAutoDefault(False)
        #self.btn_select_document.setDefault(False)
        #self.btn_select_document.setFlat(False)
        #self.btn_select_document.setObjectName("Select Document")
        self.gridLayout.addWidget(self.btn_select_document, 2, 1, 1, 5, QtCore.Qt.AlignHCenter)
        self.MainWindow.setCentralWidget(self.centralwidget)

        
        self.btn_parse_document = QtWidgets.QPushButton('Parse!', self.centralwidget)
        self.btn_parse_document.setEnabled(False)
        self.btn_parse_document.setFixedSize(150, 50)
        self.btn_parse_document.setFont(self.font_asleep)
        self.btn_parse_document.setStyleSheet(self.stylesheet_inactive)
        self.gridLayout.addWidget(self.btn_parse_document, 2, 3, 1, 5, QtCore.Qt.AlignHCenter)
        #self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "Handwriting Parser"))
        #self.btn_select_document.setText(_translate("MainWindow", "btn_select_document"))
        self.btn_select_document.clicked.connect(self.open_document)
        self.btn_parse_document.clicked.connect(self.parse_document)

    def open_document(self):
        self.doc_path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Open Document')[0]
        if self.doc_path == '':
            return
        try:
            self.document = Document(self.doc_path)
        except PackageNotFoundError:
            print("Incorrect file extension, aborting")
            self.sleep_btn_parse_document()
            return
        self.wake_btn_parse_document()
        
    def parse_document(self):
        CHARS_PER_LINE = 54
        LINES_PER_PAGE = 30
        with open('hashes.pickle', 'rb') as f:
            hashes = joblib.load(f)
        document_parser = DocumentParser(hashes, CHARS_PER_LINE, LINES_PER_PAGE)
        pdf_path = re.sub('docx', 'pdf', self.doc_path)
        document_parser.parse_document(self.document, pdf_path)
        self.sleep_btn_parse_document()

    def wake_btn_parse_document(self):
        self.btn_parse_document.setEnabled(True)
        self.btn_parse_document.setStyleSheet(self.stylesheet_active)
        self.btn_parse_document.setFont(self.font_awake)

    def sleep_btn_parse_document(self):
        self.btn_parse_document.setEnabled(False)
        self.btn_parse_document.setStyleSheet(self.stylesheet_inactive)
        self.btn_parse_document.setFont(self.font_asleep)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Styles = ['Breeze', 'Oxygen', 'QtCurve', 'Windows', 'Fusion']
    app.setStyle(Styles[4])
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
