import numpy as np
import pandas as pd
import re
import os


def va_data_to_excel(file_path):
    X = []
    Y = []
    hei = []
    speed = []
    direction = []
    va_data_frame = pd.DataFrame()
    files_name = os.listdir(file_path)
    for file_name in (files_name):
        with open(file_path+file_name,"r",encoding="GB2312") as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                if "X:" in line and "Y:" in line and "hei:" in line and "航速:" in line and "航向:" in line:
                    x_index = line.index("X:")
                    y_index = line.index("Y:")
                    hei_index = line.index("hei:")
                    speed_index = line.index("航速:")
                    direction_index = line.index("航向:")
                    X.append(float(line[x_index+1]))
                    Y.append(float(line[y_index+1]))
                    hei.append(float(line[hei_index+1]))
                    speed.append(float(line[speed_index+1]))
                    direction.append(int(line[direction_index+1]))
    va_data_frame["X"] = X
    va_data_frame["Y"] = Y
    va_data_frame["hei"]  = hei
    va_data_frame["speed"] = speed
    va_data_frame["航向"] = direction
    va_data_frame.to_excel(file_path+"民航.xlsx")

def drone_data_to_excel(file_path):
    files_name = os.listdir(file_path)
    distance = []
    orientation = []
    更好玩12 = []
    speed = []
    direction = []
    drone_data_frame = pd.DataFrame()
    for file_name in (files_name):
        with open(file_path+file_name,"r",encoding="GB2312") as f:
            lines = f.readlines()
            if "航向" in lines[0]:
                for line in lines[1:]:
                    line = line.split()
                    distance.append(float(line[2]))
                    orientation.append(float(line[3]))
                    pitch.append(float(line[4]))
                    speed.append(float(line[5]))
                    direction.append(int(line[6]))
    drone_data_frame["距离"] = distance
    drone_data_frame["方位"] = orientation
    drone_data_frame["俯仰"] = pitch
    drone_data_frame["speed"] = speed
    drone_data_frame["航向"] = direction
    drone_data_frame.to_excel(file_path+"无人机.xlsx")



if __name__ =='__main__':
    drone_file_path = "./飞机数据/无人机/"
    va_file_path = "./飞机数据/民航/"
    #预处理数据，将需要的无人机关键数据提取出来存在excel表格里面
    print("开始预处理无人机数据...")
    drone_data_to_excel(drone_file_path)
    print("无人机数据处理Finished")
    #预处理数据，将需要的民航关键数据提取出来存在excel表格里面
    print("开始预处理民航数据...")
    va_data_to_excel(va_file_path)
    print("民航数据处理Finished")


