
# 这个是将成都的数据集的txt文件转成gpx文件

def csv2gpx(outfilepath,i):
    f = open(path_in.format(i))
    lines = f.readlines()
    car_id = []
    time = []
    lat = []  # 纬度
    lon = []  # 经度
    for item in lines:
        line = item.split(',')
        car_id.append(line[0])
        t = line[5].split('/') #date
        t_0 = line[6]
        t = t[0]+'-0'+t[1]+'-'+t[2] + 'T' + t_0.strip('\n') + '+00:00'
        time.append(t)
        lon.append(line[3])  # 经度
        lat.append(line[2].strip('\n'))  # 纬度

    outstring = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    outstring += '<gpx xmlns="http://www.topografix.com/GPX/1/1" ' \
                 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
                 'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">'

    outstring += '<trk>\n<trkseg>\n'
    for i in range(len(lines)):
        item = '<trkpt lat="' + str(lat[i]) + '" lon="' + str(lon[i]) + '"><time>' + str(time[i]) + '</time></trkpt>'
        outstring = outstring + item + "\n"

    outstring += '</trkseg>\n</trk>\n</gpx>'

    fw = open(outfilepath, 'w')
    fw.write(outstring)
    fw.close()

# ------------------------------------------Test----------------------------------
def forfolders(i):
    csv2gpx(path_out.format(i),i)

path_in = '{}.txt'#排序后轨迹数据
path_out = 'traj_sim_gpx_{}.gpx'#gpx输出路径
for i in range(3,1000):
    forfolders(i)