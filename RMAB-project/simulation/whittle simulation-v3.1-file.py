'''
文件式whittle
'''

import numpy as np
import math
import  matplotlib.pyplot as plt
import os
pcome = ...
queuenum = 8
STATE_MAX = 25

class queue_simulation():
    def __init__(self,pcome,STATE_MAX,WI1,WI2):
        self.STATE_MAX = STATE_MAX
        self.pcome =pcome
        self.queuenum = len(pcome)
        self.queue = np.zeros(len(pcome),dtype=int)
        self.WI1 = WI1      #平常
        self.WI2 = WI2      #突发
        self.widthuseing = [[] for j in range(len(pcome))]
        self.drop = np.zeros(self.queuenum,dtype=int)
        self.time = 0
        self.eq = 0
        self.et = 0

    def inpacket(self):
        allpackets = []
        for q in range(self.queuenum):
            burst = np.random.rand()
            if q == 5 and 3000 < self.time < 3500:
                packets = self.random_packets(self.pcome[q]+0.45, q)
                # print(packets)
            else:
                packets = self.random_packets(self.pcome[q],q)
            allpackets.append(packets)
            self.queue[q] = self.queue[q] + packets
            if self.queue[q]>=self.STATE_MAX:
                self.drop[q] = self.drop[q]+self.queue[q]-self.STATE_MAX+1
                self.queue[q] = self.STATE_MAX -1
        # if self.time > 3000 and self.time < 3500:
        #     print( 't:', self.time, 'come:',allpackets)
        return allpackets

    '返回选择的一个发包队列'
    def outpacket(self):
        wi = []
        if 3000 < self.time < 3500:
            for q in range(self.queuenum):
                wi.append(self.WI2[q][self.queue[q]])
        else:
            for q in range(self.queuenum):
                wi.append(self.WI1[q][self.queue[q]])
        que = wi.index(max(wi))
        if self.queue[que] > 0:
            self.queue[que] = self.queue[que] -1
        else:
            que = 8
        for q in range(self.queuenum):
            self.widthuseing[q].append(1 if q==que else 0)

        if que != 8:
            self.et = self.et + 1

        return que

    def run(self,times):
        avgrewards = []
        allpackets = np.zeros(self.queuenum,dtype=int)#统计来包率
        out5 = 0  #统计队列5的发包次数
        outt5 = []  #统计队列5每时刻的发包累计情况
        comee5 = []  #统计队列5每时刻的收包累计情况
        flag = 0  # 判断极端情况是否发生
        # flagt = []  # 判断极端情况发生时间
        for q in range(self.queuenum):
            avgrewards.append([])
            avgrewards[q].append(0)
        for t in range(times):
            action1 = self.outpacket()

            pp = self.inpacket()

            for q in range(self.queuenum):
                self.eq = self.eq + self.queue[q]

            if(3000 < self.time < 3500):
                # print('s:',self.queue,'drop:',self.drop,'time:',self.time)
                if action1 == 5:
                    out5 = out5 + 1
                    outt5.append(out5)
                else:
                    outt5.append(out5)
                allpackets = allpackets + pp
                comee5.append(allpackets[5])

                # diff = allpackets[5] - out5
                # if(diff > 20):
                #     flag = 1
                #     flagt.append(self.time)

            for q in range(self.queuenum):
                avgrewards[q].append((avgrewards[q][t]*t+self.GetReward(q,action1))/(t+1))

            self.time = self.time + 1
        print("drop_num:{}".format(self.drop))
        # print('come:', allpackets, sum(allpackets))
        # print('out5:',out5)
        # print(comee5)
        # print(outt5)
        # for i in range(499):
        #     for j in range(499):
        #         if j > i:
        #             diff = comee5[j] - comee5[i]
        #             if(diff > 20 + j -i):
        #                 flag = 1
        #                 print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                        # print(comee5[j],comee5[i],j,i)
        # print('极端发生：',flag)
        return avgrewards

    def GetReward(self,queuen,action):
        ###set reward is -s
        return -self.queue[queuen]

    def random_packets(self,rate,queue):
        rad = np.random.rand()
        num = 0
        while rad>self.poission(num,expect=rate):
            rad = rad-self.poission(num,expect=rate)
            num = num +1
        return num

    def poission(self,k, expect=0.3):
        return expect ** k / math.factorial(k) * math.e ** (-expect)

    def show_width(self,step=-1):
        max_step = len(self.widthuseing[0])
        if step<0 or step>max_step:
            step = max_step
        timp = int(max_step / step)
        wid = np.zeros((self.queuenum,timp))
        for tmp in range(timp):
            for q in range(self.queuenum):
                wid[q][tmp] = sum(self.widthuseing[q][tmp*step:(tmp+1)*step])/step

