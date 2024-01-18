'''
门限+wt调度，只对3个队列设置门限0.8*smax,另加了最后一个队列的门限0.6*smax
'''

import numpy as np
import math
import  matplotlib.pyplot as plt
pcome = ...

class queue_simulation():
    def __init__(self,pcome,STATE_MAX,WI):
        self.STATE_MAX = STATE_MAX
        self.pcome =pcome
        self.queuenum = len(pcome)
        self.queue = np.zeros(len(pcome),dtype=int)
        self.WI = WI
        self.drop = np.zeros(self.queuenum,dtype=int)
        self.time = 0
        self.smax = 20
        self.thres = [0.8*self.smax, 0, 0, 0.8*self.smax, 0, 0, 0.8*self.smax, 0.6*self.smax]

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
        for q in range(self.queuenum):
            wi.append(self.WI[q][self.queue[q]])

        for q in range(self.queuenum):
            if self.queue[q] < self.thres[q] and 3000 < self.time < 3500:
                wi[q] = wi[q]/10000

        que = wi.index(max(wi))
        if self.queue[que] > 0:
            self.queue[que] = self.queue[que] -1
        else:
            que = 8
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

            # if (2800 < self.time < 3001):
            #     print('s:', self.queue, 'drop:', self.drop, 'time:', self.time)
            if(3000 < self.time < 3500):
                # -print('s:',self.queue,'drop:',self.drop,'time:',self.time)
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
        # print('come:',allpackets,sum(allpackets))
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


drop_times = 0
drop_sums = 0
exp_times = 10000

for i in range(exp_times):
    qu = queue_simulation(pcome=[0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ], \
            STATE_MAX=20,\
            WI=[[0.0, 2.6666675296759306, 2.666698754936666, 2.6678557151257447, 2.7096530131721313, 5.3333333333340835, 5.3333333333612565, 5.333333334370778, 5.33333337187684, 5.3333347654830305, 5.333386582029714, 5.33530413799825, 5.401710697107482, 8.000000001814229, 8.000000067402212, 8.000002504469691, 8.000093126004828, 8.003449456983759, 8.123958976997208, 551.5272002085283], [0.0, 2.66710723205581, 2.670139899786135, 2.6944358849373486, 2.9093145207403266, 5.333333521824748, 5.333334813697377, 5.33334495967361, 5.333424642292947, 5.334050577932608, 5.338971935610623, 5.377394105450481, 5.654178900214596, 8.000017884732195, 8.000140465819328, 8.001103861915709, 8.008705313801975, 8.069362660985696, 8.581493516465443, 2846.430666148121], [0.0, 2.666790703866969, 2.668004305472646, 2.6811811665581233, 2.8330655647294885, 5.3333333484925305, 5.3333334964806856, 5.333335089161331, 5.333352229771762, 5.333536732247385, 5.335524337758574, 5.3568058808757115, 5.568169002971729, 8.000002833989193, 8.000030499962953, 8.00032834839682, 8.003541792886523, 8.038353926311622, 8.428174674160601, 2086.272236940212], [0.0, 2.666666871058596, 2.6666775565427234, 2.6672446229963676, 2.6962577883860606, 5.333333333333373, 5.333333333335586, 5.3333333334531545, 5.333333339712098, 5.333333672970948, 5.3333514289124615, 5.334293143492992, 5.381077970345409, 8.000000000211408, 8.000000011254933, 8.000000599271992, 8.000031930055606, 8.001694164268066, 8.086389476337075, 355.8409360677126], [0.0, 2.6676798597295877, 2.6731790643257045, 2.7094450178021727, 2.9814667929761196, 5.33333431654888, 5.333339614727002, 5.3333734625142775, 5.333589699303655, 5.3349714962242345, 5.343810060548968, 5.399896620822538, 5.726690625363155, 8.000059020109887, 8.000377094509055, 8.002411775977642, 8.015508433750483, 8.101356888295918, 8.704621154942558, 3468.398871209386], [0.0, 2.6701023826422086, 2.6831118154479077, 2.7483840753330044, 3.138530011032805, 5.333344292434209, 5.333385128692926, 5.333578128235835, 5.334490271228464, 5.3388028162565675, 5.359215249163, 5.454856969574031, 5.8620605991307215, 8.00032669689302, 8.001544770652394, 8.007321984150316, 8.035065880241959, 8.172571690368521, 8.905940969883048, 4579.511837452763], [0.0, 2.6666683556437243, 2.6667197738972175, 2.6683314972049317, 2.7179227782518973, 5.333333333336206, 5.333333333423624, 5.333333336170234, 5.333333422461717, 5.3333361338712635, 5.333421388143719, 5.336089165203134, 5.414162720742546, 8.000000004933803, 8.000000155008024, 8.000004870628864, 8.000153159602128, 8.004798993373619, 8.146685885470283, 669.0655225187357], [0.0, 2.6666747011706495, 2.66683786317349, 2.670309074516932, 2.7442926184238283, 5.333333333398032, 5.333333334710652, 5.333333362652947, 5.333333957467222, 5.33334662117074, 5.333616424603115, 5.339335436465877, 5.452493363159945, 8.000000050112781, 8.000001066762657, 8.00002271199704, 8.00048399024292, 8.01028946907725, 8.216823283721808, 1028.1872185005736]]
                          )
    print('第',i+1,'次：')
    r = qu.run(5000)
    newd = sum(qu.drop)
    if newd!=0:
        drop_times = drop_times + 1
        drop_sums = drop_sums + newd

print('丢包次数为：',drop_times,'平均丢包数为：',drop_sums/exp_times)