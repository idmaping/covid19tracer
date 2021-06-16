from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np

class Suhu:
    def __init__(self) :
        self.data = genfromtxt('mlx90614_data.csv', delimiter=',')
        self.t = self.data[:,0]
        self.temperature = self.data[:,1]
        self.average = np.around(np.average(self.temperature), decimals=2)

    def getResult(self):
        return self.average

    def plot(self):
        plt.plot(self.t,np.full(len(self.temperature),self.average),color='blue',label='average')
        plt.plot(self.t,self.temperature,color='black',label='body temp')
        plt.legend(loc='upper right')
        plt.show()

if __name__ == '__main__':
    suhu = Suhu()
    print('AVG SUHU : ',suhu.getResult())
    suhu.plot()