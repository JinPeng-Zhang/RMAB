'''
more调度模拟
'''

import numpy as np
import math

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]

class queue_simulation():
    def __init__(self,pcome,STATE_MAX):
        self.STATE_MAX = STATE_MAX
        self.pcome =pcome
        self.queuenum = len(pcome)
        self.queue = np.zeros(len(pcome),dtype=int)
        self.drop = np.zeros(self.queuenum,dtype=int)
        self.time = 0
        # self.out = np.zeros(8,dtype=int)

    def inpacket(self):
        allpackets = []
        for q in range(self.queuenum):
            if q == 5 and self.time > 3000 and self.time < 3500:
                packets = self.random_packets(self.pcome[q]+0.45, q)
            else:
                packets = self.random_packets(self.pcome[q],q)
            allpackets.append(packets)
            self.queue[q] = self.queue[q] + packets
            if self.queue[q]>=self.STATE_MAX:
                self.drop[q] = self.drop[q]+self.queue[q]-self.STATE_MAX+1
                self.queue[q] = self.STATE_MAX -1
        return allpackets


    '返回选择的一个发包队列'
    def outpacket(self):
        ascend_index = np.argsort(self.queue)
        descend_index = ascend_index[::-1] ##descend_index[0]就是最大队列的序号
        que = descend_index[0]
        if self.queue[que] > 0:
            self.queue[que] = self.queue[que] -1
            # if (3000 < self.time < 3500):
            #     self.out[que] = self.out[que] + 1
        else:
            que = 8
        return que

    def run(self,times):
        avgrewards = []
        allpackets = np.zeros(self.queuenum, dtype=int)  # 统计来包率
        for q in range(self.queuenum):
            avgrewards.append([])
            avgrewards[q].append(0)
        for t in range(times):
            action1 = self.outpacket()
            pp = self.inpacket()
            if (3000 < self.time < 3500):
                # print('s:',self.queue,'drop:',self.drop,'time:',self.time)
                allpackets = allpackets + pp
            for q in range(self.queuenum):
                avgrewards[q].append((avgrewards[q][t]*t+self.GetReward(q,action1))/(t+1))
            self.time = self.time + 1
        print("drop_num:{}".format(self.drop))
        # print('come:', allpackets, sum(allpackets))
        return avgrewards

    def GetReward(self,queuen,action):
        return -self.queue[queuen]

    def random_packets(self,rate,queue):
        rad = np.random.rand()
        num = 0
        while rad > self.poission(num, expect=rate):
            rad = rad-self.poission(num, expect=rate)
            num = num + 1
        return num

    def poission(self,k, expect=0.3):
        return expect ** k / math.factorial(k) * math.e ** (-expect)

drop_times = 0
drop_sums = 0
exp_times = 1000

for i in range(exp_times):
    qu = queue_simulation(pcome=[0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ], \
            STATE_MAX = 25)
    print('第',i+1,'次：')
    r = qu.run(5000)
    newd = sum(qu.drop)
    if newd != 0:
        drop_times = drop_times + 1
        drop_sums = drop_sums + newd

print('丢包次数为：', drop_times, '平均丢包数为：', drop_sums/exp_times)
# print(qu.out,sum(qu.out))