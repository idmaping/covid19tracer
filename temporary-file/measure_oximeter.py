from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Oximeter:
    def __init__(self) :
        self.data = genfromtxt('max30102_data.csv', delimiter=',')
        self.t,self.ir,self.red = [],[],[]
        ir_prev,red_prev = 0.0,0.0

        for ii in range(3,len(self.data)):
            curr_data = self.data[ii]
            if len(curr_data)==3:
                if abs((float(curr_data[1])-ir_prev)/float(curr_data[1]))>1.01 or\
                abs((float(curr_data[2])-red_prev)/float(curr_data[2]))>1.01:
                    continue
                self.t.append(float(curr_data[0]))
                self.ir.append(float(curr_data[1]))
                self.red.append(float(curr_data[2]))
                ir_prev = float(curr_data[1])
                red_prev = float(curr_data[2])
        
        #print(self.ir)


        #self.t = self.data[:,0]
        #self.ir = self.data[:,1]
        #self.red = self.data[:,2]

        self.heartrate()


    def heartrate(self):
        smoothing_size = 20 # convolution smoothing size
        samp_rate = 1/np.mean(np.diff(self.t)) # average sample rate for determining peaks
        y_vals = self.ir
        y_vals = np.convolve(y_vals,np.ones((smoothing_size,)),'same')/smoothing_size
        y_vals = np.append(np.repeat(y_vals[int(smoothing_size/2)],int(smoothing_size/2)),y_vals[int(smoothing_size/2):-int(smoothing_size/2)])
        y_vals = np.append(y_vals,np.repeat(y_vals[-int(smoothing_size/2)],int(smoothing_size/2)))
        indexes, _ = signal.find_peaks(y_vals, distance=samp_rate*.5)
        scatter_x,scatter_y = [],[]
        for jj in indexes:
            scatter_x.append(self.t[jj])
            scatter_y.append(y_vals[jj])
        bpm = np.around(60/np.mean(np.diff(scatter_x)), decimals=2)

        plt.plot(self.t, self.ir)
        plt.plot(self.t, y_vals)
        plt.show()

        print(bpm)
        

    def getResult(self):
        pass        

    def plot(self):
        f, axes = plt.subplots(2)
        axes[0].plot(self.t,
                     self.ir,
                     color='blue',label='ir data')
        axes[0].plot(self.t,
                     self.red,
                     color='red',label='red data')

        plt.show()



if __name__ == '__main__':
    oxi = Oximeter()
    #oxi.plot()