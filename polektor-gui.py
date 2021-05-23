from typing import Text
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from polektor import Ui_Form
from validation import Ui_Dialog
import serial, serial.tools.list_ports
import time,os,csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.signal
import string,random
import fb_config as fb

class gui (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port = ""

        self.start_word = False
        self.max30105 = []
        self.mlx90614 = []
        
        #EVENT HANDLE
        self.btn_refresh.clicked.connect(self.refresh)
        self.btn_measure.clicked.connect(self.measure)
        self.btn_generate.clicked.connect(self.generate)
        self.btn_validation.clicked.connect(self.validation)

    def validation(self):
        current_date = self.lbl_time.text()
        nik = self.in_nik.text()
        nama = self.in_nama.text()
        kelamin = self.cb_kelamin.currentText()
        umur = self.in_umur.text()
        suhu = self.lbl_suhu.text()
        bpm = self.lbl_bpm.text()
        spo2 = self.lbl_spo2.text()
        tensi = self.lbl_tensi.text()
        kategori = self.lbl_kategori.text()
        berlaku = self.cb_masaberlaku.currentText()[:1]
        pw = self.lbl_pw.text()

        datafile_name = 'foo.csv'
        if os.path.isfile(datafile_name):
            os.remove(datafile_name)

        a = np.array([[current_date,nik,nama,kelamin,umur,suhu[2:],tensi[2:],bpm[2:],spo2[2:],berlaku,kategori[2:]]])
        with open('foo.csv', 'a') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(a)

        path_on_cloud = "result/" + nik + "_" + pw + ".csv"
        fb.publish(path_on_cloud=path_on_cloud,path_local="foo.csv")

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

    def find_spo2(self,t_vec,red_vec, ir_vec, sample):
        frate = 0.95
        avered = 0
        aveir = 0
        sumredrms = 0
        sumirrms = 0
        R=0
        buff_spo2,buff_ratio=[],[]
        for i in range(len(t_vec)):
            avered = avered * frate + red_vec[i] * (1.0 - frate)
            sumredrms += (red_vec[i] - avered) * (red_vec[i] - avered)        
            aveir = aveir * frate + ir_vec[i] * (1.0 - frate)
            sumirrms += (ir_vec[i] - aveir) * (ir_vec[i] - aveir)

            if i%sample == 0:
                R = (np.sqrt(sumredrms) / avered) / (np.sqrt(sumirrms) / aveir)
                SpO2 = -23.3 * (R - 0.4) + 100
                sumredrms = 0
                sumirrms = 0
                buff_spo2.append(SpO2)
            buff_ratio.append(R)
            
        return buff_ratio,buff_spo2

    def calculate_oximeter(self):
        datafile_name = 'max30102_data.csv'
        if os.path.isfile(datafile_name):
            os.remove(datafile_name)
        
        #preprocessing data
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
        #print('Sample Rate: {0:2.1f}Hz'.format(1.0/np.mean(np.abs(np.diff(t_vec)))))

        
        ## calculate heartrate
        smoothing_size = 20 # convolution smoothing size
        samp_rate = 1/np.mean(np.diff(t_vec)) # average sample rate for determining peaks
        y_vals = ir_vec
        y_vals = np.convolve(y_vals,np.ones((smoothing_size,)),'same')/smoothing_size
        y_vals = np.append(np.repeat(y_vals[int(smoothing_size/2)],int(smoothing_size/2)),y_vals[int(smoothing_size/2):-int(smoothing_size/2)])
        y_vals = np.append(y_vals,np.repeat(y_vals[-int(smoothing_size/2)],int(smoothing_size/2)))
        indexes, _ = scipy.signal.find_peaks(y_vals, distance=samp_rate*.5)
        scatter_x,scatter_y = [],[]
        for jj in indexes:
            scatter_x.append(t_vec[jj])
            scatter_y.append(y_vals[jj])
        bpm = 60/np.mean(np.diff(scatter_x))
        self.lbl_bpm.setText(": " + str(bpm)[:5])
        
        ## calculate SPo2
        ratio_vec,spo2_vec = self.find_spo2(t_vec=t_vec,red_vec=red_vec, ir_vec=ir_vec, sample=int(np.mean(np.diff(indexes))))
        self.lbl_spo2.setText(": " + str(np.mean(spo2_vec))[:5])

        ## saving data
        with open(datafile_name,'a') as f:
            writer = csv.writer(f,delimiter=',')
            for t,x,y in zip(t_vec,ir_vec,red_vec):
                writer.writerow([t,x,y])

    def calculate_suhu(self):
        datafile_name = 'mlx90614_data.csv'
        if os.path.isfile(datafile_name):
            os.remove(datafile_name)

        #preprocessing data
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

        #AVERAGE
        self.lbl_suhu.setText(": " + str(np.mean(suhu_vec))[:5])

        ## saving data
        with open(datafile_name,'a') as f:
            writer = csv.writer(f,delimiter=',')
            for t,x in zip(t_vec,suhu_vec):
                writer.writerow([t,x])

    def measure(self):
        port = str(self.cb_serial.currentText())
        if port == "None":
            print("PORT IS DISCONNECTED") #TAMPILKAN ALERT MESSAGE
        else:
            print("BEGIN MEASURING OXIMETER") #TAMPILKAN SHOW MESSAGE
            ser = serial.Serial(port,baudrate=115200)
            self.start_word = False
            self.max30105 = []
            self.mpx90614 = []
            while True:
                curr_line = ser.readline()
                if self.start_word == False:

                    if curr_line[0:-2]==b'MAX30102':
                        self.start_word = "MAX30102"
                        continue

                    elif curr_line[0:-2]==b'MLX90614':
                        self.start_word = "MLX90614"
                        continue
                    else :
                        continue
                if curr_line[0:-2]==b'END':
                    self.start_word = False 
                if curr_line[0:-2]==b'ENDMEASURE':
                    break
                if self.start_word == "MAX30102":
                    self.max30105.append(curr_line)
                if self.start_word == "MLX90614":
                    self.mlx90614.append(curr_line)
            self.calculate_oximeter()
            self.calculate_suhu()
            
if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')
    window = gui()
    window.setWindowTitle('POLECTOR - Poltekad Covid19 Detector')
    window.show()
    sys.exit(app.exec_())