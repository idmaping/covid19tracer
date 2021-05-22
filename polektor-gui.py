from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from polektor import Ui_Form
import serial, serial.tools.list_ports
import time,os,csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class gui (QtWidgets.QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.port = ""

        self.start_word = False
        self.max30105 = []
        self.mlx90614 = []
        
        #EVENT HANDLE
        self.btn_refresh.clicked.connect(self.refresh_serial)
        self.btn_measure.clicked.connect(self.measure)
        #self.btn_connect.clicked.connect(self.connect)
        
    def refresh_serial(self):
        self.cb_serial.clear()
        self.cb_serial.addItem("None")
        portData = serial.tools.list_ports.comports()
        for i in range(0,len(portData)):
            port = portData[i]
            strPort = str(port)
            if '/dev/tty' in strPort :
                splitPort=strPort.split(' ')
                self.cb_serial.addItem(splitPort[0])

    def calculate_oximeter(self):
        datafile_name = 'max30102_data.csv'
        if os.path.isfile(datafile_name):
            os.remove(datafile_name)
        
        '''
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
        print('Sample Rate: {0:2.1f}Hz'.format(1.0/np.mean(np.abs(np.diff(t_vec)))))

        ## saving data
        with open(datafile_name,'a') as f:
            writer = csv.writer(f,delimiter=',')
            for t,x,y in zip(t_vec,ir_vec,red_vec):
                writer.writerow([t,x,y])

        ## plotting data vectors 
        fig = plt.figure(figsize=(12,8))
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('Time [s]',fontsize=24)
        ax1.set_ylabel('IR Amplitude',fontsize=24,color='#CE445D',labelpad=10)
        ax1.tick_params(axis='both',which='major',labelsize=16)
        plt1 = ax1.plot(t_vec,ir_vec,label='IR',color='#CE445D',linewidth=4)
        ax1_2 = plt.twinx()
        ax1_2.grid('off')
        ax1_2.set_ylabel('Red Amplitude',fontsize=24,color='#37A490',labelpad=10)
        ax1_2.tick_params(axis='y',which='major',labelsize=16)
        plt2 = ax1_2.plot(t_vec,red_vec,label='Red',color='#37A490',linewidth=4)
        lns = plt1+plt2
        labels = [l.get_label() for l in lns]
        ax1_2.legend(lns,labels,fontsize=16)
        plt.xlim([t_vec[0],t_vec[-1]])
        plt.tight_layout(pad=1.2)
        plt.savefig('max30102_example.png',dpi=300,facecolor=[252/255,252/255,252/255])
        plt.show()
        '''


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
                #try :
                curr_line = ser.readline() # read line
                #print(curr_line[0:-2],self.start_word)

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

                #except KeyboardInterrupt:
                #    break
            #print("================================================")
            #print("MAX30105")
            #print(self.max30105)
            #print("MLX90614")
            #print(self.mlx90614)
            self.calculate_oximeter()
            

            


if __name__=='__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Windows')
    window = gui()
    window.setWindowTitle('Test Open GL')
    window.show()
    sys.exit(app.exec_())