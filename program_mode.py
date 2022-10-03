from PySide6 import QtCore, QtGui
from ui_prog_mode_wid import Ui_Form


class ProgWidget(QWidget):
    delete = Signal(int)

    def __init__(self, id_widget: int, val_list: list, parent=None):
        super(ProgWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.id_widget = id_widget
        self.ui.groupBox.setTitle(str(id_widget))
        self.ui.pushButton.clicked.connect(self.press_del)

        self.val_list = val_list

        try:
            self.ui.lineEdit_2.setText(val_list[0])
            self.ui.lineEdit_3.setText(val_list[1])
            self.ui.lineEdit_4.setText(val_list[2])
            self.ui.lineEdit_5.setText(val_list[3])
            self.ui.lineEdit.setText(val_list[4])
            self.ui.comboBox.setCurrentIndex(val_list[5])
        except Exception:
            pass

        self.output_t = QtCore.QTimer()
        self.output_t.setInterval(500)
        self.output_t.timeout.connect(self.widget_out)
        self.output_t.start()

    @Slot()
    def press_del(self):
        self.delete.emit(self.id_widget)

    @Slot()
    def widget_out(self):
        self.val_list = [self.ui.lineEdit_2.text(),  # 0 speed
                         self.ui.lineEdit_3.text(),  # 1 ac
                         self.ui.lineEdit_4.text(),  # 2 pos
                         self.ui.lineEdit_5.text(),  # 3 ampl
                         self.ui.lineEdit.text(),  # 4 time
                         self.ui.comboBox.currentIndex()]  # 5 mode

        if str(self.ui.comboBox.currentIndex()) == '0':

            self.ui.lineEdit_2.show()
            self.ui.lineEdit_3.show()
            self.ui.lineEdit_4.hide()
            self.ui.lineEdit_5.hide()

            self.ui.label_8.hide()
            self.ui.label_9.hide()
            self.ui.label_10.hide()
            self.ui.label_11.hide()

            self.ui.label_4.show()
            self.ui.label_5.show()
            self.ui.label_6.show()
            self.ui.label_7.show()

        elif str(self.ui.comboBox.currentIndex()) == '1':

            self.ui.lineEdit_2.show()
            self.ui.lineEdit_3.show()
            self.ui.lineEdit_4.show()
            self.ui.lineEdit_5.hide()

            self.ui.label_10.hide()
            self.ui.label_11.hide()

            self.ui.label_4.show()
            self.ui.label_5.show()
            self.ui.label_6.show()
            self.ui.label_7.show()

            self.ui.label_8.show()
            self.ui.label_9.show()

        elif str(self.ui.comboBox.currentIndex()) == '2':

            self.ui.lineEdit_2.show()
            self.ui.lineEdit_3.show()
            self.ui.lineEdit_4.hide()
            self.ui.lineEdit_5.show()

            self.ui.label_8.hide()
            self.ui.label_9.hide()

            self.ui.label_4.show()
            self.ui.label_5.show()
            self.ui.label_6.show()
            self.ui.label_7.show()

            self.ui.label_10.show()
            self.ui.label_11.show()

        elif str(self.ui.comboBox.currentIndex()) == '3':
            self.ui.lineEdit_2.hide()
            self.ui.lineEdit_3.hide()
            self.ui.lineEdit_4.hide()
            self.ui.lineEdit_5.hide()

            self.ui.label_8.hide()
            self.ui.label_9.hide()
            self.ui.label_10.hide()
            self.ui.label_11.hide()

            self.ui.label_4.hide()
            self.ui.label_5.hide()
            self.ui.label_6.hide()
            self.ui.label_7.hide()
