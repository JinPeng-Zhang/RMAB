'可对txt文件的wt进行升序检测，并判断两个wt是否一致（判断收敛性）'
import numpy as np

STATE_MAX = 24
M = 110
burst1 = [0,0,0,0,0,0,0,0]
burst2 = [0,0,0,0,0,0.45,0,0]

def getwhittle_from_txt(file_path):
    wt = []
    with open(file_path, 'r') as file:
        wt2 = file.read()
    a = getindex(wt2, ',')
    b = getindex(wt2, '[')
    c = getindex(wt2, ']')
    b = b[1:]  #去掉第一个[
    c = c[0:-1]  #去掉最后一个]
    for k in range(M+1):
        wtt = []
        leftb = b[k] + 1  # 第一个开头
        rightb = a[(STATE_MAX+1) * k]  # 第一个结尾
        numstr = wt2[leftb:rightb]
        num = float(numstr)
        wtt.append(num)
        for j in range(STATE_MAX-1):
            left = a[j + (STATE_MAX+1) * k] + 2
            right = a[j + 1 + (STATE_MAX+1) * k]
            numstr = wt2[left:right]
            num = float(numstr)
            wtt.append(num)
        leftl = a[(STATE_MAX+1) * k + STATE_MAX-1] + 2  # 最后一个开头
        rightl = c[k]  # 最后一个结尾
        numstr = wt2[leftl:rightl]
        num = float(numstr)
        wtt.append(num)
        wt.append(wtt)
    return wt

def getindex(str,sym):
    index = []
    for i in range(len(str)):
        if str[i]==sym:
            index.append(i)
    return index

path1 = 'C:/Users/48935/Desktop/data/new-wt/d=20000-1000-longstep.txt'
path2 = 'C:/Users/48935/Desktop/data/new-wt/d=20000-1000.txt'
wt = getwhittle_from_txt(path1)
wtt = getwhittle_from_txt(path2)

s_not_increase_flag = 0
lam_not_increase_flag = 0
wt_equal_wtt_flag = 0


for s in range(STATE_MAX):
    for lam in range(M):
        if(wt[lam][s] > wt[lam+1][s]):
            lam_not_increase_flag = 1
            #print(s,lam)
            #print(wt[lam][s],wt[lam+1][s])
            #print('-------------')

for lam in range(M + 1):
    for s in range(STATE_MAX - 1):
        if (wt[lam][s] > wt[lam][s+1]):
            s_not_increase_flag = 1
            #print(s, lam)
            #print(wt[lam][s], wt[lam][s+1])
            #print('-------------')

for s in range(STATE_MAX+1):
    for lam in range(M+1):
        if(wt[lam][s] != wtt[lam][s]):
            wt_equal_wtt_flag = 1
            print(s,lam)
            print(wt[lam][s],wtt[lam][s])

#print(s_not_increase_flag)
#print(lam_not_increase_flag)
print(wt_equal_wtt_flag)