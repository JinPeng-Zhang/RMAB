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
        self.eq = 0
        self.et = 0

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
        wi = []
        for q in range(self.queuenum):
            wi.append(self.WI[q][self.queue[q]])
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

drop_times = 0
drop_sums = 0
exp_times = 10000

# etime = np.zeros(50) #统计e的取值分别落在0-0.01 0.01-0.02...0.19-0.2区间的次数

for i in range(exp_times):
    qu = queue_simulation(pcome=[0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ], \
            STATE_MAX=25,\
            WI=[[0.0, 0.23333333333333342, 0.23333333333333323, 0.23333333333333345, 0.2333333333333334, 0.23333333333333295, 0.2333333333333334, 0.23333333333333317, 0.23333333333333384, 0.23333333333333295, 0.2333333333333334, 0.23333333333333384, 0.23333333333333295, 0.2333333333333374, 0.23333333333347106, 0.2333333333384826, 0.233333333524663, 0.23333334044239074, 0.23333359742776816, 0.23334313497904446, 0.23369859228195544, 0.24852884715474577, 1.318422092188734, 84.53621447493954, 3191.472622947561], [-2.7755575615628914e-17, 0.23333333333333345, 0.23333333333333334, 0.23333333333333323, 0.2333333333333334, 0.23333333333333595, 0.2333333333333527, 0.23333333333348083, 0.23333333333449557, 0.23333333334245987, 0.23333333340500673, 0.23333333389624, 0.23333333775425746, 0.23333336805414806, 0.23333360602190734, 0.2333354749850871, 0.23335015487450006, 0.2334654772737994, 0.23437199407979348, 0.24168238329436242, 0.3205207581877687, 1.744762817428489, 31.15331917213212, 438.3553544231973, 2687.489194574152], [0.0, 0.23333333333333336, 0.2333333333333334, 0.23333333333333317, 0.2333333333333334, 0.23333333333333361, 0.23333333333333295, 0.23333333333333517, 0.2333333333333456, 0.23333333333346484, 0.23333333333474604, 0.23333333334855277, 0.23333333349711705, 0.23333333509602516, 0.23333335230388474, 0.23333353750020303, 0.23333553068639334, 0.23335698496204893, 0.23358802898751962, 0.2361029370610277, 0.2682402403580788, 0.7535273323802398, 15.360597696427007, 310.26164923659866, 2859.185959414391], [0.0, 0.2333333333333334, 0.2333333333333334, 0.23333333333333328, 0.23333333333333328, 0.23333333333333373, 0.23333333333333295, 0.23333333333333273, 0.2333333333333345, 0.23333333333333361, 0.23333333333333295, 0.23333333333333428, 0.2333333333333325, 0.23333333333333428, 0.23333333333333872, 0.23333333333362782, 0.2333333333491301, 0.23333333417419455, 0.2333333781169311, 0.23333571652654328, 0.23346027906659472, 0.24048441622722816, 0.7528220553662353, 58.59206989773262, 3232.6595266555373], [0.0, 0.2333333333333335, 0.23333333333333373, 0.2333333333333359, 0.23333333333334993, 0.23333333333343953, 0.23333333333401052, 0.23333333333766015, 0.23333333336097462, 0.23333333350992458, 0.2333333344615025, 0.23333334054079202, 0.23333337937906817, 0.2333336275022444, 0.23333521266983004, 0.23334534007800034, 0.23341005486697286, 0.23382373804098222, 0.23647235463292393, 0.25412599076086684, 0.4259838824619191, 3.384726770234444, 50.467452876745966, 552.084985797839, 2542.73772140036], [-5.551115123125783e-17, 0.23333333333338502, 0.2333333333335772, 0.23333333333448542, 0.23333333333877937, 0.2333333333590708, 0.23333333345497487, 0.23333333390824063, 0.23333333605048545, 0.23333334617524937, 0.23333339402734943, 0.23333362018825188, 0.2333346890853445, 0.23333974108602584, 0.23336362127493748, 0.23347656042472265, 0.23401190423109908, 0.23657360124471793, 0.24948382629323618, 0.3353928517307616, 1.0138900436775309, 10.01627280757399, 105.3358020099304, 776.1642943969026, 2272.512669917537], [6.938893903907228e-18, 0.23333333333333334, 0.2333333333333334, 0.2333333333333334, 0.2333333333333335, 0.23333333333333284, 0.23333333333333361, 0.23333333333333428, 0.23333333333333273, 0.23333333333333317, 0.2333333333333334, 0.2333333333333334, 0.23333333333333384, 0.23333333333335515, 0.23333333333398176, 0.23333333335376016, 0.233333333974985, 0.23333335349482853, 0.23333396669236173, 0.23335320606003496, 0.23396044929267124, 0.2560065657737578, 1.767396791387175, 100.40788837087703, 3166.61593335553], [1.3877787807814457e-17, 0.23333333333333334, 0.23333333333333336, 0.233333333333333, 0.23333333333333373, 0.23333333333333295, 0.23333333333333317, 0.23333333333333428, 0.23333333333333317, 0.23333333333333406, 0.23333333333333384, 0.23333333333333606, 0.23333333333339068, 0.2333333333345653, 0.23333333335957107, 0.23333333389186395, 0.23333334522327442, 0.2333335864466659, 0.23333872049546844, 0.23344780457583436, 0.23579031524138117, 0.2972739776775706, 3.6941221806925446, 150.28598186372452, 3090.1001964874617]]
                          )
    print('第',i+1,'次：')
    r = qu.run(5000)
    newd = sum(qu.drop)
    if newd!=0:
        drop_times = drop_times + 1
        drop_sums = drop_sums + newd
    # print(qu.eq, qu.et,qu.et/qu.eq)
    # e = qu.et/qu.eq
    # etime[int(e/0.01)] = etime[int(e/0.01)] + 1

# print(etime)
print('丢包次数为：',drop_times,'平均丢包数为：',drop_sums/exp_times)
