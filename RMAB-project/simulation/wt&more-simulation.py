'''
根据计算好的whittle进行仿真
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
        self.widthuseing = [[] for j in range(len(pcome))]
        self.drop = np.zeros(self.queuenum,dtype=int)
        self.time = 0

    def inpacket(self):
        allpackets = []
        for q in range(self.queuenum):
            burst = np.random.rand()
            if q == 5 and self.time > 3000 and self.time < 3500:
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
        flag = 0
        thres = 19
        for q in range(self.queuenum):
            if self.queue[q] > thres:
                flag = 1
        if flag == 0:
            wi = []
            for q in range(self.queuenum):
                wi.append(self.WI[q][self.queue[q]])
            que = wi.index(max(wi))
            if self.queue[que] > 0:
                self.queue[que] = self.queue[que] -1
            else:
                que = 8
        else:
            ascend_index = np.argsort(self.queue)
            descend_index = ascend_index[::-1]  ##descend_index[0]就是最大队列的序号
            que = descend_index[0]
            if self.queue[que] > 0:
                self.queue[que] = self.queue[que] - 1

        for q in range(self.queuenum):
            self.widthuseing[q].append(1 if q==que else 0)
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

            if(3000 < self.time < 3500):
                print('s:',self.queue,'drop:',self.drop,'time:',self.time)
                allpackets = allpackets + pp
                # if action1 == 5:
                #     out5 = out5 + 1
                #     outt5.append(out5)
                # else:
                #     outt5.append(out5)



                # comee5.append(allpackets[5])

                # diff = allpackets[5] - out5
                # if(diff > 20):
                #     flag = 1
                #     flagt.append(self.time)

            for q in range(self.queuenum):
                avgrewards[q].append((avgrewards[q][t]*t+self.GetReward(q,action1))/(t+1))

            self.time = self.time + 1
        print("drop_num:{}".format(self.drop))
        # print('out5:',out5)
        print('come:',allpackets,sum(allpackets))
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

drop_times = 0
drop_sums = 0
exp_times = 1

for i in range(exp_times):
    qu = queue_simulation(pcome=[0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ], \
            STATE_MAX=20,\
            WI=[[0.0, 2.6666675296759306, 2.666698754936666, 2.6678557151257447, 2.7096530131721313, 5.333333333334091, 5.333333333361416, 5.333333334376501, 5.333333372089768, 5.333334773393958, 5.333386876016299, 5.335315129434303, 5.402196192808937, 8.070038970611925, 10.737038577877634, 13.403734687975643, 16.070430143364106, 18.741199727412237, 21.663890605325875, 7657.1585756412605], [0.0, 2.66710723205581, 2.6701398997861348, 2.6944358849373504, 2.9093145207403257, 5.333333527334382, 5.333334856968779, 5.333345299525291, 5.333427311944405, 5.334071578518554, 5.339138992077938, 5.378836663862895, 5.672970498991695, 8.365215636682507, 11.035154152582791, 13.703715951078863, 16.37217439222671, 19.112387587451437, 22.883982710574486, 6913.135686473121], [0.0, 2.6667907038669685, 2.668004305472645, 2.681181166558124, 2.8330655647294876, 5.333333348802759, 5.333333499819572, 5.33333512509542, 5.333352616520692, 5.333540896579553, 5.335569401915084, 5.357319117796713, 5.576687121715224, 8.25728122423098, 10.926217246486608, 13.593800061605108, 16.261331074205017, 18.97042155738299, 22.475132464428256, 7166.606049918337], [0.0, 2.666666871058596, 2.6666775565427234, 2.6672446229963676, 2.6962577883860606, 5.333333333333373, 5.3333333333355935, 5.333333333453613, 5.333333339736498, 5.333333674269756, 5.333351498070616, 5.334296838284953, 5.381300932526052, 8.048541205767748, 10.71537892761797, 13.382055865812632, 16.04873264063039, 18.717431299962698, 21.56370527023222, 7717.963221393411], [0.0, 2.6676798597295877, 2.673179064325705, 2.7094450178021745, 2.9814667929761365, 5.333334353248992, 5.333339849193235, 5.333374960557158, 5.333599274855384, 5.335032880711225, 5.34421088402603, 5.402810979101311, 5.7588183694590995, 8.461181830724001, 11.133874640701578, 13.80326104541691, 16.47256842794613, 19.242571140307774, 23.212323079846826, 6699.4464350020135], [0.0, 2.670102382642217, 2.683111815447949, 2.748384075333207, 3.1385300110344376, 5.333344891548954, 5.333387960519168, 5.333591518042052, 5.334553686424993, 5.339105479458077, 5.36071209415357, 5.463426250190057, 5.934465723752325, 8.65677132905514, 11.338046384465649, 14.007213396618639, 16.677124372966446, 19.505173624596907, 23.749175919688128, 6300.53428876639], [0.0, 2.6666683556437243, 2.6667197738972175, 2.6683314972049317, 2.7179227782518973, 5.333333333336228, 5.333333333424214, 5.333333336188854, 5.333333423046838, 5.333336152254439, 5.3334219659059094, 5.3361074711090986, 5.414865050198024, 8.083175011827606, 10.750291905031993, 13.417006462307228, 16.083719780065287, 18.75606552371812, 21.724495694587432, 7620.462462026939], [0.0, 2.6666747011706495, 2.66683786317349, 2.670309074516932, 2.7442926184238283, 5.33333333339867, 5.333333334724205, 5.333333362941438, 5.333333963608567, 5.333346751907701, 5.333619210103372, 5.3393957452968195, 5.454181248203874, 8.124419614331146, 10.791965080764612, 13.458777527998109, 16.125584697725543, 18.8042344935933, 21.91152875659145, 7507.502059618424]]
                          )
    print('第',i+1,'次：')
    r = qu.run(5000)
    newd = sum(qu.drop)
    if newd!=0:
        drop_times = drop_times + 1
        drop_sums = drop_sums + newd

print('丢包次数为：',drop_times,'平均丢包数为：',drop_sums/exp_times)