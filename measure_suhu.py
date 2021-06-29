from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np

terms = [
    -8.4014746232701378e+004,
     2.1739806157783503e+004,
    -2.3133737885459614e+003,
     1.3267940735230485e+002,
    -4.4588031827509482e+000,
     8.8188683424628669e-002,
    -9.5351532814659599e-004,
     4.3578741171212412e-006
]

def regress(x):
  t = 1
  r = 0
  for c in terms:
    r += c * t
    t *= x
  return r



class Suhu:    
    def __init__(self) :
        self.data = genfromtxt('mlx90614_data.csv', delimiter=',')
        self.t = self.data[:,0]
        self.raw_temperature = self.data[:,1]
        self.regress_temperature = regress(self.data[:,1])
        self.average = np.around(np.average(self.regress_temperature), decimals=2)

    def getResult(self):
        return self.average

    def plot(self):
        plt.plot(self.t,np.full(len(self.raw_temperature),self.average),color='blue',label='3) Average Body Temp')
        plt.plot(self.t,self.regress_temperature,color='red',label='2) Regress Body Temp')
        plt.plot(self.t,self.raw_temperature,color='black',label='1) Raw Body Temp')
        
        
        plt.legend(loc='upper right')
        plt.show()

if __name__ == '__main__':
    suhu = Suhu()
    print('AVG SUHU : ',suhu.getResult())
    suhu.plot()