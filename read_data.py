import pandas as pd
import numpy as np
global data_size
data_size = 10000
def read_data(filename):
    file_path = "./data/"
    data = pd.read_excel(file_path+filename)
    data_values = data.values
    return data_values
def get_data():
    va_data = read_data("无人机.xlsx")[:data_size]
    drone_data = read_data("民航飞机.xlsx")[0:data_size]
    data = np.concatenate((va_data,drone_data),axis=0)
    return data
def get_label():
    va_label = np.array([np.array([0,1]) for i in range(data_size)])
    drone_label = np.array([np.array([1,0]) for i in range(data_size)])
    label = np.concatenate((va_label,drone_label),axis=0)
    return label
def get_data_label():
    data = get_data()
    label = get_label()
    return data,label
if __name__ == '__main__':
    get_data_label()