import csv
import numpy as np
import cv2

class knn:
    def __init__(self):
        self.kelas = []
        self.measure = []
        self.kNearest = cv2.ml.KNearest_create()
    
    def generate_dataset(self,file="dummy_dataset.csv"):
        kelas = []
        measure = []
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            index = 0
            for row in csv_reader:
                if index == 0:
                    index +=1
                else:            
                    kelas.append(ord(row[8])) #separate class
                    row[2] = ord(row[2]) #get jenis kelamin and convert to ascii
                    measure.append(row[1:8]) #bypass NO coloum
                    index +=1
        kelas=np.array(kelas,np.float32)
        measure=np.array(measure,np.float32)
        np.savetxt("class.txt", kelas)
        np.savetxt("measure.txt", measure)

    def initialize(self,kelas_file="class.txt",measure_file="measure.txt"):
        self.kelas = np.loadtxt(kelas_file, np.float32)
        self.measure = np.loadtxt(measure_file, np.float32)
        self.kelas = self.kelas.reshape((self.kelas.size, 1))      
        self.kNearest.train(self.measure, cv2.ml.ROW_SAMPLE, self.kelas)


    def predict(self,umur=20,jenis_kelamin=ord("L"),suhu=36,spo2=95,detak_jantung=70,systole=120,diastole=60,k=5):
        in_measure = [[umur,jenis_kelamin,suhu,spo2,detak_jantung,systole,diastole]]
        in_measure = np.float32(in_measure)
        retval, results, neigh_resp, dists = self.kNearest.findNearest(in_measure, k = k)              
        results = str(chr(int(results[0][0])))
        return retval, results, neigh_resp, dists

if __name__=="__main__":
    knn = knn()
    
    #knn.generate_dataset(file='datasetRST.csv') #UNTUK DATASET RST
    knn.generate_dataset() #UNTUK DUMMY RST
    
    
    
    #knn.initialize()
    #retval, result, neigh_resp, dists = knn.predict()
    
       
    
    