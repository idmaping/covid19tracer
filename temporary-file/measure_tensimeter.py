from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Tensimeter:
    def __init__(self):
        self.data = genfromtxt('adstensi_data.csv', delimiter=',')
        self.t = self.data[:,0] #Time Raw
        self.ymmHg = self.normalize(arr = self.data[:,1], #Kalibrasi Manual TODO:COBA CARI DENGAN KALIBRASI DENGAN ALAT UKUR
                                   t_min = np.min(self.data[:,1]),
                                   t_max = np.max(self.data[:,1]))
        self.yfLP, self.yfHP, self.yfBP = self.filter(self.ymmHg)
        self.deflation, self.oscilation, self.oscilation_index, self.pulse, self.map, self.systolic_index, self.diastolic_index =self.measure()    

    def getResult(self):
        pulse = np.around(60/np.average(self.pulse), decimals=2)
        map = np.around(self.map[1], decimals=2)
        sys = np.average(self.yfLP[self.systolic_index[0]:self.systolic_index[1]])
        dys = np.average(self.yfLP[self.diastolic_index[0]:self.diastolic_index[1]])
        
        print('PULSE : ', pulse)
        print('MAP : ', map)
        print('SYS : ', sys)
        print('DIAS : ', dys)
        
        return pulse,map,sys,dys

    def filter(self,ymmHg):
        ## FREQUENCY SAMPLING
        fs = 50 

        ## LOWPASS FILTER
        f5 = 5
        bLP, aLP = signal.butter(4, f5/fs*2, 'lowpass')
        yfLP = signal.lfilter(bLP, aLP, ymmHg)
        
        ## HIGHPASS FILTER
        f05 = .5
        bHP, aHP = signal.butter(4, f05/fs*2, 'highpass')
        yfHP = signal.lfilter(bHP, aHP, yfLP)

        ## BANDPASS FILTER
        yfBP = yfLP-yfHP

        return yfLP,yfHP,yfBP

    def normalize(self, arr, t_min, t_max):
        norm_arr = []
        for i in arr:
            temp = (i-t_min)/(t_max - t_min) *200
            norm_arr.append(temp)
        return norm_arr

    def measure(self):
        ## FINDING LOCAL MAXIMA
        localMax, _ = signal.find_peaks(self.yfHP, prominence = .3 )
        yMaximas = self.yfBP[localMax]
        tMaximas = self.t[localMax]
        oscMax = self.yfHP[localMax] # the local max values of the oscillation
        
        ## FINDING WHEN DEFLATION STARTED 
        xPumpedUp = np.argmax(yMaximas) # get indice of overal max pressure 
        yPumpedUP = yMaximas[xPumpedUp] # the pressure that was pumped up to
        tPumpedUP = tMaximas[xPumpedUp] # the start time of the deflation 
        
        ## FINDING START AND END OF OSCILLATION
        deltaT = np.zeros(len(tMaximas))
        delta2T = np.zeros(len(tMaximas))
        validCnt = 0
        oscStartInd = 0
        oscEndInd = 0
        for i in range(1,len(tMaximas)-1):
            deltaT[i] = tMaximas[i]-tMaximas[i-1]
            delta2T[i] = deltaT[i]-deltaT[i-1]
            ### FIND START OF OSCILATION
            if oscStartInd == 0 :
                if np.abs(delta2T[i]) < 0.2 and i > xPumpedUp :
                    validCnt += 1
                    if validCnt == 5 : #calibration factor for sys
                        oscStartInd = i - (validCnt-1)
                else:
                    validCnt = 0
            ### FIND END OF OSCILATION
            elif oscEndInd == 0:    
                if (oscMax[oscStartInd]*1.2) > oscMax[i]: #calibration factor for dias
                    oscEndInd = i-3
        if oscEndInd == 0:
            oscEndInd = len(tMaximas)-4

        tMaxP = tMaximas[oscStartInd:oscEndInd+1]
        oscMaxP = oscMax[oscStartInd:oscEndInd+1]
        deltaP = deltaT[oscStartInd:oscEndInd+1]

        ## FIND MEAN ARTERIAL PRESSURE (MAP)
        argMax = np.argmax(oscMaxP)
        for i in range (0,len(self.t)):
            if self.t[i] == tMaxP[argMax]:
                aMAP = i
        pMAP = self.yfLP[aMAP]
        tMAP = tMaxP[argMax]
        
        ## FIND SYSTOLIC 
        searchSys = np.max(oscMaxP)*0.5 #ratio
        indS = np.argmax(oscMaxP > searchSys)
        dt = tMaxP[indS]-tMaxP[indS-1]
        dosc = oscMaxP[indS]-oscMaxP[indS-1]
        tM = (((searchSys-oscMaxP[indS-1])*dt/dosc)+tMaxP[indS-1])
        avPulse = np.average(deltaP)
        tS = tM - (avPulse/2)
        tE = tM + (avPulse/2)
        startSys = 0
        endSys = 0
        for i in range (0,len(self.t)):
            if self.t[i] >= tS and startSys==0:
                startSys=i
            elif self.t[i] >= tE and endSys==0:
                endSys=i

        ## FIND DIASTOLIC 
        searchDia = np.max(oscMaxP)*0.4 #ratio
        indD = argMax + np.argmax(oscMaxP[argMax:] < searchDia)
        dt = tMaxP[indD]-tMaxP[indD-1]
        dosc = oscMaxP[indD]-oscMaxP[indD-1]
        tM = (((searchDia-oscMaxP[indD-1])*dt/dosc)+tMaxP[indD-1])
        tS = tM - (avPulse/2)
        tE = tM + (avPulse/2)
        startDys = 0
        endDys = 0
        for i in range (0,len(self.t)):
            if self.t[i] >= tS and startDys==0:
                startDys=i
            elif self.t[i] >= tE and endDys==0:
                endDys=i

        #       start deflation        beatpoint                   oscilation start indx    pulse     map          systolic           diastolic      
        return [tPumpedUP,yPumpedUP], [tMaximas,yMaximas,oscMax], [oscStartInd,oscEndInd], [deltaP], [tMAP,pMAP], [startSys,endSys], [startDys,endDys]
        


    def plot(self):
        f, axes = plt.subplots(2)
        axes[0].plot(self.deflation[0], 
                             self.deflation[1], 
                             'o', label='Start Deflating', color='black')
        axes[0].plot(self.map[0], 
                       self.map[1], 
                       'X', label='MAP', color='red')
        axes[0].plot(self.t[self.systolic_index[0]:self.systolic_index[1]], 
                                  self.yfLP[self.systolic_index[0]:self.systolic_index[1]], 
                                  'o', label='Systolic Area', color='steelblue')
        axes[0].plot(self.t[self.diastolic_index[0]:self.diastolic_index[1]],
                                   self.yfLP[self.diastolic_index[0]:self.diastolic_index[1]], 
                                   'o', label='Diastolic Area', color='darkmagenta')
        axes[0].plot(self.t, self.yfLP, label='Low Pass Filter', color='dimgray')
        axes[0].legend(loc='upper right')


        axes[1].plot(self.t, self.yfHP, label='High Pass Filter', color='dimgray')
        axes[1].plot(self.oscilation[0], 
                                   self.oscilation[2], 
                                   'x', label='Oscilation Peak', color='black')
        axes[1].plot(self.oscilation[0][self.oscilation_index[0]:self.oscilation_index[1]], 
                              self.oscilation[2][self.oscilation_index[0]:self.oscilation_index[1]], 
                              'X', label='Measured Area', color='green')
        map_index = np.argmax(self.oscilation[2][self.oscilation_index[0]:self.oscilation_index[1]])
        axes[1].plot(self.oscilation[0][self.oscilation_index[0]:self.oscilation_index[1]][map_index], 
                              self.oscilation[2][self.oscilation_index[0]:self.oscilation_index[1]][map_index], 
                              'X', label='MAP Peak', color='red')
        axes[1].legend(loc='upper right')
        plt.show()


if __name__ == '__main__':
    tensimeter = Tensimeter()
    tensimeter.getResult()
    tensimeter.plot()
    