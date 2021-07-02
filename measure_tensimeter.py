from numpy import genfromtxt, typename
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from matplotlib.widgets import Slider

class Tensimeter:
    def __init__(self):
        self.titik_puncak = 160
        self.oscilating_factor = 0.5
        self.data = genfromtxt('adstensi_data.csv', delimiter=',')
        self.t = self.data[:,0] 
        self.ymmHg = self.normalize(arr = self.data[:,1], #Kalibrasi Manual TODO:COBA CARI DENGAN KALIBRASI DENGAN ALAT UKUR
                                   #t_min = 20100, 
                                   t_min = np.min(self.data[:,1]), 
                                   t_max = np.max(self.data[:,1]))
        #self.ymmHg = self.data[:,1]
        self.measure(self.t,self.ymmHg)

    def measure(self,t,ymmHg):
        ## FILTER
        fs = 100
        ### 5 Hz LP filter
        f5 = 5
        bLP, aLP = signal.butter(4, f5/fs*2, 'lowpass')
        yfLP = signal.lfilter(bLP, aLP, ymmHg)  
        ### 0.5 Hz HP filter
        f05 = self.oscilating_factor # TODO: might be better to set lower ~0.3
        bHP, aHP = signal.butter(4, f05/fs*2, 'highpass')
        yfHP = signal.lfilter(bHP, aHP, yfLP)
        yBP = yfLP - yfHP

        ## FINDING LOCAL MAXIMA
        localMax, _ = signal.find_peaks(yfHP, prominence = 0.3 )
        yMaximas = yfLP[localMax]
        tMaximas = t[localMax]
        oscMax = yfHP[localMax]
        xPumpedUp = np.argmax(yMaximas)
        yPumpedUP = yMaximas[xPumpedUp]
        tPumpedUP = tMaximas[xPumpedUp]

        ## FINDING LOCAL MINIMA
        localMin, _ = signal.find_peaks(-yfHP, prominence = 0.3 )
        yMinima = yfLP[localMin]
        tMinima = t[localMin]
        oscMin = yfHP[localMin]

        ## FINDING OSCILATION START AND END POINT
        deltaT = np.zeros(len(tMaximas))
        delta2T = np.zeros(len(tMaximas))
        validCnt = 0
        oscStartInd = 0
        oscEndInd = 0
        for i in range(1,len(tMaximas)-1):
            deltaT[i] = tMaximas[i]-tMaximas[i-1]
            delta2T[i] = deltaT[i]-deltaT[i-1]
            if oscStartInd == 0 :
                if np.abs(delta2T[i]) < 0.2 and i > (xPumpedUp) :
                    validCnt += 1
                    if validCnt == 5 :
                        oscStartInd = i - (validCnt-1)#) #-1)
                else:
                    validCnt = 0
            elif oscEndInd == 0: 
                if oscMax[i] < (oscMax[oscStartInd]*0.45) : 
                    oscEndInd = i -1
        if oscEndInd == 0:
            oscEndInd = len(tMaximas)-4
        
        ## FINDING TITIK MAXIMA
        tStart = tMaximas[oscStartInd]
        tEnd = tMaximas[oscEndInd]        
        tMaxP = tMaximas[oscStartInd:oscEndInd+1]
        oscMaxP = oscMax[oscStartInd:oscEndInd+1]
        
        ## FINDING TITIK MINIMA
        minStart = np.argmax(tMinima>tMaximas[oscStartInd])-1
        minEnd = np.argmax(tMinima>tMaximas[oscEndInd])
        tMinP = tMinima[minStart:minEnd+1]
        oscMinP = oscMin[minStart:minEnd+1]
        dMaxMin = oscMaxP - oscMinP[1:len(tMaxP)+1]
        
        '''
        ## OSCILATING AREA
        iStart = 0
        iEnd = 0
        for i in range(len(t)):
            if iStart == 0 and t[i] >= int(tStart):
                iStart = i
            if iEnd == 0 and t[i] >= int(tEnd):
                iEnd = i
        tP = t[iStart:iEnd+1]
        yhpP = yfHP[iStart:iEnd+1]
        ylpP = yfLP[iStart:iEnd+1]
        '''
        
        ## KITA BISA DAPET PULSE LOH DISINI TERNYATA
        deltaP = deltaT[oscStartInd:oscEndInd+1]
        avPulse = np.average(deltaP)
        self.pulse=60/avPulse
        #print("Pulse: ", np.around(pulse, decimals=1))

        ## FINDING MAP USING MAX POINT ONLY
        #MAPIndex = np.argmax(oscMaxP)
        MAPIndex = np.argmax(dMaxMin)
        
        ### FINDING SYSTOLIC
        SYSIndex = 0
        searchSys = np.max(oscMaxP)*0.3 #Ratio Sys
        for i in range(MAPIndex,0,-1):
            if oscMaxP[i] <= searchSys:
                SYSIndex = i
                break
        
        ### FINDING DIASTOLIC
        DYSIndex = MAPIndex
        searchDis = np.max(oscMaxP)*0.7 #0.9Ratio Dys
        for i in range(MAPIndex+1,len(oscMaxP)):
            if oscMaxP[i] <= searchDis:
                DYSIndex = i-1
                break        
        
        '''
        ### FINDING MAP USING MIN MAX POINT
        argMax = np.argmax(dMaxMin)
        for i in range(len(t)):
            if t[i] >= tMaxP[argMax]:
                tMAP = t[i]
                yMAP = yfLP[i]
                break
        print('MAP MIN MAX POINT',yMAP)

        ### FINDING MAP USING INTERPOLATION
        intMax = interp1d(tMaxP, oscMaxP, kind='linear')
        intMin = interp1d(tMinP, oscMinP, kind='linear')
        print(intMax(tP))
        omweInter = intMax(tP) - intMin(tP)
        pMAPinter = ylpP[np.argmax(omweInter)]
        print(pMAPinter)
        '''

        ## EXPORT TO GLOBAL VARIABLE FOR PLOTTING
        self.yfLP = yfLP
        self.tMaximas = tMaximas
        self.yMaximas = yMaximas
        self.tPumpedUP = tPumpedUP
        self.yPumpedUP = yPumpedUP
        self.oscStartInd = oscStartInd
        self.oscEndInd = oscEndInd
        self.MAPIndex = MAPIndex
        self.SYSIndex = SYSIndex
        self.DYSIndex = DYSIndex
        self.yfHP = yfHP
        self.oscMax = oscMax
        self.tMaxP = tMaxP
        self.oscMaxP = oscMaxP

    def getResult(self):
        pulse = np.around(self.pulse, decimals=2)
        map = np.around(self.yMaximas[self.oscStartInd:self.oscEndInd][self.MAPIndex], decimals=2)
        sys = np.around(self.yMaximas[self.oscStartInd:self.oscEndInd][self.SYSIndex], decimals=2)
        dys = np.around(self.yMaximas[self.oscStartInd:self.oscEndInd][self.DYSIndex], decimals=2)
        return pulse,map,sys,dys

    def normalize(self, arr, t_min, t_max):
        norm_arr = []
        for i in arr:
            temp = (i-t_min)/(t_max - t_min) * self.titik_puncak
            norm_arr.append(temp)
        return norm_arr

    def plot(self):
        f, axes = plt.subplots(2)
        axes[0].plot(self.t,self.yfLP,color='black',label='1) Read Data')
        axes[0].plot(self.tMaximas,self.yMaximas,'x',color='black',label='4) Peak Data')
        axes[0].plot(self.tPumpedUP,self.yPumpedUP,'o',color='darkorange',label='5) Deflating Point')
        axes[0].plot(self.tMaximas[self.oscStartInd:self.oscEndInd],self.yMaximas[self.oscStartInd:self.oscEndInd],'X',color='darkgreen',label='7) Process Data')
        axes[0].plot(self.tMaximas[self.oscStartInd:self.oscEndInd][self.MAPIndex],self.yMaximas[self.oscStartInd:self.oscEndInd][self.MAPIndex],'X',color='lime',label='9) MAP Data Point')
        axes[0].plot(self.tMaximas[self.oscStartInd:self.oscEndInd][self.SYSIndex],self.yMaximas[self.oscStartInd:self.oscEndInd][self.SYSIndex],'X',color='red',label='11) SYSTOLIC Data Point')
        axes[0].plot(self.tMaximas[self.oscStartInd:self.oscEndInd][self.DYSIndex],self.yMaximas[self.oscStartInd:self.oscEndInd][self.DYSIndex],'X',color='blue',label='13) DIASTOLIC Data Point')
        axes[0].legend(loc='upper right')
        
        axes[1].plot(self.t,self.yfHP,color='black',label='2) Delta Data')
        axes[1].plot(self.tMaximas,self.oscMax,'x',color='black',label='3) Peak Oscilation')
        axes[1].plot(self.tMaxP,self.oscMaxP,'X',color='darkgreen',label='6) Process Oscilating Area')
        axes[1].plot(self.tMaxP[self.MAPIndex],self.oscMaxP[self.MAPIndex],'X',color='lime',label='8) MAP Oscilation Point')
        axes[1].plot(self.tMaxP[self.SYSIndex],self.oscMaxP[self.SYSIndex],'X',color='red',label='10) SYSTOLIC Oscilation Point')
        axes[1].plot(self.tMaxP[self.DYSIndex],self.oscMaxP[self.DYSIndex],'X',color='blue',label='12) DIASTOLIC Oscillation Point')
        axes[1].legend(loc='upper right')

        plt.show()

if __name__ == '__main__':
    tensimeter = Tensimeter()
    pulse,map,sys,dys = tensimeter.getResult()
    print('PULSE : ',pulse)
    print('MAP : ',map)
    print('SYS : ',sys)
    print('DYS : ',dys)
    tensimeter.plot()
    