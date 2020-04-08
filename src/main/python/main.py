import sys
import os
import re
import subprocess
import platform

#sys.path.insert(1, os.path.join('.', 'src'))
from document_parser import DocumentParser

from PyQt5 import QtCore, QtGui, QtWidgets
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
from fbs_runtime.application_context.PyQt5 import ApplicationContext
import joblib

class Ui_MainWindow(QtCore.QObject):

    def setupUi(self, MainWindow, AppContext):
        ### Styles for appliction UI elements

        ## Stylesheets

        # 'Select Document' button
        self.stylesheet_new_select = """
        QPushButton {
            color: white; 
            background-color: #4086F6; 
            border: 0; 
            border-radius: 25px;
        }
        QPushButton:pressed {
            color: white;
            background-color: #3A80F0;
            border: 0;
            border-radius: 25px;
        }
        """
        self.stylesheet_selected ="""
        QPushButton {
            color: #4086F6; 
            background-color: #FFFFFF; 
            border: 2px; 
            border-color: #4086F6;
            border-radius: 25px;
            border-style: solid;
        }
        QPushButton:pressed {
            color: white;
            background-color: #3A80F0;
            border: 2px;
            border-radius: 25px;
        }
        """
        # 'Write' inactive
        self.stylesheet_write_inactive = """
        opacity: 0.3; 
        color: grey; 
        background-color: #e7e7e7; 
        border: 0; 
        border-radius: 25px;
        """
        
        # 'Write' active
        self.stylesheet_write_active = """
        QPushButton {
            color: white; 
            background-color: #4086F6; 
            border: 0; 
            border-radius: 25px;
        }
        QPushButton:pressed {
            color: white;
            background-color: #3A80F0;
            border: 0;
            border-radius: 25px;
        }
        """

        self.stylesheet_busy_progressbar = """
        QProgressBar {
            padding: 3;
            border: 2;
        }

        QProgressBar::chunk {
            background-color: #4086F6;
        }
        """
        
        self.stylesheet_complete_progressbar = """
            QProgressBar {
                padding: 3; 
                border: 2; 
            }
            QProgressBar::chunk {
                background-color: #109D58;
            }
        """

        ## Fonts

        # Write inactive
        self.font_asleep = QtGui.QFont('Roboto', 12)
        
        # Write active
        self.font_awake = QtGui.QFont('Roboto', 12)
        self.font_awake.setBold(True)
        
        # Select
        font_select = QtGui.QFont('Roboto', 11)
        font_select.setBold(True)

        ### UI Elements

        # Main Window

        path_animated_logo = AppContext.get_resource('DSC_logo_animated.gif')
        path_logo_small = AppContext.get_resource('handwriter_logo_small.png')
        path_logo = AppContext.get_resource('handwriter_logo.png')
        self.path_hashes = AppContext.get_resource('hashes.pickle')

        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("HandWriter")
        self.MainWindow.setStyleSheet("QMainWindow {background: 'white'}")
        self.MainWindow.setFixedSize(800, 600)
        self.MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)    # Disable window maximize button
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.MainWindow.setWindowIcon(QtGui.QIcon(path_logo_small))

        # Animated DSC Logo

        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_label.resize(200, 80)
        self.logo_label.move(320, 45)
        # Custom class moviebox resizes QMovie to desired width (pixels):
        self.logo_movie = MovieBox(path_animated_logo).resized_movie(180)
        self.logo_movie.setSpeed(350)
        self.logo_movie.frameChanged.connect(self.check_stopping_frame)
        self.logo_label.setMovie(self.logo_movie)
        self.logo_movie.start()

        # Application name logo

        app_logo = QtWidgets.QLabel(self.centralwidget)
        app_logo.setPixmap(QtGui.QPixmap(path_logo).scaled(540, 100, QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation))
        app_logo.setFixedSize(540, 100)
        app_logo.setObjectName("app_logo")
        app_logo.setGeometry(185, 210, 300, 150)

        # Select Document Button

        self.btn_select_document = QtWidgets.QPushButton('Select Document', self.centralwidget)
        self.btn_select_document.setStyleSheet(self.stylesheet_new_select)
        self.btn_select_document.setEnabled(True)
        self.btn_select_document.setFixedSize(200, 50)
        self.btn_select_document.setFont(font_select)
        self.btn_select_document.setShortcut('Ctrl+O')
        self.btn_select_document.setGeometry(175, 445, 150, 50)

        # Write Button
        
        self.btn_write = QtWidgets.QPushButton('Write', self.centralwidget)
        self.btn_write.setEnabled(False)
        self.btn_write.setFixedSize(200, 50)
        self.btn_write.setFont(self.font_asleep)
        self.btn_write.setStyleSheet(self.stylesheet_write_inactive)
        self.btn_write.setShortcut('Ctrl+E')
        self.btn_write.setGeometry(435, 445, 150, 50)

        # Progress Bar

        self.progress = QtWidgets.QProgressBar(self.MainWindow)
        self.progress.setStyleSheet(self.stylesheet_busy_progressbar)
        self.progress.setGeometry(0, 590, 800, 10)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "HandWriter"))
        self.btn_select_document.clicked.connect(self.open_document)
        self.btn_write.clicked.connect(self.parse_document)

        self.MainWindow.show()


    def open_document(self):
        self.doc_path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Open Document', filter = '*.docx')
        self.doc_path = self.doc_path[0]       
        if self.doc_path == '':
            self.sleep_btn_write()
            self.unselect_btn_select()
            return
        try:
            self.document = Document(self.doc_path)
            self.selected_btn_select()
        except PackageNotFoundError:
            self.sleep_btn_write()
            return
        self.pdf_path = re.sub('docx', 'pdf', self.doc_path)
        self.wake_btn_write()
        
    # Parse document on a thread separate from main UI thread
    def parse_document(self):
        self.progress.setRange(0, 0)
        self.progress.setStyleSheet(self.stylesheet_busy_progressbar)
        self.start_parsing()
    # Uncomment to help with debugging:
