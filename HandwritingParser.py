import sys
import os
import re

sys.path.insert(1, os.path.join('.', 'src'))
from document_parser import DocumentParser

from PyQt5 import QtCore, QtGui, QtWidgets
from docx import Document
from docx.opc.exceptions import PackageNotFoundError
import joblib

class Ui_MainWindow(QtCore.QObject):

    def setupUi(self, MainWindow):
        ### Styles for appliction UI elements

        ## Stylesheets

        # 'Select Document' button
        self.stylesheet_select = """
        QPushButton {
            color: white; 
            background-color: #4086F6; 
            border: 0; 
            border-radius: 7px;
        }
        QPushButton:pressed {
            color: white;
            background-color: #3A80F0;
            border: 0;
            border-radius: 7px;
        }
        """

        # 'Write' inactive
        self.stylesheet_write_inactive = "opacity: 0.3; color: grey; background-color: #e7e7e7; border: 0; border-radius: 7px;"
        
        # 'Write' active
        self.stylesheet_write_active = """
        QPushButton {
            color: white; 
            background-color: #109D58; 
            border: 0; 
            border-radius: 7px;
        }
        QPushButton:pressed {
            color: white;
            background-color: #0A9852;
            border: 0;
            border-radius: 7px;
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

        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("HandWriter")
        self.MainWindow.setStyleSheet("QMainWindow {background: 'white'}")
        self.MainWindow.setFixedSize(800, 600)
        self.MainWindow.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)    # Disable window maximize button
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.MainWindow.setCentralWidget(self.centralwidget)

        # Animated DSC Logo

        self.logo_label = QtWidgets.QLabel(self.centralwidget)
        self.logo_label.resize(200, 80)
        self.logo_label.move(300, 165)
        # Custom class moviebox resizes QMovie to desired width (pixels):
        self.logo_movie = MovieBox("assets/DSC_logo_animated.gif").resized_movie(200)
        self.logo_movie.setSpeed(350)
        self.logo_movie.frameChanged.connect(self.check_stopping_frame)
        self.logo_label.setMovie(self.logo_movie)
        self.logo_movie.start()

        # Application name logo

        app_logo = QtWidgets.QLabel(self.centralwidget)
        app_logo.setPixmap(QtGui.QPixmap(os.path.join('assets', 'HR_UI.png')).scaled(300, 150, QtCore.Qt.KeepAspectRatio, transformMode = QtCore.Qt.SmoothTransformation))
        app_logo.setFixedSize(300, 150)
        app_logo.setObjectName("app_logo")
        app_logo.setGeometry(250, 225, 300, 150)

        # Select Document Button

        self.btn_select_document = QtWidgets.QPushButton('Select Document', self.centralwidget)
        self.btn_select_document.setStyleSheet(self.stylesheet_select)
        self.btn_select_document.setEnabled(True)
        self.btn_select_document.setFixedSize(150, 50)
        self.btn_select_document.setFont(font_select)
        self.btn_select_document.setShortcut('Ctrl+O')
        self.btn_select_document.setGeometry(235, 395, 150, 50)

        # Write Button
        
        self.btn_write = QtWidgets.QPushButton('Write', self.centralwidget)
        self.btn_write.setEnabled(False)
        self.btn_write.setFixedSize(150, 50)
        self.btn_write.setFont(self.font_asleep)
        self.btn_write.setStyleSheet(self.stylesheet_write_inactive)
        self.btn_write.setShortcut('Ctrl+E')
        self.btn_write.setGeometry(415, 395, 150, 50)

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
        self.doc_path = QtWidgets.QFileDialog.getOpenFileName(self.MainWindow, 'Open Document', filter = '*.docx')[0]
        if self.doc_path == '':
            self.sleep_btn_write()
            return
        try:
            self.document = Document(self.doc_path)
        except PackageNotFoundError:
            self.sleep_btn_write()
            return
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
        self.thread = ParserThread(self.doc_path, self.document)
        self.thread.change_value.connect(self.stop_progressbar)
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
    

    def wake_btn_write(self):
        self.btn_write.setEnabled(True)
        self.btn_write.setStyleSheet(self.stylesheet_write_active)
        self.btn_write.setFont(self.font_awake)

    def sleep_btn_write(self):
        self.btn_write.setEnabled(False)
        self.btn_write.setStyleSheet(self.stylesheet_write_inactive)
        self.btn_write.setFont(self.font_asleep)

    def check_stopping_frame(self):
        if self.logo_movie.currentFrameNumber() == 110: # 110 - Frame where DSC logo completes
            self.logo_movie.stop()

# Thread class for executing application logic separate from main UI thread            
class ParserThread(QtCore.QThread):
    def __init__(self, doc_path, document):
        super(ParserThread, self).__init__()
        self.doc_path = doc_path
        self.document = document

    change_value = QtCore.pyqtSignal()

    def run(self):
        CHARS_PER_LINE = 54
        LINES_PER_PAGE = 30
        with open('hashes.pickle', 'rb') as f:
            hashes = joblib.load(f)
        document_parser = DocumentParser(hashes, CHARS_PER_LINE, LINES_PER_PAGE)
        pdf_path = re.sub('docx', 'pdf', self.doc_path)
        
        document_parser.parse_document(self.document, pdf_path)
        self.change_value.emit()

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