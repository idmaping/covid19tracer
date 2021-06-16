from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Oximeter:
    def __init__(self) :
        self.data = genfromtxt('max30102_data.csv', delimiter=',')
        self.t = self.data[:,0]
        self.ir = self.data[:,1]
        self.red = self.data[:,2]

        self.heartrate()
        self.spo2()

    def spo2(self):
        frate = 0.95
        avered = 0
        aveir = 0
        sumredrms = 0
        sumirrms = 0
        R=0
        buff_spo2,buff_ratio=[],[]
        for i in range(len(self.t)):
            avered = avered * frate + self.red[i] * (1.0 - frate)
            sumredrms += (self.red[i] - avered) * (self.red[i] - avered)        
            aveir = aveir * frate + self.ir[i] * (1.0 - frate)
            sumirrms += (self.ir[i] - aveir) * (self.ir[i] - aveir)

            if i%int(np.mean(np.diff(self.indexes))) == 0:
                R = (np.sqrt(sumredrms) / avered) / (np.sqrt(sumirrms) / aveir)
                self.SpO2 = -23.3 * (R - 0.4) + 100
                sumredrms = 0
                sumirrms = 0
                buff_spo2.append(self.SpO2)
            buff_ratio.append(R)

        

        
        

    def heartrate(self):
        smoothing_size = 20 
        samp_rate = 1/np.mean(np.diff(self.t)) 
        self.y_vals = self.ir
        self.y_vals = np.convolve(self.y_vals,np.ones((smoothing_size,)),'same')/smoothing_size
        self.y_vals = np.append(np.repeat(self.y_vals[int(smoothing_size/2)],int(smoothing_size/2)),self.y_vals[int(smoothing_size/2):-int(smoothing_size/2)])
        self.y_vals = np.append(self.y_vals,np.repeat(self.y_vals[-int(smoothing_size/2)],int(smoothing_size/2)))
        self.indexes, _ = signal.find_peaks(self.y_vals, distance=samp_rate*.5)
        self.scatter_x,self.scatter_y = [],[]
        for jj in self.indexes:
            self.scatter_x.append(self.t[jj])
            self.scatter_y.append(self.y_vals[jj])
        self.bpm = np.around(60/np.mean(np.diff(self.scatter_x)), decimals=2)

    def getResult(self):
        bpm = np.around(self.bpm,decimals=2)
        spo2 = np.around(self.SpO2,decimals=2)
        return bpm, spo2  

    def plot(self):
        f, axes = plt.subplots(2)
        axes[0].plot(self.t,
                     self.ir,
                     color='black',label='1) IR Data')
        axes[0].plot(self.t,
                     self.y_vals,
                     color='blue',label='2) Filtered IR Data')
        axes[0].plot(self.scatter_x,
                     self.scatter_y,
                     'X',color='red',label='3) Peak IR Data')
        axes[0].set_xlabel("Time (s)")
        axes[0].set_ylabel("IR Value")
        axes[0].legend(loc='upper right')

        axes[1].plot(self.t,
                     self.ir,
                     color='blue',label='1) IR Data')
        axes[1].set_ylabel('IR Data', color='tab:blue')
        ax2 = axes[1].twinx()      
        ax2.plot(self.t,
                     self.red,
                     color='red',label='2) RED Data')
        ax2.set_ylabel('RED Data', color='tab:red')
        axes[1].set_xlabel("Time (s)")
        plt.show()



if __name__ == '__main__':
    oxi = Oximeter()
    oxi.plot()