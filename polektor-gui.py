from typing import Text
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from polektor import Ui_Form

import serial, serial.tools.list_ports
import os,csv
import numpy as np
import time
import scipy.signal
import string,random
import fb_config as fb
import knn
from datetime import datetime
from measure_suhu import Suhu
from measure_oximeter import Oximeter
from measure_tensimeter import Tensimeter

class ClickableLineEdit(QLineEdit):
    clicked = pyqtSignal() # signal when the text entry is left clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton: self.clicked.emit()
        else: super().mousePressEvent(event)

class gui (QtWidgets.QDialog, Ui_Form):
    sigKeyButtonClicked = pyqtSignal(object) 
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port = ""
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.start_word = False
        self.max30105 = []
        self.mlx90614 = []
        self.adstensi = []
        
        #EVENT TIMER
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.time)
        self.timer.start(1000)

        #EVENT HANDLE
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_measure_oxi.clicked.connect(self.measure_oxi)
        self.btn_measure_suhu.clicked.connect(self.measure_suhu)
        self.btn_measure_tensi.clicked.connect(self.measure_tensi)
        self.btn_generate.clicked.connect(self.generate)
        self.btn_validation.clicked.connect(self.validation)
        self.btn_predict.clicked.connect(self.predict)
        self.btn_reset.clicked.connect(self.reset_data)

        #KNN
        self.knn = knn.knn()
        self.knn.initialize()

        #INPUT
        self.in_nama.clicked.connect(self.handle_in_nama)
        self.in_nik.clicked.connect(self.handle_in_nik)
        self.in_umur.clicked.connect(self.handle_in_umur)
        self.in_sys.clicked.connect(self.handle_in_sys)
        self.in_dias.clicked.connect(self.handle_in_dias)
        self.in_suhu.clicked.connect(self.handle_in_suhu)
        self.in_bpm.clicked.connect(self.handle_in_bpm)
        self.in_spo2.clicked.connect(self.handle_in_spo2)
        
        #KEYBOARD
        self.pos_cursor = 0 #0:none 1:nama 2:nik 3:21 4:diastole 5:sistole 6:suhu 7:jantung 8:spo2
        self.buff_key = ''
        self.key_q.clicked.connect(self.inkey_q)
        self.key_w.clicked.connect(self.inkey_w)
        self.key_e.clicked.connect(self.inkey_e)
        self.key_r.clicked.connect(self.inkey_r)
        self.key_t.clicked.connect(self.inkey_t)
        self.key_y.clicked.connect(self.inkey_y)
        self.key_u.clicked.connect(self.inkey_u)
        self.key_i.clicked.connect(self.inkey_i)
        self.key_o.clicked.connect(self.inkey_o)
        self.key_p.clicked.connect(self.inkey_p)
        self.key_a.clicked.connect(self.inkey_a)
        self.key_s.clicked.connect(self.inkey_s)
        self.key_d.clicked.connect(self.inkey_d)
        self.key_f.clicked.connect(self.inkey_f)
        self.key_g.clicked.connect(self.inkey_g)
        self.key_h.clicked.connect(self.inkey_h)
        self.key_j.clicked.connect(self.inkey_j)
        self.key_k.clicked.connect(self.inkey_k)
        self.key_l.clicked.connect(self.inkey_l)
        self.key_z.clicked.connect(self.inkey_z)
        self.key_x.clicked.connect(self.inkey_x)
        self.key_c.clicked.connect(self.inkey_c)
        self.key_v.clicked.connect(self.inkey_v)
        self.key_b.clicked.connect(self.inkey_b)
        self.key_n.clicked.connect(self.inkey_n)
        self.key_m.clicked.connect(self.inkey_m)
        self.key_1.clicked.connect(self.inkey_1)
        self.key_2.clicked.connect(self.inkey_2)
        self.key_3.clicked.connect(self.inkey_3)
        self.key_4.clicked.connect(self.inkey_4)
        self.key_5.clicked.connect(self.inkey_5)
        self.key_6.clicked.connect(self.inkey_6)
        self.key_7.clicked.connect(self.inkey_7)
        self.key_8.clicked.connect(self.inkey_8)
        self.key_9.clicked.connect(self.inkey_9)
        self.key_0.clicked.connect(self.inkey_0)
        self.key_space.clicked.connect(self.inkey_space)
        self.key_comma.clicked.connect(self.inkey_comma)
        self.key_bs.clicked.connect(self.handle_inkey_bs)
        self.key_enter.clicked.connect(self.handle_inkey_enter)
        self.key_del.clicked.connect(self.handle_inkey_del)
        self.btn_exit.clicked.connect(self.handle_exit)

    def print(self,kata):
        self.console.append(str(kata))

    def handle_exit(self):
        sys.exit()

    def time(self):
        now = datetime.now()
        self.lbl_jam.setText(now.strftime("%H:%M:%S"))
        self.lbl_time.setText(now.strftime("%-m/%-d/%Y"))
    
    def handle_inkey_del(self):
        if self.pos_cursor == 1:
            self.in_nama.setText("")
        elif self.pos_cursor == 2:
            self.in_nik.setText("")
        elif self.pos_cursor == 3:
            self.in_umur.setText("")
        elif self.pos_cursor == 4:
            self.in_sys.setText("")
        elif self.pos_cursor == 5:
            self.in_dias.setText("")
        elif self.pos_cursor == 6:
            self.in_suhu.setText("")
        elif self.pos_cursor == 7:
            self.in_bpm.setText("")
        elif self.pos_cursor == 8:
            self.in_spo2.setText("")

    def reset_data(self):
        self.in_nama.setText("")
        self.in_nik.setText("")
        self.in_umur.setText("")
        self.in_sys.setText("")
        self.in_dias.setText("")
        self.in_suhu.setText("")
        self.in_bpm.setText("")
        self.in_spo2.setText("")
        self.lbl_kategori.setText("-")
        self.lbl_pw.setText("-")

    def handle_inkey_enter(self):
        self.pos_cursor = 0
        self.clear_color_button()

    def handle_inkey_bs(self):
        if self.pos_cursor == 1:
            currenttext = self.in_nama.text()
            self.in_nama.setText(currenttext[:-1])
        elif self.pos_cursor == 2:
            currenttext = self.in_nik.text()
            self.in_nik.setText(currenttext[:-1])
        elif self.pos_cursor == 3:
            currenttext = self.in_umur.text()
            self.in_umur.setText(currenttext[:-1])
        elif self.pos_cursor == 4:
            currenttext = self.in_sys.text()
            self.in_sys.setText(currenttext[:-1])
        elif self.pos_cursor == 5:
            currenttext = self.in_dias.text()
            self.in_dias.setText(currenttext[:-1])
        elif self.pos_cursor == 6:
            currenttext = self.in_suhu.text()
            self.in_suhu.setText(currenttext[:-1])
        elif self.pos_cursor == 7:
            currenttext = self.in_bpm.text()
            self.in_bpm.setText(currenttext[:-1])
        elif self.pos_cursor == 8:
            currenttext = self.in_spo2.text()
            self.in_spo2.setText(currenttext[:-1])

    def clear_color_button(self):
        self.in_nama.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_nik.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_umur.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_sys.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_dias.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_bpm.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_spo2.setStyleSheet("QPushButton{font-size : 18px;}")
        self.in_suhu.setStyleSheet("QPushButton{font-size : 18px;}")
        
    def handle_in_nama(self):
        self.clear_color_button()
        self.in_nama.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 1
        self.enable_abjad = True
        self.enable_angka = False

    def handle_in_nik(self):
        self.clear_color_button()
        self.in_nik.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 2
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_umur(self):
        self.clear_color_button()
        self.in_umur.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 3
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_sys(self):
        self.clear_color_button()
        self.in_sys.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 4
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_dias(self):
        self.clear_color_button()
        self.in_dias.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 5
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_suhu(self):
        self.clear_color_button()
        self.in_suhu.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 6
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_bpm(self):
        self.clear_color_button()
        self.in_bpm.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 7
        self.enable_abjad = False
        self.enable_angka = True

    def handle_in_spo2(self):
        self.clear_color_button()
        self.in_spo2.setStyleSheet("QPushButton{background-color : rgb(85, 87, 83);}"
                                   "QPushButton{color : rgb(238, 238, 236);}"
                                   "QPushButton{font-size : 18px;}")
        self.pos_cursor = 8
        self.enable_abjad = False
        self.enable_angka = True

