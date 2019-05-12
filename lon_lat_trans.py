import pandas as pd
import numpy as np
import math
import openpyxl
def va_trans():
    file_path = "./飞机数据/"
    file_name = "无人机.xlsx"
    va_data = pd.read_excel(file_path+file_name)
    distance_values = va_data["距离"].values
    orientation_values = va_data["方位"].values
    pitch_values= va_data["俯仰"].values
    va_Lon_list = []
    va_Lat_list = []
    va_Hei_list = []
    for i  in range(len(distance_values)):
        orientation = (orientation_values[i]*360)/6000
        pitch = (pitch_values[i]*360)/6000
        distance = distance_values[i]
        lfRadarL = 104
        lfRadarM = 30
        lfRadarH = 500
        Pi = 3.1415926
        a_global = 6378137.000
        b_global = 6356752.314
        e  = 0.0818191908426
        #目标在雷达地理坐标系下的坐标为x, y, z;
        x = distance * np.cos(pitch * Pi / 180) * np.cos(orientation * Pi / 180)
        y = distance * np.cos(pitch * Pi / 180) * np.sin(orientation * Pi / 180)
        z = -distance * np.sin(pitch * Pi / 180)
        #目标在84空间直角坐标系中的坐标X84, Y84, Z84，下面将雷达地理坐标系下的坐标为x, y, z转为84坐标;
        #地球卯酉曲率半径N；
        cosLr = np.cos(lfRadarL * Pi / 180)
        sinLr = np.sin(lfRadarL * Pi / 180)
        cosMr = np.cos(lfRadarM * Pi / 180)
        sinMr = np.sin(lfRadarM * Pi / 180)
        N = a_global / np.sqrt(1 - e * e * sinMr * sinMr);
        X84 = - x * sinMr * cosLr- y * sinLr - z * cosMr * cosLr+ (N + lfRadarH) * cosMr * cosLr
        Y84 = -x * sinMr * sinLr+ y * cosLr - z * cosMr * sinLr+ (N + lfRadarH) * cosMr * sinLr
        Z84 = x * cosMr - z * sinMr +(N * (1 - e * e) + lfRadarH) * sinMr
        #下面将目标的84直角坐标转换84地理坐标
        if (X84 >= 0):
            lfTargetL = (math.atan(Y84 / X84)) * 180 / Pi
        if (X84 <= 0 and Y84 >= 0):
            lfTargetL = (Pi + math.atan(Y84 / X84)) * 180 / Pi
        if (X84 <= 0 and Y84 <= 0):
            lfTargetL = (-Pi + math.atan(Y84 / X84)) * 180 / Pi
        #目标纬度和高度用叠代法：
        ncount = 0 #累积循环次数
        #坐标变换中间量
        sqrtXY = np.sqrt(X84 * X84 + Y84 * Y84)
        N0 = a_global
        H0 = np.sqrt(float(X84 * X84 + Y84 * Y84 + Z84 * Z84)) - np.sqrt(float(a_global * b_global))
        M0 = math.atan(Z84 / sqrtXY * 1 / (1 - e * e * N0 / (N0 + H0)))
        Error_M = 4.848136811095e-9 #计算误差0.001秒, 对应距离误差0.03米
        Error_H = 0.001 #高度计算误差0.001米
        M840 = M0
        H840 = H0
        while True:
            sinM840 = np.sin(M840);
            N841 = a_global / np.sqrt(1 - e * e * sinM840 * sinM840);
            H841 = sqrtXY / np.cos(M840) - N841;
            M841 = math.atan(Z84 / sqrtXY * 1 / (1 - e * e * N841 / (N841 + H841)));
            dlM84 = np.fabs(M841 - M840);
            dlH84 = np.fabs(H841 - H840);
            ncount += 1
            if (dlM84 > Error_M or dlH84 > Error_H):
                M840 = M841
                H840 = H841
            if (not((dlM84 > Error_M or dlH84 > Error_H) and ncount < 5)):
                break
        #最终输出84坐标
        lfTargetM = M841 * 180 / Pi
        lfTargetH = H841
        va_Lon_list.append(lfTargetL)
        va_Lat_list.append(lfTargetM)
        va_Hei_list.append(lfTargetH)
    return va_Lon_list,va_Lat_list,va_Hei_list
