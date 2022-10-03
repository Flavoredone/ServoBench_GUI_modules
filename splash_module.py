import sys
import json
import math

from main_window import MainWindow
from PySide6 import QtCore, QtGui
from ui_startup import Ui_SplashScreen


class SplashScreen(QMainWindow):
    open_fl: bool

    def __init__(self):
        global user_nm

        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        ##################################################################

        self.ui.pushButton.setIcon(QIcon('startup.png'))

        ##################################################################

        self.ui.pushButton_2.clicked.connect(self.close_splash)
        self.ui.pushButton_4.clicked.connect(self.splash_serial)
        self.ui.pushButton_3.clicked.connect(self.close_app)

        with open('ip_port.json', 'r') as file:
            data = json.load(file)
            self.ui.lineEdit_5.setText(data['PC_IP'])
            self.ui.lineEdit_4.setText(str(data['PC_PORT']))
            self.ui.lineEdit.setText(data["CNTR_IP"])
            self.ui.lineEdit_2.setText(str(data["CNTR_PORT"]))

        self.show()

    @QtCore.Slot()
    def close_splash(self):
        global user_nm

        self.ui.pushButton_4.click()

        try:

            if self.open_fl:

                user_nm = str(self.ui.lineEdit.text())

                self.main = MainWindow()
                self.main.show()
                self.close()

            else:
                self.ui.label_5.setText('Неуспешное подключение')
                self.ui.label_5.setStyleSheet('color: red; font-size: 18px;')
        except Exception:
            pass

    @QtCore.Slot()
    def close_app(self):
        sys.exit(app.exec())

    @QtCore.Slot()
    def splash_serial(self):
        global SERVER_HOST, SERVER_PORT, CONTROLLER_HOST, CONTROLLER_PORT

        SERVER_HOST = str(self.ui.lineEdit_5.text())
        SERVER_PORT = int(self.ui.lineEdit_4.text())

        CONTROLLER_HOST = str(self.ui.lineEdit.text())
        CONTROLLER_PORT = int(self.ui.lineEdit_2.text())

        ip_dict = {"PC_IP": SERVER_HOST,
                   "PC_PORT": SERVER_PORT,
                   "CNTR_IP": CONTROLLER_HOST,
                   "CNTR_PORT": CONTROLLER_PORT
                   }

        try:
            self.ui.lineEdit_3.setText(str(communicate_with_lm(b"AA[6]\r"))[9:-2])
            with open('ip_port.json', 'w') as file:
                json.dump(ip_dict, file, indent=3)
        except Exception:
            self.ui.label_5.setText('Неуспешное подключение')
            self.ui.label_5.setStyleSheet('color: red; font-size: 18px;')

        with open('config.json', 'r') as file:
            data = json.load(file)
            ser_list = data['ser_nums'].get('0')

            if str(self.ui.lineEdit_3.text()) in ser_list:
                self.ui.label_5.setText('Серийный номер действителен')
                self.ui.label_5.setStyleSheet('color: green; font-size: 18px;')
                self.open_fl = True
            else:
                self.ui.label_5.setText(' Серийный номер не действителен, либо подкючение неуспешно')
                self.ui.label_5.setStyleSheet('color: red; font-size: 18px;')
                self.open_fl = False