#        if self.thread.isRunning():
#            print('Thread started')

    def start_parsing(self):
        self.thread = ParserThread(self.doc_path, self.document, self.path_hashes)
        self.thread.change_value.connect(self.popup_success)
        self.thread.key_exception.connect(self.popup_keyerror)
        self.thread.start()        
        
    def stop_progressbar(self):
        self.thread.requestInterruption()
        self.sleep_btn_write()
        # Uncomment to help with debugging:
#        if self.thread.isFinished():
#            print("Thread terminated")
        self.progress.setRange(0, 1)
        self.progress.setStyleSheet(self.stylesheet_complete_progressbar)
        self.progress.setTextVisible(False)
        self.progress.setValue(1)
        self.unselect_btn_select()
    
    def popup_success(self):
        self.stop_progressbar()
        success_popup = QtWidgets.QMessageBox(self.centralwidget)
        success_popup.setIcon(QtWidgets.QMessageBox.NoIcon)
        success_popup.setWindowTitle('Success: File Written')
        success_popup.setText('The file was successfully written to ' + self.pdf_path)
        btn_open_folder = QtWidgets.QPushButton('Open Containing Folder')
        btn_open_folder.clicked.connect(self.open_containing_folder)
        success_popup.addButton(btn_open_folder, QtWidgets.QMessageBox.AcceptRole)
        success_popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
        success_popup.show()        
    
    def open_containing_folder(self):
        if platform.system() == 'Windows':
            pdf_path = re.search('^(.+)\\([^\\]+)$', self.pdf_path).groups()[0]
            os.startfile(pdf_path)

        elif platform.system() == 'Darwin':
            pdf_path = re.search('^(.+)/([^/]+)$', self.pdf_path).groups()[0]
            subprocess.Popen(['open', pdf_path])
            
        else:
            pdf_path = re.search('^(.+)/([^/]+)$', self.pdf_path).groups()[0]
            subprocess.Popen(['xdg-open', pdf_path])

    def popup_keyerror(self, foreign_char):
        self.stop_progressbar()
        error_popup = QtWidgets.QMessageBox(self.centralwidget)
        error_popup.setIcon(QtWidgets.QMessageBox.Critical)
        error_popup.setWindowTitle('Error: Unable to write character')
        error_popup.setText('The character ' + foreign_char + ' has not been fed into this version of HandWriter. Raise an issue on the official GDGVIT repo')
        error_popup.setStandardButtons(QtWidgets.QMessageBox.Ok)
        error_popup.show()
        
    def wake_btn_write(self):
        self.btn_write.setEnabled(True)
        self.btn_write.setStyleSheet(self.stylesheet_write_active)
        self.btn_write.setFont(self.font_awake)

    def sleep_btn_write(self):
        self.btn_write.setEnabled(False)
        self.btn_write.setStyleSheet(self.stylesheet_write_inactive)
        self.btn_write.setFont(self.font_asleep)

    def unselect_btn_select(self):
        self.btn_select_document.setStyleSheet(self.stylesheet_new_select)
        self.btn_select_document.setText("Select Document")

    def selected_btn_select(self):
        self.btn_select_document.setStyleSheet(self.stylesheet_selected)
        document_name = re.search('[^/]*$', self.doc_path).group()
        self.btn_select_document.setText(document_name)

    def check_stopping_frame(self):
        if self.logo_movie.currentFrameNumber() == 210: # 110 - Frame where DSC logo completes
            self.logo_movie.stop()

# Thread class for executing application logic separate from main UI thread            
class ParserThread(QtCore.QThread):
    def __init__(self, doc_path, document, path_hashes):
        super(ParserThread, self).__init__()
        self.doc_path = doc_path
        self.document = document
        self.HASHES = path_hashes

    change_value = QtCore.pyqtSignal()
    key_exception = QtCore.pyqtSignal(str)
    
    def run(self):
        CHARS_PER_LINE = 54
        LINES_PER_PAGE = 30
        with open(self.HASHES, 'rb') as f:
            hashes = joblib.load(f)
        document_parser = DocumentParser(hashes, CHARS_PER_LINE, LINES_PER_PAGE)
        pdf_path = re.sub('docx', 'pdf', self.doc_path)
        
        try:
            document_parser.parse_document(self.document, pdf_path)
            self.change_value.emit()
        except KeyError as e:
            self.key_exception.emit(str(e)[1])



# Used to return a resized QMovie object
class MovieBox():
    def __init__(self, movie_path):
        self.movie = QtGui.QMovie(movie_path)

    def resized_movie(self, width):
        self.movie.jumpToFrame(0)
        movie_size = self.movie.currentImage().size()
        movie_aspect = movie_size.width() / movie_size.height()

        self.movie.setScaledSize(QtCore.QSize(width, int(width / movie_aspect)))
        return self.movie


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, appctxt)
    MainWindow.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)