def drone_trans():
    file_path = "./飞机数据/"
    file_name = "民航飞机.xlsx"
    drone_data = pd.read_excel(file_path + file_name)
    x_values = drone_data["X"].values
    y_values = drone_data["Y"].values


    PI = 3.1415926
    m_RadarHei,m_Hei,m_Lon,m_Lat,m_latcos,m_latsin,m_longcos,m_longsin = InitRadarPara()
    RHei = m_RadarHei
    RLat = m_Lat / 180.0 * PI
    RLon = m_Lon / 180.0 * PI
    RLatCos = m_latcos
    RLatSin = m_latsin


    drone_Lon_list = []
    drone_Lat_list = []
    for x_value,y_value in zip(x_values,y_values):
        templong = RLon
        Px = x_value
        Py = y_value
        if Px == 0:
                m_LLPos_Lon = m_Lon
        else:
            templong += math.atan(4 * RHei * Px / ((4 * RHei * RHei - Px * Px - Py * Py) * RLatCos - 4 * RHei * Py * RLatSin))
            m_LLPos_Lon = templong * 180.0 / PI
        templong -= RLon
        if Px != 0:
            m_LLPos_Lat = math.atan(Py * np.sin(templong) / (Px * RLatCos) + np.tan(RLat) * np.cos(templong)) * 180.0 / PI
        else:
            m_LLPos_Lat = m_Lat + 180.0 / PI * math.asin(4 * RHei * Py / (4 * RHei * RHei + Py * Py))

        drone_Lon_list.append(m_LLPos_Lon)
        drone_Lat_list.append(m_LLPos_Lat)
    return drone_Lon_list,drone_Lat_list


def InitRadarPara():
    Radar_palne_Lon = 110.3057
    Radar_palne_Lat = 21.178
    Radar_palne_Hei = 149
    Pi = 3.1415926
    ErthRO = 6378.137   #地球赤道参考半径
    EARTH_RADIUS_METER = ErthRO * 1000
    EibSiLon = 0.0818191    #地球第一偏心率
    m_Hei = Radar_palne_Hei
    m_Lon = Radar_palne_Lon
    m_Lat = Radar_palne_Lat

    Lat = Radar_palne_Lat * Pi / 180.0
    Lon = Radar_palne_Lon * Pi / 180.0

    m_latcos = np.cos(Lat)
    m_latsin = np.sin(Lat)
    m_longcos = np.cos(Lon)
    m_longsin = np.sin(Lon)

    medval = EibSiLon * EibSiLon
    m_Radius = EARTH_RADIUS_METER * np.sqrt(1 - medval * m_latsin * m_latsin)
    m_RadarHei = m_Radius + m_Hei
    return m_RadarHei,m_Hei,m_Lon,m_Lat,m_latcos,m_latsin,m_longcos,m_longsin

def write_excel():
    wb = openpyxl.Workbook()
    wb.get_sheet_names()
def va_data_write(va_Lon_list,va_Lat_list,va_Hei_list):
    drone_data = [[i,j,k] for i,j,k in zip(va_Lon_list,va_Lat_list,va_Hei_list)]
    va_data_df = pd.DataFrame(drone_data)
    va_data_df.columns = ["Longtitude", "Latitude", "Height"]
    writer = pd.ExcelWriter("无人机经度纬度高度.xlsx")
    va_data_df.to_excel(writer, "page1")
    writer.save()
def drone_data_write(drone_Lon_list,drone_Lat_list):
    drone_data = [[i,j] for i,j in zip(drone_Lon_list,drone_Lat_list)]
    drone_data_df = pd.DataFrame(drone_data)
    drone_data_df.columns = ["Longtitude", "Latitude"]
    writer = pd.ExcelWriter("民航飞机经度纬度.xlsx")
    drone_data_df.to_excel(writer, "page1")
    writer.save()
if __name__ =='__main__':
    va_Lon_list,va_Lat_list,va_Hei_list = va_trans()
    drone_Lon_list,drone_Lat_list = drone_trans()
    va_data_write(va_Lon_list,va_Lat_list,va_Hei_list)
    drone_data_write(drone_Lon_list,drone_Lat_list)