'获取符号sym在字符串str中的索引'
def getindex(str,sym):
    index = []
    for i in range(len(str)):
        if str[i]==sym:
            index.append(i)
    return index

'将txt中的whittle index转化为列表类型，返回直接使用的wt'
def getwhittle(file_path,ee):
    wt = []
    with open(file_path, 'r') as file:
        wt2 = file.read()
    a = getindex(wt2, ',')
    b = getindex(wt2, '[')
    c = getindex(wt2, ']')
    b = b[1:]  #去掉第一个[
    c = c[0:-1]  #去掉最后一个]
    for k in range(queuenum):
        wtt = []
        leftb = b[k] + 1  # 第一个开头
        rightb = a[25 * k]  # 第一个结尾
        numstr = wt2[leftb:rightb]
        num = float(numstr)
        wtt.append(num)
        for j in range(23):
            left = a[j + 25 * k] + 2
            right = a[j + 1 + 25 * k]
            numstr = wt2[left:right]
            num = float(numstr)
            wtt.append(num)
        leftl = a[25 * k + 23] + 2  # 最后一个开头
        rightl = c[k]  # 最后一个结尾
        numstr = wt2[leftl:rightl]
        num = float(numstr)
        wtt.append(num)
        wt.append(wtt)
    return wt

exp_times = 1
enum = 3
ebegin = 0.04
drop_ave = []
drop_rate = []
eee = []

