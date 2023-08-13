# -*- coding: utf-8 -*-
import gc
import os.path
import time
from collections import namedtuple, defaultdict
from scipy.spatial import distance
import fiona
import pandas as pd
from pyproj import Proj
import gpxpy.parser as parser
import datetime
import shapefile
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

TrackRec = namedtuple('TrackRec', ['x', 'y', 'object_id', 'taxi_id', 'log_time'])
POI=namedtuple("poi",["name","leibie","p_x","p_y","area","num"])

def get_time_stamp(result):
# 日期+时间转时间戳
    local_date = result + datetime.timedelta(hours=0)#加上时区
    local_date_srt = datetime.datetime.strftime(local_date,"%Y-%m-%d %H:%M:%S.%f")#2020-12-01 11:21:57.330000
    time_array1 = time.mktime(time.strptime(local_date_srt,"%Y-%m-%d %H:%M:%S.%f"))#1606792917.0
    return time_array1

def read_track(gpx_path):
#读取轨迹数据
    gpx_file = open(gpx_path,'r')  # 读取文件
    gpx_parser = parser.GPXParser(gpx_file)
    gpx = gpx_parser.parse()  # 文件解析
    gpx_file.close()

    taxi_id_logs = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                log = []
                log.append(point.latitude)
                log.append(point.longitude)
                log.append(point.time)
                if type(log[2]) == datetime.datetime:
                    log[2] = int(get_time_stamp(log[2]))
                    # log[2] = int(log[2].timestamp())
                taxi_id_logs.append(log)
    return taxi_id_logs[-1]



def read_poi(path):
# 读取poi
    df = pd.read_csv(path, encoding="utf-8")
    poi_list = df.values.tolist()
    print(poi_list)
    return poi_list
    # 读取poi
    # num = 1
    # poi_id_logs = defaultdict(list)
    # df = pd.read_csv(path, encoding="utf-8")
    # for i in range(5):
    #     name = df.iloc[i, 0]
    #     leibie = df.iloc[i, 1]
    #     p_x = df.iloc[i, 2]
    #     p_y = df.iloc[i, 3]
    #     area = df.iloc[i, 4]
    #     poi_id_logs[i].append(
    #         POI(
    #             name,
    #             leibie,
    #             p_x,
    #             p_y,
    #             area,
    #             num,
    #         ))
    #     num += 1
    # return poi_id_logs

def choose_poi(t,poi_list):
#选取候选poi
    num=0
    poi_s = []
    drop=[]
    # 首先定义要转换的投影坐标系
    proj1 = Proj("epsg:2383")
    '''
    epsg编号通过epsg官网或者arcmap中查询获得，此为WGS 84 / UTM zone 1N投影
    或者p1 = Proj('+proj=utm +zone=1 +datum=WGS84 +units=m +no_defs')
    '''
    lon2, lat2 = proj1(t[1], t[0])
    drop.append(lon2)
    drop.append(lat2)
    print(drop)
    # for i in range(0, len(point_logs)):
    #     t = point_logs[i]
    for i in range(0,len(poi_list)):
        p = poi_list[i]
        poi_logs = []
        lon1, lat1 = proj1(p[2], p[3])  # 将地理坐标转换为投影坐标，地理坐标为WGS84下的坐标

        poi_logs.append(lon1)
        poi_logs.append(lat1)

        # print(poi_logs)
        d = distance.euclidean(drop, poi_logs)

        if d <= 200:
            print(d)
            poi_s.append(p)
            num += 1
        else:
            continue
    return poi_s,num

