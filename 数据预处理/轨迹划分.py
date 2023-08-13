import pandas as pd
import sys
import os


path_1='.csv'#原始轨迹数据
path_2='.csv'#下车点数据
path_out='.txt'#单条轨迹数据

for i in range(1,2):
    f = open(path_1.format(i))
    data = pd.read_csv(f, names=['ID', 'lat', 'lon', 'passager', 'time', 'hour'])
    f1=open(path_2.format(i))
    data1=pd.read_csv(f1, names=['no','ID', 'lat', 'lon', 'passager', 'time', 'hour','change'])
    num=data1['no']
    for j in range(1,len(num)):
    # for j in range(1, 2):
        a=int(num[j])
        b=int(num[j+1])
        log=data.loc[a:b]
        print(log)
            # print(pd.DataFrame(log))
        log.to_csv(path_out.format(j),header=False)



