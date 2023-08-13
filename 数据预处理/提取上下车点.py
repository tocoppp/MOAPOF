import pandas as pd
import numpy as np
import datetime
path_in='{}.csv'#原始轨迹数据
path_out='{}.csv'#下车点数据输出路径

for i in range(1,2):
    f = open(path_in.format(i))
    data = pd.read_csv(f, names=['ID', 'lat', 'lon', 'passager', 'time', 'hour'])
    data['passager_1'] = data['passager'].shift(1)
    data['change'] = data['passager'] - data['passager_1']
    data = data.drop(['passager_1'], axis=1)  # axis=0 为删掉某行； axis=1位删掉某列
    data = data.loc[data['change'] == -1]
    data['time'] = pd.to_datetime(data['time'])
    # data = data.set_index('time')
    print(data.iloc[:, 0])
    # data.to_csv(path_out.format(i))


