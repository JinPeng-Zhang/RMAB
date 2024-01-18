'''
适配new wt-v2.1调度，txt文件格式为(S+1)*(M+1)*2的whittle-（S，lambda）映射对
'''

import numpy as np
import math
import os
pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
queuenum = 8
STATE_MAX = 24
d1 = 20000
d2 = 1000
lambda_min = 0.01
lambda_gap = 0.01
M = 70  ##来包率范围为lambda_min+1*lambda_gap~(M+1)*1*lambda_gap = 0.01~0.71
burst1 = [0,0,0,0,0,0,0,0]
burst2 = [0,0,0,0,0,0.45,0,0]

class queue_simulation():
    def __init__(self,pcome,STATE_MAX):
        self.STATE_MAX = STATE_MAX
        self.pcome =pcome
        self.queuenum = len(pcome)
        self.queue = np.zeros(len(pcome),dtype=int)
        self.drop = np.zeros(self.queuenum,dtype=int)
        self.time = 0
        self.path = file_path

    def inpacket(self):
        allpackets = []
        for q in range(self.queuenum):
            if q == 5 and 3000 < self.time < 3500:
                packets = self.random_packets(self.pcome[q]+0.45, q)
            else:
                packets = self.random_packets(self.pcome[q],q)
            allpackets.append(packets)
            self.queue[q] = self.queue[q] + packets
            if self.queue[q] > self.STATE_MAX:
                self.drop[q] = self.drop[q]+self.queue[q]-self.STATE_MAX
                self.queue[q] = self.STATE_MAX
        return allpackets

    '返回选择的一个发包队列'
    def outpacket(self,wt_txt):
        WI1 = self.getwhittle_to_use(wt_txt,burst1)  #上一时隙的wt------后续将替换为pcome1和pcome2
        WI2 = self.getwhittle_to_use(wt_txt,burst2)  #这一时隙的wt
        if 3000 < self.time < 3500:
            wi = WI2
        else:
            wi = WI1
        que = wi.index(max(wi))
        if self.queue[que] > 0:
            self.queue[que] = self.queue[que] -1
        else:
            que = 8
        #if (3000 < self.time < 4000):
        #    print('time:',self.time,'send:',que)
        #    print(wi)
        return que

    def run(self,times):
        wt_txt = getwhittle_from_txt(self.path)
        for t in range(times):
            action1 = self.outpacket(wt_txt)
            #print('send:::',action1)
            pp = self.inpacket()
            #print('come:::',pp)

            #if(3000 < t < 4000):
            #    print('ttt:::',t,'sss：：：',self.queue)
            self.time = self.time + 1
        print("drop_num:{}".format(self.drop))

    def random_packets(self,rate,queue):
        rad = np.random.rand()
        num = 0
        while rad>self.poission(num,expect=rate):
            rad = rad-self.poission(num,expect=rate)
            num = num +1
        return num

    def poission(self,k, expect=0.3):
        return expect ** k / math.factorial(k) * math.e ** (-expect)

    '从wt矩阵中查找数据'
    def getwhittle_to_use(self,wt_txt,burst):
        wt = []
        for q in range(queuenum):
            ss = self.queue[q]  #wt矩阵纵坐标
            m = int((self.pcome[q]-lambda_min)/lambda_gap) + 1  #wt矩阵横坐标
            # print(ss,m)
            # index = m * (STATE_MAX + 1) + ss
            # print(burst[q])
            m = m + int(burst[q]/lambda_gap)
            # print(ss, m)
            wtt = wt_txt[m][ss]
            wt.append(wtt)
        return wt

'获取符号sym在字符串str中的索引'
def getindex(str,sym):
    index = []
    for i in range(len(str)):
        if str[i]==sym:
            index.append(i)
    return index

'将txt中的whittle index转化为列表类型，返回直接使用的wt'
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

exp_times = 1000
drop_times = 0
drop_sums = 0
file_path = '/home/test/Desktop/RMAB/data/new-wt/' + 'd=' + str(d1) + '-' + str(d2) + '.txt'

for i in range(exp_times):
    qu = queue_simulation(pcome = pcome,STATE_MAX =STATE_MAX)
    print('第',i+1,'次：')
    qu.run(5000)
    newd = sum(qu.drop)
    if newd!=0:
        drop_times = drop_times + 1
        drop_sums = drop_sums + newd
print('丢包次数为：', drop_times, '平均丢包数为：', drop_sums / exp_times)