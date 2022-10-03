import time
import json
import math

import pyqtgraph as pg

from PySide6 import QtCore, QtGui
from datetime import datetime
from ui_startup import Ui_SplashScreen
from ui_prog_mode_wid import Ui_Form
from sys import argv, executable


class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.y = None
        self.x = None
        self.pr_remain_time = None
        self.val_dict = None
        self.sin_time = None
        self.stoptime = None
        self.timer = None

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.counter_id: int = 0
        self.value_list: list = [0, 0, 0, 0, 0]

    def init_handler(self):
        try:
            self.ui.lineEdit_24.setText(str(user_nm))
            self.ui.lineEdit_25.setText(str(communicate_with_lm(b"AA[6]\r"))[9:-2])

            self.ui.pushButton_3.click()
        except Exception:
            pass

    @QtCore.Slot()
    def update_plot_data(self, tmst, tpxl):

        pen = pg.mkPen(color=(255, 0, 0))

        tmst.append(round(self.x[-1]))
        self.x = self.x[1:]
        self.x.append(float(self.x[-1] + gr_time / 1000))

        tpxl.append(self.y[-1])

        self.y = self.y[1:]
        self.y.append(txl[-1])

        self.graphWidget.plot(self.x, self.y, pen=pen)

    @QtCore.Slot()
    def graph_mixin(self):
        self.multi_axis()

    @QtCore.Slot()
    def multi_axis(self):

        p = self.graphWidget

        p.showAxis('right')
        p.setLabel('right', 'Скорость', units="<font>[]</font>",
                   color='#025b94', **{'font-size': '12pt'})
        p.getAxis('right').setPen(pg.mkPen(color='#025b94', width=3))

        p2 = pg.ViewBox()
        p.scene().addItem(p2)
        p.getAxis('right').linkToView(p2)
        p2.setXLink(p)

        curve2 = pg.PlotCurveItem(pen=pg.mkPen(color='#025b94', width=1))
        p2.addItem(curve2)

    @QtCore.Slot()
    def to_progmode(self):
        if str(self.ui.comboBox.currentText()) == 'Программа':
            self.ui.btn_new.click()

    def save_csv(self, ttpxl=None, ttmst=None):
        csv_list[0] = 'Позиция (' + str(self.ui.comboBox_2.currentText()) + '); Время (с); ' + str(datetime.now())
        csv_list = [
            str([str(scale[int(widgets.comboBox_2.currentIndex())] * x) for x in ttpxl][x]) + "; " + str(ttmst[x])
            for x in range(len(tmst))]
        a = "\n".join(csv_list)
        fname = QFileDialog.getSaveFileName(self, "Сохранить график", "", "Excel (*.csv)")[0]
        f = open(fname, 'w')
        with f:
            f.write(a)
            f.close()

    @QtCore.Slot()
    def stoprun(self):
        try:
            communicate_with_lm(b"SO\r")
            time.sleep(0.1)
            communicate_with_lm(b"MO=0\r")
            self.stoptime1.stop()
        except Exception:
            pass

    @QtCore.Slot()
    def sinus_run(self, sin_var):
        sin_var += 1

        snd = str(
            format(scale_b[int(widgets.comboBox_2.currentIndex())] * math.sin(
                float(widgets.lineEdit_2.text()) * sin_var / 57) * float(widgets.lineEdit_2.text()),
                   '.0f'))

        communicate_with_lm(('JV=' + snd + '\r').encode('utf-8'))
        time.sleep(0.05)
        communicate_with_lm(b"BG\r")

    ##############  mode #########################

    @QtCore.Slot()
    def t_pos_sp(self):
        self.t_pos_speed = QtCore.QTimer()
        self.t_pos_speed.setInterval(int(gr_time / 5))
        self.t_pos_speed.timeout.connect(self.pos_sp)
        self.t_pos_speed.start()

    @QtCore.Slot()
    def pos_sp(self, mst, scale):
        try:
            px = str(communicate_with_lm(b"PX\r"))[6:-2]
            pxl.append(int(px))

            mst.append(mst[-1] + 0.2)

            vx = str(communicate_with_lm(b"VX\r"))[6:-2]
            vxl.append(int(vx))

            ####

            le_p = float(format(scale[int(widgets.comboBox_2.currentIndex())] * float(px), '.2f'))

            le_v = float(format(scale[int(widgets.comboBox_2.currentIndex())] * float(vx), '.2f'))

            ####

            if (str(widgets.comboBox_3.currentText())) == 'Абсолютный':
                self.abs_mode(le_p, le_v)

            elif (str(widgets.comboBox_3.currentText())) == 'Относительный ':
                self.relative_mode(le_p, le_v, rel_a)

            elif (str(widgets.comboBox_3.currentText())) == 'Относительный (0 - 360 град)':
                self.relative_0_360(le_p, le_v, rel_a)

        except Exception:
            self.ui.creditsLabel.setText('Не подключено')
            pass

    ##############  combobox linker ##############

    @QtCore.Slot()
    def rel_active(self):
        global rel_a, rel

        rel_a = pxl[-1]
        rel = 0
        self.ui.comboBox_4.setCurrentIndex(self.ui.comboBox_3.currentIndex())

    ##############  abs rel mode #################

    @QtCore.Slot()
    def abs_mode(self, le_p, le_v):
        global txl

        txl.append(float(le_p))

        self.pos_sp_ui(le_p, le_v)

    @QtCore.Slot()
    def relative_mode(self, le_p, le_v, r, txl):

        relative_p = float(le_p - scale[int(self.ui.comboBox_2.currentIndex())] * r + 0.001)

        txl.append(float(relative_p))

        self.pos_sp_ui(relative_p, le_v)

    @QtCore.Slot()
    def relative_0_360(self, le_p, le_v, r, rel):

        relative_p_2 = float(le_p) - scale[int(widgets.comboBox_2.currentIndex())] * r + rel + 0.001

        if int(relative_p_2) > 359:
            rel -= relative_p_2
        if int(relative_p_2) < -359:
            rel += relative_p_2

        self.pos_sp_ui(relative_p_2, le_v)

        txl.append(relative_p_2)

    @QtCore.Slot(float, float)
    def pos_sp_ui(self, pos, sp):

        self.ui.lineEdit_3.setText(str(format(pos, '.2f')))
        self.ui.lineEdit_6.setText(str(format(pos, '.2f')))

        self.ui.lineEdit_4.setText(str(format(sp, '.2f')))
        self.ui.lineEdit_5.setText(str(format(sp, '.2f')))

    ############## program mode ##################

    @QtCore.Slot()
    def add_progwidget(self):
        self.counter_id += 1

        prog_widget = ProgWidget(self.counter_id, self.value_list)
        self.ui.verticalLayout_21.addWidget(prog_widget)
        prog_widget.delete.connect(self.delete_widget)

    @QtCore.Slot()
    def clear_area(self):
        while self.ui.verticalLayout_21.count() > 0:
            item = self.ui.verticalLayout_21.takeAt(0)
            item.widget().deleteLater()
            self.counter_id = 0

    @QtCore.Slot(int)
    def delete_widget(self, wid: int):
        item = self.ui.verticalLayout_21.takeAt(wid - 1)
        widget = item.widget()

        self.ui.verticalLayout_21.removeWidget(widget)
        widget.deleteLater()

    @QtCore.Slot()
    def program_out(self):

        pr_name = "Программа " + str(int(self.ui.comboBox_5.count()) + 1)

        self.ui.comboBox_5.addItem(pr_name)
        self.ui.comboBox_5.setCurrentText(pr_name)

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)

        self.val_dict[pr_name] = {}

        for wid in range(self.ui.verticalLayout_21.count()):
            print(wid)

            item = self.ui.verticalLayout_21.itemAt(wid)
            widget = item.widget()
            self.value_list = widget.val_list
            print(self.value_list)

            self.val_dict[pr_name].update({wid: tuple(self.value_list)})

        with open('progmode.json', 'w') as file:
            json.dump(self.val_dict, file, indent=3)

    @QtCore.Slot()
    def program_save(self):

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)

        pr_name = self.ui.comboBox_5.currentText()

        self.val_dict[pr_name] = {}

        for wid in range(self.ui.verticalLayout_21.count()):
            item = self.ui.verticalLayout_21.itemAt(wid)
            widget = item.widget()
            self.value_list = widget.val_list

            self.val_dict[pr_name].update({wid: tuple(self.value_list)})

        with open('progmode.json', 'w') as file:
            json.dump(self.val_dict, file, indent=3)

    @QtCore.Slot()
    def program_update(self):

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)

        a = list(self.val_dict.keys())
        b = [self.ui.comboBox_5.itemText(i) for i in range(self.ui.comboBox_5.count())]

        res = list(set(a) - set(b))

        self.ui.comboBox_5.addItems(sorted(res))

    @QtCore.Slot()
    def program_select(self):
        self.clear_area()

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)

        pr_name = self.ui.comboBox_5.currentText()
        try:
            pr = self.val_dict[pr_name]

            for i in range(len(pr)):
                self.counter_id += 1
                prog_widget = ProgWidget(self.counter_id, pr[str(i)])
                self.ui.verticalLayout_21.addWidget(prog_widget)
                prog_widget.delete.connect(self.delete_widget)
        except Exception:
            pass

    @QtCore.Slot()
    def program_delete(self):
        self.clear_area()

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)

        pr_name = self.ui.comboBox_5.currentText()

        self.val_dict[pr_name] = {}

        self.ui.comboBox_5.removeItem(self.ui.comboBox_5.currentIndex())

        with open('progmode.json', 'w') as file:
            json.dump(self.val_dict, file, indent=3)

    ############## inner program mode ##############

    def turn_off_btn(self):
        try:

            communicate_with_lm(b"SO\r")
            time.sleep(0.1)

            communicate_with_lm(b"MO=0\r")
            time.sleep(0.1)

            try:
                self.stoptime1.stop()
                self.stoptime2.stop()
                self.sin_time.stop()
            except:
                pass

            self.ui.lineEdit_9.setText('СТОП')
            self.ui.lineEdit_23.setText('СТОП')
            self.ui.creditsLabel.setText('Окончание сеанса')
        except Exception:
            pass

    @QtCore.Slot(list)
    def unlim_rotate(self, l: list):

        communicate_with_lm(b"MO=1\r")
        time.sleep(0.1)
        communicate_with_lm(b"UM=2\r")
        time.sleep(0.1)

        bit_scale = scale_b[int(widgets.comboBox_6.currentIndex())]

        try:
            communicate_with_lm(('AC=' + str(format(bit_scale * float(l[1]), '.1f')) + '\r').encode('utf-8'))
        except Exception:
            pass
        communicate_with_lm(('JV=' + str(format(bit_scale * float(l[0]), '.1f')) + '\r').encode('utf-8'))

        # print(l, 'unlim')

        time.sleep(0.1)
        communicate_with_lm(b"BG\r")

    @QtCore.Slot(list)
    def pos_rotate(self, l: list):

        communicate_with_lm(b"MO=1\r")
        time.sleep(0.1)
        communicate_with_lm(b"UM=5\r")
        time.sleep(0.1)

        bit_scale = scale_b[int(self.ui.comboBox_6.currentIndex())]

        communicate_with_lm(('JP=' + str(format(bit_scale * float(l[0]), '.1f')) + '\r').encode('utf-8'))
        time.sleep(0.1)

        try:
            communicate_with_lm(('AC=' + str(format(bit_scale * float(l[1]), '.1f')) + '\r').encode('utf-8'))
        except Exception:
            pass
        time.sleep(0.1)

        communicate_with_lm(('PA=' + str(format(bit_scale * float(l[2]), '.1f')) + '\r').encode('utf-8'))
        time.sleep(0.1)
        communicate_with_lm(b"BG\r")

    @QtCore.Slot(list)
    def sin_rotate(self, l: list):
        global sin_var
        sin_var = 0

        communicate_with_lm(b"MO=1\r")
        time.sleep(0.1)
        communicate_with_lm(b"UM=2\r")
        time.sleep(0.1)

        bit_scale = scale_b[int(self.ui.comboBox_6.currentIndex())]

        try:
            communicate_with_lm(('AC=' + str(format(bit_scale * float(l[1]), '.1f')) + '\r').encode('utf-8'))

            communicate_with_lm(('SP=' + str(format(bit_scale * float(l[0]), '.1f')) + '\r').encode('utf-8'))
        except Exception:
            pass

        self.l_sin = l
        self.sin_time = QtCore.QTimer()
        self.sin_time.setInterval(500)
        self.sin_time.timeout.connect(self.sin_handler)
        self.sin_time.start()

    @QtCore.Slot()
    def sin_handler(self):
        global sin_var

        sin_var += 1

        l = self.l_sin

        bit_scale = scale_b[int(self.ui.comboBox_6.currentIndex())]

        snd = str(format(bit_scale * float(l[0]) * math.sin(float(l[3] * sin_var) * 0.008772), '.0f'))

        communicate_with_lm(('JV=' + snd + '\r').encode('utf-8'))

        communicate_with_lm(b"BG\r")

    @QtCore.Slot()
    def go_to_zero(self):
        self.pos_rotate(["100", "10", "0", "", "", 1])

    ############## inner program mode  ##############

    @QtCore.Slot()
    def progmode_handler(self):
        global cntr

        self.program_save()

        adder = 0
        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)
        pr_name = self.ui.comboBox_5.currentText()
        pr = self.val_dict[pr_name]

        for step in range(len(pr)):
            QTimer.singleShot(adder, lambda: self.progmode_filter())
            adder += int(float(pr[str(step)][4]) * 60000)

        cntr = 0
        self.ui.lineEdit_23.setText(str(adder / 1000))

        self.pr_remain_time = QtCore.QTimer()
        self.pr_remain_time.setInterval(1000)
        self.pr_remain_time.timeout.connect(self.progmode_remainer)
        self.pr_remain_time.start()

    @QtCore.Slot()
    def progmode_remainer(self):
        try:
            a = float(self.ui.lineEdit_23.text()[:-2])

            if a > 0.5:
                a -= 1.0
                self.ui.lineEdit_23.setText(str(a))
            else:

                communicate_with_lm(b"SO\r")
                time.sleep(0.1)
                communicate_with_lm(b"MO=0\r")

        except Exception:
            try:
                self.ui.lineEdit_23.setText('СТОП')
                self.pr_remain_time.stop()
                self.sin_time.stop()
            except Exception:
                pass

    @QtCore.Slot()
    def progmode_filter(self):
        global cntr

        with open('progmode.json', 'r') as file:
            self.val_dict = json.load(file)
        pr_name = self.ui.comboBox_5.currentText()
        pr = self.val_dict[pr_name]

        if str(pr[str(cntr)][5]) == "0":
            self.unlim_rotate(pr[str(cntr)])

        elif str(pr[str(cntr)][5]) == "1":
            self.pos_rotate(pr[str(cntr)])

        elif str(pr[str(cntr)][5]) == "2":
            self.sin_rotate(pr[str(cntr)])

        elif str(pr[str(cntr)][5]) == "3":
            self.turn_off_btn()

        cntr += 1