for k in range(enum):
    drop_times = 0
    drop_sums = 0
    ee = ebegin + 0.01*k+0.08
    eee.append(ee)
    if ee!= 0.1:
        file_path = 'C:/Users/48935/Desktop/test/w=500/'+'s='+str(STATE_MAX)+'  e='+str(ee)+'.txt'
    else:
        file_path = 'C:/Users/48935/Desktop/test/w=500/' + 's=' + str(STATE_MAX) + '  e=0.1'+ '.txt'
    wt2 = getwhittle(file_path,ee)
    for i in range(exp_times):
        qu = queue_simulation(pcome=[0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ], \
                STATE_MAX=25,\
                WI1=[[-6.938893903907228e-18, 0.14999999999999997, 0.15000000000000002, 0.15000000000000002, 0.15000000000000008, 0.15000000000000013, 0.15000000000000002, 0.15000000000000013, 0.1499999999999997, 0.15000000000000036, 0.1499999999999999, 0.1499999999999997, 0.15000000000000036, 0.15000000000000124, 0.15000000000004188, 0.15000000000156, 0.15000000005792824, 0.15000000215232756, 0.15000007996471565, 0.15000297034185017, 0.1501102652916022, 0.15413255784190172, 0.3238946762104056, 13.439105251011704, 503.09087876843], [2.7755575615628914e-17, 0.14999999999999994, 0.15, 0.15000000000000008, 0.15000000000000013, 0.15000000000000163, 0.15000000000001446, 0.15000000000011093, 0.15000000000087255, 0.15000000000685287, 0.15000000005382397, 0.15000000042271777, 0.1500000033199198, 0.1500000260737977, 0.1500002047770661, 0.15000160828794096, 0.15001263233925188, 0.15009923153032823, 0.15077969202476416, 0.15627183929507416, 0.21676941923776116, 1.4073087205085266, 25.990247604952877, 366.37530591362304, 2246.4625101292904], [0.0, 0.14999999999999997, 0.15000000000000002, 0.15000000000000008, 0.14999999999999997, 0.1499999999999998, 0.15000000000000058, 0.15000000000000058, 0.15000000000000735, 0.15000000000008207, 0.1500000000008861, 0.15000000000952962, 0.1500000001025683, 0.1500000011038598, 0.15000001188002732, 0.15000012785644223, 0.1500013760569061, 0.1500148115781652, 0.15015951580553066, 0.15173430299704105, 0.1710967453661154, 0.45637024982208985, 9.024180403295972, 181.99900846645838, 1677.0739558751786], [0.0, 0.14999999999999997, 0.15000000000000002, 0.15000000000000013, 0.14999999999999958, 0.15000000000000024, 0.15000000000000002, 0.1499999999999998, 0.15000000000000036, 0.1499999999999997, 0.1499999999999999, 0.14999999999999947, 0.15000000000000058, 0.1499999999999999, 0.1499999999999999, 0.15000000000004343, 0.15000000000229718, 0.15000000012222525, 0.15000000650923262, 0.15000034648660732, 0.15001843210899812, 0.15098888621338036, 0.2086807029694251, 6.497906934807917, 351.6307394475125], [0.0, 0.15000000000000008, 0.15000000000000038, 0.15000000000000246, 0.1500000000000158, 0.1500000000001006, 0.15000000000064406, 0.15000000000411318, 0.15000000002627778, 0.1500000001678783, 0.1500000010725142, 0.15000000685188808, 0.1500000437741329, 0.15000027965649299, 0.15000178662162011, 0.15001141443203458, 0.15007293750251982, 0.15046618976646675, 0.15298248635006306, 0.16977835547718945, 0.3379520149326489, 3.4844700007151705, 53.555318932571176, 587.0094498449789, 2704.0300483929495], [0.0, 0.15000000000005012, 0.1500000000002365, 0.1500000000011179, 0.15000000000528324, 0.15000000002497033, 0.1500000001180153, 0.15000000055776785, 0.150000002636147, 0.1500000124590679, 0.15000005888458734, 0.15000027830310647, 0.15000131533342453, 0.1500062167174725, 0.15002938521232956, 0.15013896315258002, 0.15065824450680365, 0.1531383057775999, 0.1656904699747166, 0.26031191342538484, 1.2990869698091285, 15.14776044507688, 161.78131769381292, 1193.7471661576242, 3495.723405333239], [6.938893903907228e-18, 0.15000000000000002, 0.15000000000000002, 0.1499999999999998, 0.15000000000000024, 0.1499999999999998, 0.15000000000000036, 0.1499999999999998, 0.15000000000000013, 0.1499999999999997, 0.15000000000000058, 0.14999999999999947, 0.1499999999999997, 0.15000000000000813, 0.1500000000002304, 0.15000000000725722, 0.15000000022798954, 0.15000000716333695, 0.15000022505556654, 0.15000706866862856, 0.15022235153910346, 0.15746963823587556, 0.4408825831319172, 18.937713639326752, 593.900617865489], [1.3877787807814457e-17, 0.14999999999999997, 0.15, 0.1500000000000001, 0.14999999999999963, 0.1499999999999999, 0.1500000000000007, 0.14999999999999947, 0.15000000000000047, 0.1499999999999999, 0.1499999999999997, 0.15000000000000058, 0.150000000000021, 0.150000000000438, 0.150000000009332, 0.15000000019863036, 0.15000000422846194, 0.15000009001491144, 0.1500019159662509, 0.15004073587043232, 0.1508727086243904, 0.17184731112983664, 1.128711852313141, 42.42237359084396, 870.5365738365501]],\
                WI2=wt2
                              )
        print(ee   ,'第',i+1,'次：')
        r = qu.run(5000)
        newd = sum(qu.drop)
        if newd!=0:
            drop_times = drop_times + 1
            drop_sums = drop_sums + newd
    print('e=',ee,'时丢包次数为：', drop_times, '平均丢包数为：', drop_sums / exp_times)
    drop_ave.append(drop_sums / exp_times)
    drop_rate.append(drop_times/exp_times)

print(eee)
print(drop_ave)
print(drop_rate)