#### KEYBOARD FUNCTION ####
    def input_angka(self):
        if self.pos_cursor == 2:
            currenttext = self.in_nik.text()
            self.in_nik.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 3:
            currenttext = self.in_umur.text()
            self.in_umur.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 4:
            currenttext = self.in_sys.text()
            self.in_sys.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 5:
            currenttext = self.in_dias.text()
            self.in_dias.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 6:
            currenttext = self.in_suhu.text()
            self.in_suhu.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 7:
            currenttext = self.in_bpm.text()
            self.in_bpm.setText(currenttext + self.buff_key)

        elif self.pos_cursor == 8:
            currenttext = self.in_spo2.text()
            self.in_spo2.setText(currenttext + self.buff_key)
    def input_abjad(self):
        if self.pos_cursor == 1:
            currenttext = self.in_nama.text()
            self.in_nama.setText(currenttext + self.buff_key)
    def inkey_space(self):
        self.buff_key = ' '
        self.input_abjad()
    def inkey_q(self):
        self.buff_key = 'Q'
        self.input_abjad()
    def inkey_w(self):
        self.buff_key = 'W'
        self.input_abjad()
    def inkey_e(self):
        self.buff_key = 'E'
        self.input_abjad()
    def inkey_r(self):
        self.buff_key = 'R'
        self.input_abjad()
    def inkey_t(self):
        self.buff_key = 'T'
        self.input_abjad()
    def inkey_y(self):
        self.buff_key = 'Y'
        self.input_abjad()
    def inkey_u(self):
        self.buff_key = 'U'
        self.input_abjad()
    def inkey_i(self):
        self.buff_key = 'I'
        self.input_abjad()
    def inkey_o(self):
        self.buff_key = 'O'
        self.input_abjad()
    def inkey_p(self):
        self.buff_key = 'P'
        self.input_abjad()
    def inkey_a(self):
        self.buff_key = 'A'
        self.input_abjad()
    def inkey_s(self):
        self.buff_key = 'S'
        self.input_abjad()
    def inkey_d(self):
        self.buff_key = 'D'
        self.input_abjad()
    def inkey_f(self):
        self.buff_key = 'F'
        self.input_abjad()
    def inkey_g(self):
        self.buff_key = 'G'
        self.input_abjad()
    def inkey_h(self):
        self.buff_key = 'H'
        self.input_abjad()
    def inkey_j(self):
        self.buff_key = 'J'
        self.input_abjad()
    def inkey_k(self):
        self.buff_key = 'K'
        self.input_abjad()
    def inkey_l(self):
        self.buff_key = 'L'
        self.input_abjad()
    def inkey_z(self):
        self.buff_key = 'Z'
        self.input_abjad()
    def inkey_x(self):
        self.buff_key = 'X'
        self.input_abjad()
    def inkey_c(self):
        self.buff_key = 'C'
        self.input_abjad()
    def inkey_v(self):
        self.buff_key = 'V'
        self.input_abjad()
    def inkey_b(self):
        self.buff_key = 'B'
        self.input_abjad()
    def inkey_n(self):
        self.buff_key = 'N'
        self.input_abjad()
    def inkey_m(self):
        self.buff_key = 'M'
        self.input_abjad()
    def inkey_1(self):
        self.buff_key = '1'
        self.input_angka()
    def inkey_2(self):
        self.buff_key = '2'
        self.input_angka()
    def inkey_3(self):
        self.buff_key = '3'
        self.input_angka()
    def inkey_4(self):
        self.buff_key = '4'
        self.input_angka()
    def inkey_5(self):
        self.buff_key = '5'
        self.input_angka()
    def inkey_6(self):
        self.buff_key = '6'
        self.input_angka()
    def inkey_7(self):
        self.buff_key = '7'
        self.input_angka()
    def inkey_8(self):
        self.buff_key = '8'
        self.input_angka()
    def inkey_9(self):
        self.buff_key = '9'
        self.input_angka()
    def inkey_0(self):
        self.buff_key = '0'
        self.input_angka()
    def inkey_comma(self):
        self.buff_key = '.'
        self.input_angka()