def time_para(time):
#时间权重设置，可根据设定改变
    w = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # 餐饮美食 公司企业 购物消费 交通设施 金融机构 酒店住宿 科教文化 旅游景点 商务住宅 生活服务 休闲娱乐 医疗保健 运动健身
    t1=int(datetime.datetime(2014, 8, 23, 7, 0, 0).timestamp())
    t2=int(datetime.datetime(2014, 8, 23, 9, 0, 0).timestamp())
    t3=int(datetime.datetime(2014, 8, 23, 11, 0, 0).timestamp())
    t4=int(datetime.datetime(2014, 8, 23, 14, 0, 0).timestamp())
    t5=int(datetime.datetime(2014, 8, 23, 17, 0, 0).timestamp())
    t6=int(datetime.datetime(2014, 8, 23, 19, 0, 0).timestamp())
    t7=int(datetime.datetime(2014, 8, 23, 21, 0, 0).timestamp())
    # 7:00-9:00
    print(time)
    if t1 < time < t2:
        w[1] = w[6] = 0.4
        w[3] = w[11] = 0.2
    # 9:00-11:00
    elif t2 < time < t3:
        w[2] = w[3] = w[9] = 0.25
        w[11] = 0.07
        w[0] = w[1] = w[4] = w[5] = w[6] = w[7] = w[8] = w[10] = w[12] = 0.02
    # 11:00-14:00
    elif t3 < time < t4:
        w[3] = w[11] = 0.04
        w[0] = w[2] = w[1] = w[9] = 0.195
        w[4] = w[5] = w[6] = w[7] = w[8] = w[10] = w[12] = 0.02
    # 14:00-17:00
    elif t4 < time < t5:
        w[2] = w[3] = w[9] = 0.25
        w[11] = 0.07
        w[0] = w[1] = w[4] = w[5] = w[6] = w[7] = w[8] = w[10] = w[12] = 0.02
    # 17:00-19:00
    elif t5 < time < t6:
        w[0] = w[2] = w[5] = w[6] = w[8] = w[9] = 0.15
        w[3] = 0.06
        w[7] = w[10] = w[12] = 0.01
    # 19:00-21:00
    elif t6 < time < t7:
        w[0] = w[2] = w[5] = w[8] = w[10] = w[9] = 0.155
        w[3] = 0.06
        w[12] = 0.01
    else:
        w[5] = w[8] = 0.46
        w[3] = w[10] = 0.04
    print("w=", w)
    return w


def gravity(poi,w):
#重要参数统计
    category = [121721, 60533, 182257, 40137, 7076, 17231, 25995, 2997, 22738, 88969, 10004, 28541, 6957]
    poi_num = poi[1]
    rou = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    c = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ca_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    G = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, poi_num):
        if poi[0][i - 1][1] == '餐饮美食':
            ca_num[0] += 1
        elif poi[0][i - 1][1] == '公司企业':
            ca_num[1] += 1
        elif poi[0][i - 1][1] == '购物消费':
            ca_num[2] += 1
        elif poi[0][i - 1][1] == '交通设施':
            ca_num[3] += 1
        elif poi[0][i - 1][1] == '金融机构':
            ca_num[4] += 1
        elif poi[0][i - 1][1] == '酒店住宿':
            ca_num[5] += 1
        elif poi[0][i - 1][1] == '科教文化':
            ca_num[6] += 1
        elif poi[0][i - 1][1] == '旅游景点':
            ca_num[7] += 1
        elif poi[0][i - 1][1] == '商务住宅':
            ca_num[8] += 1
        elif poi[0][i - 1][1] == '生活服务':
            ca_num[9] += 1
        elif poi[0][i - 1][1] == '休闲娱乐':
            ca_num[10] += 1
        elif poi[0][i - 1][1] == '医疗保健':
            ca_num[11] += 1
        elif poi[0][i - 1][1] == '运动健身':
            ca_num[12] += 1
    print(ca_num)
    sum = 0
    for i in range(-1, 12):
        rou[i] = 100 * ca_num[i] / category[i]
        sum += rou[i]
    for i in range(-1, 12):
        c[i] = 100 * rou[i] / sum
        G[i]=c[i]*w[i]
    I=G.index(max(G))
    poi_type = ['餐饮美食', '公司企业', '购物消费', '交通设施', '金融机构', '酒店住宿', '科教文化', '旅游景点', '商务住宅', '生活服务', '休闲娱乐', '医疗保健', '运动健身']
    global last_poi
    last_poi = poi_type[I]
    print(rou)
    print(sum)
    print(c)
    print("G=",G)
    #print(last_poi)

if __name__ == '__main__':
    gpx_path='.result/traj_sim_gpx_{}.gpx.res.gpx'#匹配后轨道数据
    poi_list=read_poi(r'POI数据.csv')#poi点数据
    #下车点经纬度提取
    # point_logs=[]
    # time=[]
    l_p = []
    # for taxi_id, logs in a.items():
    #     for log in logs:
    #         point = []
    #         point.append(log.x)
    #         point.append(log.y)
    #         point_logs.append(point)
    #         time.append(log.log_time)
    # print(point_logs)
    # print(time)
    #遍历下车点进行筛选poi
    for i in range(1,11747):
        try:
            t = read_track(gpx_path.format(i))
            print(t)
            # t=point_logs[i]
            p = choose_poi(t, poi_list)
            print(p)
            w = time_para(t[2])  # 时间权重计算,参数为时间
            gravity(p, w)
            l_p.append(last_poi)
        except OSError:
            pass
        except ZeroDivisionError:
            pass
    print(l_p)
    result = pd.value_counts(l_p, ascending=True, normalize=True)
    result.to_csv(r"RESULT.CSV")#结果输出路径


