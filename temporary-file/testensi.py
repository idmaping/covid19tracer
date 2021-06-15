from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

#'''
def normalize(arr, t_min, t_max):
    norm_arr = []
    for i in arr:
        temp = (i-t_min)/(t_max - t_min) *200
        norm_arr.append(temp)
    return norm_arr
data = genfromtxt('adstensi_data.csv', delimiter=',')
data[:,1] = normalize(arr = data[:,1],t_min = np.min(data[:,1]),t_max = np.max(data[:,1])) 
fs= 50 # Hz
resolution = 24 # bits
N = len(data)
T = 1/fs
bin_size = fs/N 
ymmHg = data[:,1]
t = data[:,0] 
'''
data = np.loadtxt('sample_07_07.dat')
fs= 1000 # Hz
resolution = 24 # bits
N = len(data)
T = 1/fs
bin_size = fs/N 
y1 = data[:,1]
t = data[:,0] 
# convert data
vmin = -1.325
vmax = +1.325
xmax = (2**24 -1)
# Choose data set to work with and convert to voltage
if np.max(y1) > vmax:
    #for raw data: 
    y = ((y1 * (vmax-vmin) / xmax ) + vmin) 
    t = t/1000
else:
    y = y1 #for raw data: ((y1 * (vmax-vmin) / xmax ) + vmin) 
ambientV = 0.710#0.675 # from calibration
mmHg_per_kPa = 7.5006157584566 # from literature
kPa_per_V = 50 # 20mV per 1kPa / 0.02 or * 50 - from sensor datasheet
corrFact = 2.50 # from calibration
ymmHg = (y - ambientV)  * mmHg_per_kPa * kPa_per_V * corrFact
'''

## FILTER
# 5 Hz LP filter
f5 = 5#20
bLP, aLP = signal.butter(4, f5/fs*2, 'lowpass')
yfLP = signal.lfilter(bLP, aLP, ymmHg)
# 0.5 Hz HP filter
f05 = .5#9 # TODO: might be better to set lower ~0.3
bHP, aHP = signal.butter(4, f05/fs*2, 'highpass')
yfHP = signal.lfilter(bHP, aHP, yfLP)
f5 = .8
bLLP, aLLP = signal.butter(4, f5/fs*2, 'lowpass')
yfLLP = signal.lfilter(bLLP, aLLP, ymmHg)
yfBP = yfLP-yfHP

## FINDING START MEASURE POINT
localMax, _ = signal.find_peaks(yfHP, prominence = .3 ) 
yMaximas = yfBP[localMax]
tMaximas = t[localMax]
# the local max values of the oscillation
oscMax = yfHP[localMax]
# get indice of overal max pressure 
xPumpedUp = np.argmax(yMaximas)
# the pressure that was pumped up to
yPumpedUP = yMaximas[xPumpedUp]
# the start time of the deflation 
tPumpedUP = tMaximas[xPumpedUp]

localMin, _ = signal.find_peaks(-yfHP, prominence = .3 )
# get values of local maximas in pressure and time
yMinima = yfBP[localMin]
tMinima = t[localMin]
# the local max values of the oscillation
oscMin = yfHP[localMin]

deltaT = np.zeros(len(tMaximas))
delta2T = np.zeros(len(tMaximas))
validCnt = 0
oscStartInd = 0
oscEndInd = 0

deltaTtest = np.diff(tMaximas)
for i in range(1,len(tMaximas)-1):
    deltaT[i] = tMaximas[i]-tMaximas[i-1]
    delta2T[i] = deltaT[i]-deltaT[i-1]
    if oscStartInd == 0 :
        # check for start of oscillogram: 
        if np.abs(delta2T[i]) < 0.2 and i > xPumpedUp :
            validCnt += 1
            if validCnt == 5 : #calibration factor for sys
                oscStartInd = i - (validCnt-1)
        else:
            validCnt = 0
    elif oscEndInd == 0:    
        if (oscMax[oscStartInd]*1.2) > oscMax[i]: #calibration factor for dias
            oscEndInd = i-3
            