###########################

    def predict(self):
        kelamin = self.cb_kelamin.currentText()
        if kelamin == "PRIA" :
            kelamin = ord("L")
        elif kelamin == "WANITA":
            kelamin = ord("P")

        umur = self.in_umur.text()
        suhu = self.in_suhu.text()
        bpm = self.in_bpm.text()
        spo2 = self.in_spo2.text()
        sys = self.in_sys.text()
        dias = self.in_dias.text()
        
        #print(umur,kelamin,suhu,spo2,bpm,sys,dias)
        try:
            retval, result, neigh_resp, dists = self.knn.predict(
                                                                #umur=umur,
                                                                #jenis_kelamin=kelamin,
                                                                suhu=suhu,
                                                                #detak_jantung=bpm,
                                                                spo2=spo2,
                                                                #systole=sys,
                                                                #diastole=dias,
                                                                k=5)
            print(retval, result, neigh_resp, dists)
            if result == 'N':
                self.lbl_kategori.setText("NEGATIF")
                self.lbl_kategori.setStyleSheet("color: yellow;")

            elif result == 'P':
                self.lbl_kategori.setText("POSITIF")
                self.lbl_kategori.setStyleSheet("color: red;")
                
            self.print("DONE PREDICT")
            
        except:
            self.print("DATA TIDAK LENGKAP")
        
    def validation(self):
        current_date = self.lbl_time.text()
        nik = self.in_nik.text()
        nama = self.in_nama.text()
        kelamin = self.cb_kelamin.currentText()
        umur = self.in_umur.text()
        suhu = self.in_suhu.text()
        bpm = self.in_bpm.text()
        spo2 = self.in_spo2.text()
        tensi = self.in_sys.text() + "/" + self.in_dias.text()
        kategori = self.lbl_kategori.text()
        berlaku = self.cb_masaberlaku.currentText()[:1]
        pw = self.lbl_pw.text()

        if nik == '' or nama == '' or umur == '' or suhu == '' or bpm == '' or spo2 == '' or self.in_sys.text() == '' or self.in_dias.text() == '':
            self.print("PUBLISH FAILED, DATA EMPTY")
        else :
            datafile_name = 'foo.csv'
            if os.path.isfile(datafile_name):
                os.remove(datafile_name)

            a = np.array([[current_date,nik,nama,kelamin,umur,suhu,tensi,bpm,spo2,berlaku,kategori]])
            
            with open('foo.csv', 'a') as file:
                mywriter = csv.writer(file, delimiter=',')
                mywriter.writerows(a)

            path_on_cloud = "result/" + nik + "_" + pw + ".csv"
            fb.publish(path_on_cloud=path_on_cloud,path_local="foo.csv")
            self.print("PUBLISH DONE")

    def generate(self):
        def pw_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))
        self.lbl_pw.setText(str(pw_generator()))

    def refresh(self):
        self.cb_serial.clear()
        self.cb_serial.addItem("None")
        portData = serial.tools.list_ports.comports()
        for i in range(0,len(portData)):
            port = portData[i]
            strPort = str(port)
            if '/dev/tty' in strPort :
                splitPort=strPort.split(' ')
                self.cb_serial.addItem(splitPort[0])

    def measure_oxi(self):
        self.max30105 = []
        port = str(self.cb_serial.currentText())

        if port == "None":
            self.print("PORT IS DISCONNECTED") 
            oxi_measure = Oximeter()
            bpm,spo2 = oxi_measure.getResult()
            self.in_bpm.setText(str(bpm))
            self.in_spo2.setText(str(spo2))
        else:
            ## READ FROM ARDUINO
            self.print("BEGIN MEASURING OXI")
            arduino = serial.Serial(port=port,baudrate=115200,timeout=.1)
            time.sleep(2)
            arduino.write(bytes('0', 'utf-8')) #KIRIM KE ARDUINO 0
            time.sleep(0.05)
            while True:
                curr_line = arduino.readline()
                if curr_line[0:-2]==b'ENDMEASURE':
                    break
                if curr_line[0:-2]!=b'':
                    self.max30105.append(curr_line)
            
            ## CLEAR LAST DATA
            datafile_name = 'max30102_data.csv'
            if os.path.isfile(datafile_name):
                os.remove(datafile_name)

            ## PREPROCESSING DATA
            t_vec,ir_vec,red_vec = [],[],[]
            ir_prev,red_prev = 0.0,0.0
            for ii in range(3,len(self.max30105)):
                try:
                    curr_data = (self.max30105[ii][0:-2]).decode("utf-8").split(',')
                except:
                    continue
                if len(curr_data)==3:
                    if abs((float(curr_data[1])-ir_prev)/float(curr_data[1]))>1.01 or\
                    abs((float(curr_data[2])-red_prev)/float(curr_data[2]))>1.01:
                        continue
                    t_vec.append(float(curr_data[0])/1000000.0)
                    ir_vec.append(float(curr_data[1]))
                    red_vec.append(float(curr_data[2]))
                    ir_prev = float(curr_data[1])
                    red_prev = float(curr_data[2])
            
            ## SAVE TO CSV
            with open(datafile_name,'a') as f:
                writer = csv.writer(f,delimiter=',')
                for t,x,y in zip(t_vec,ir_vec,red_vec):
                    writer.writerow([t,x,y])

            ## CALCULATING
            oxi_measure = Oximeter()
            bpm,spo2 = oxi_measure.getResult()
            self.in_bpm.setText(str(bpm))
            self.in_spo2.setText(str(spo2))
            self.print("MEASURING OXI DONE")

    def measure_suhu(self):
        self.mlx90614 = []
        port = str(self.cb_serial.currentText())

        if port == "None":
            self.print("PORT IS DISCONNECTED")
            suhu_measure = Suhu()
            self.in_suhu.setText(str(suhu_measure.getResult()))
        else:
            ## READ FROM ARDUINO
            self.print("BEGIN MEASURING SUHU")
            arduino = serial.Serial(port=port,baudrate=115200,timeout=.1)
            time.sleep(2)
            arduino.write(bytes('1', 'utf-8')) #NGIRIM SINYAL KE ARDUINO
            time.sleep(0.05)
            while True:
                curr_line = arduino.readline()
                if curr_line[0:-2]==b'ENDMEASURE':
                    break
                if curr_line[0:-2]!=b'':
                    self.mlx90614.append(curr_line)
            
            ## CLEAR LAST DATA
            datafile_name = 'mlx90614_data.csv'
            if os.path.isfile(datafile_name):
                os.remove(datafile_name)

            ## PREPROCESSING DATA
            t_vec,suhu_vec = [],[]
            suhu_prev = 0.0
            for ii in range(3,len(self.mlx90614)):
                try:
                    curr_data = (self.mlx90614[ii][0:-2]).decode("utf-8").split(',')
                except:
                    continue
                if len(curr_data)==2:
                    if abs((float(curr_data[1])-suhu_prev)/float(curr_data[1]))>1.01:
                        continue
                    t_vec.append(float(curr_data[0])/1000000.0)
                    suhu_vec.append(float(curr_data[1]))
                    suhu_prev = float(curr_data[1])

            ## SAVE TO CSV
            with open(datafile_name,'a') as f:
                writer = csv.writer(f,delimiter=',')
                for t,x in zip(t_vec,suhu_vec):
                    writer.writerow([t,x])

            ## CALCULATE
            suhu_measure = Suhu()
            self.in_suhu.setText(str(suhu_measure.getResult()))
            self.print("MEASURING SUHU DONE")
                
    def measure_tensi(self):
        self.adstensi = []
        port = str(self.cb_serial.currentText())

        if port == "None":
            self.print("PORT IS DISCONNECTED") 
            tensi_measure = Tensimeter()
            pulse,map,sys,dys = tensi_measure.getResult()
            self.in_sys.setText(str(sys))
            self.in_dias.setText(str(dys))
        else:
            self.print("BEGIN MEASURING TENSI")
            arduino = serial.Serial(port=port,baudrate=115200,timeout=.1)
            time.sleep(2)
            arduino.write(bytes('2', 'utf-8'))
            time.sleep(0.05)
            while True:
                curr_line = arduino.readline()
                if curr_line[0:-2]==b'ENDMEASURE':
                    break
                if curr_line[0:-2]!=b'':
                    self.adstensi.append(curr_line)
                    
            
            ## CLEAR LAST DATA
            datafile_name = 'adstensi_data.csv'
            if os.path.isfile(datafile_name):
                os.remove(datafile_name)
            
            ## PREPROCESSING DATA
            t_vec,tensi_vec = [],[]
            tensi_prev = 0.0
            for ii in range(3,len(self.adstensi)):
                try:
                    curr_data = (self.adstensi[ii][0:-2]).decode("utf-8").split(',')
                except:
                    continue
                if len(curr_data)==2:
                    if abs((float(curr_data[1])-tensi_prev)/float(curr_data[1]))>1.01:
                        continue
                    t_vec.append(float(curr_data[0])/1000000.0)
                    tensi_vec.append(float(curr_data[1]))
                    tensi_prev = float(curr_data[1])

            ## SAVE TO CSV
            with open(datafile_name,'a') as f:
                writer = csv.writer(f,delimiter=',')
                for t,x in zip(t_vec,tensi_vec):
                    writer.writerow([t,x])

            ## CALCULATE
            try:
                tensi_measure = Tensimeter()
                pulse,map,sys,dys = tensi_measure.getResult()
                self.in_sys.setText(str(sys))
                self.in_dias.setText(str(dys))
                self.print("MEASURING TENSI DONE")
            except:
                self.print("MEASURING TENSI FAILED")
              
if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    window = gui()
    window.setWindowTitle('POLECTOR - Poltekad Covid19 Detector')
    window.show()
    sys.exit(app.exec_())