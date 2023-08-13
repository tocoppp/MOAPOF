
# 这个函数是利用选择排序对文件进行排序
# 选择排序就是每轮都选择最小的那个放在第一个位置，然后循环
def sort_txt(k):
    f = open(path_in.format(k))
    lines = f.readlines()

    for i in range(len(lines)):

        min_idx = i
        for j in range(i + 1, len(lines)):
            time_1 = lines[min_idx].split(',')[4]
            time_2 = lines[j].split(',')[4]
            t_1 = lines[min_idx].split(',')[6]
            t_2 = lines[j].split(',')[6]
            if compare_big(t_1, t_2):
                min_idx = j
        lines[i], lines[min_idx] = lines[min_idx], lines[i]
    for i in range(len(lines)):
        with open(path_out.format(k), "a") as f:
            # 这里注意一下:不能写成了"w"，w每次都会覆盖前面写入的，a是每次都是追加
            f.write(lines[i])

    print("排序后的数组：")
    for i in range(len(lines)):
        print(lines[i])


# 这个函数是比较下面这样的数据结构的
# t1 = '21:18:46'
# t2 = '21:18:15'
# print(compare_big(t1, t2))
# 如果t1>t2，那么就输出True
def compare_big(t1, t2):
    t1 = t1.split(':')
    t2 = t2.split(':')
    hour1 = int(t1[0])
    hour2 = int(t2[0])
    minute1 = int(t1[1])
    minute2 = int(t2[1])
    second1 = int(t1[2])
    second2 = int(t2[2])
    if hour1 > hour2:
        return True
    if hour1 == hour2:
        if minute1 > minute2:
            return True
        if minute1 == minute2:
            if second1 > second2:
                return True
            if second1 < second2:
                return False
        if minute1 < minute2:
            return False
    if hour1 < hour2:
        return False

path_in='{}.txt'#单条轨迹数据
path_out='{}.txt'#排按时间排序后输出路径
for i in range(1,12000):
    sort_txt(i)