if oscEndInd == 0:
    oscEndInd = len(tMaximas)-4

## PROCESSING
tStart = tMaximas[oscStartInd]
tEnd = tMaximas[oscEndInd]
iStart = int(tStart*1000)
iEnd = int(tEnd*1000)
tMaxP = tMaximas[oscStartInd:oscEndInd+1]
oscMaxP = oscMax[oscStartInd:oscEndInd+1]
deltaP = deltaT[oscStartInd:oscEndInd+1]
deltaPtest = deltaTtest[oscStartInd:oscEndInd+1]
tP = t[iStart:iEnd+1]
yhpP = yfHP[iStart:iEnd+1]
ylpP = yfLP[iStart:iEnd+1]
minStart = np.argmax(tMinima>tMaximas[oscStartInd])-1
minEnd = np.argmax(tMinima>tMaximas[oscEndInd])
tMinP = tMinima[minStart:minEnd+1]
oscMinP = oscMin[minStart:minEnd+1]

dMaxMin = oscMaxP - oscMinP[1:len(tMaxP)+1]

## FIND PULSE
avPulse = np.average(deltaP)
pulse=60/avPulse
print("Pulse: ", np.around(pulse, decimals=1))

## FIND MAP
argMax = np.argmax(oscMaxP)
for i in range (0,len(t)):
    if t[i] == tMaxP[argMax]:
        aMAP = i
pMAP = yfLP[aMAP]
tMAP = tMaxP[argMax]
print("MAP (max value): ", np.around(pMAP, decimals=2))

## FIND SYSTOLIC
searchSys = np.max(oscMaxP)*0.5
indS = np.argmax(oscMaxP > searchSys)
dt = tMaxP[indS]-tMaxP[indS-1]
dosc = oscMaxP[indS]-oscMaxP[indS-1]
tM = (((searchSys-oscMaxP[indS-1])*dt/dosc)+tMaxP[indS-1])
tS = tM - (avPulse/2)
tE = tM + (avPulse/2)
startSys = 0
endSys = 0
for i in range (0,len(t)):
    if t[i] >= tS and startSys==0:
        startSys=i
    elif t[i] >= tE and endSys==0:
        endSys=i
pSBPmax = np.average(yfLP[startSys:endSys])

## FIND DIASTOLIC
searchDia = np.max(oscMaxP)*0.4
indD = argMax + np.argmax(oscMaxP[argMax:] < searchDia)
dt = tMaxP[indD]-tMaxP[indD-1]
dosc = oscMaxP[indD]-oscMaxP[indD-1]
# pDBPmax = yfLP[int(round((((searchDia-oscMaxP[indD-1])*dt/dosc)+tMaxP[indD-1])*1000))]
tM = (((searchDia-oscMaxP[indD-1])*dt/dosc)+tMaxP[indD-1])
tS = tM - (avPulse/2)
tE = tM + (avPulse/2)
startDys = 0
endDys = 0
for i in range (0,len(t)):
    if t[i] >= tS and startDys==0:
        startDys=i
    elif t[i] >= tE and endDys==0:
        endDys=i
pDBPmax = np.average(yfLP[startDys:endDys])

print(pSBPmax,pDBPmax)

plt.subplot(2, 1, 1)
#plt.plot(t,ymmHg)
plt.plot(t,yfLP,color='black')
#plt.plot(tMinima,yMinima,'X', color='black')
#plt.plot(tMaximas,yMaximas,'x', color='red')
plt.plot(tPumpedUP,yPumpedUP,'o', color='green')
plt.plot(tMAP,pMAP,'X', color='red')
#plt.plot(t,yPumpedUP,'o', color='green')

plt.subplot(2, 1, 2)
plt.plot(t,yfHP,color='black')
plt.plot(tMaximas,oscMax,'x', color='orange')
plt.plot(tMaximas,delta2T,color='blue')
plt.plot(tMaxP,oscMaxP,'X', color='green')
#plt.plot(tMaxP,deltaPtest,color='green')






plt.show()