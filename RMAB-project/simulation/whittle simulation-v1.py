import numpy as np
import math
import  matplotlib.pyplot as plt
pcome = ...
# P0 = ...
# P1 = ...

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

    '每个队列进数据包，并统计丢包'
    def inpacket(self):
        for q in range(self.queuenum):
            packets = self.random_packets(self.pcome[q],q)
            self.queue[q] = self.queue[q] + packets
            if self.queue[q]>=self.STATE_MAX:
                self.drop[q] = self.drop[q]+self.queue[q]-self.STATE_MAX+1
                self.queue[q] = self.STATE_MAX -1

    '输出数据包，若wi最大的队列无包则不输出，最后返回输出的队列编号（不输出则为8）'
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
        return que

    '模拟调度过程，打印队列和丢包数，返回平均奖励（时间平均）'
    def run(self,times):
        avgrewards = []
        finalreward = 0##记录最后时刻的队列平均奖励
        for q in range(self.queuenum):
            avgrewards.append([])
            avgrewards[q].append(0)
        # average reward = (old*time+new)/(time+1),time = time+1
        for t in range(times):
            action1 = self.outpacket()
            self.inpacket()

            # print(self.queue)

            for q in range(self.queuenum):
                avgrewards[q].append((avgrewards[q][t]*t+self.GetReward(q,action1))/(t+1))#时间平均

            self.time = self.time + 1
        # print("drop_num:{}".format(self.drop))
        # return avgrewards
            if(t == times-1):
                for q in range(self.queuenum):
                    finalreward = finalreward + avgrewards[q][t]
            finalreward = finalreward / self.queuenum
        return finalreward,self.drop

    '随机生成满足泊松分布分布个数num个数据包，queue为数据包加入的队列'
    def random_packets(self,rate,queue):
        rad = np.random.rand()
        num = 0
        while rad>self.poission(num,expect=rate):
            rad = rad-self.poission(num,expect=rate)
            num = num +1

        brust = np.random.rand()
        if brust <0.15 and queue==5 and self.time>3000 and self.time <3500:
            num = num+3

        return num

    def poission(self,k, expect=0.3):
        return expect ** k / math.factorial(k) * math.e ** (-expect)

    ''
    def show_width(self,step=-1):##step为输出时间步长，step=-1表示输出全部时间节点
        max_step = len(self.widthuseing[0])

        # print('widthuseing[0]:',self.widthuseing[0])   =很多0,1的矩阵

        if step<0 or step>max_step:
            step = max_step
        timp = int(max_step / step)

        # print('timp:',timp)   =50

        wid = np.zeros((self.queuenum,timp))
        for tmp in range(timp):
            for q in range(self.queuenum):
                wid[q][tmp] = sum(self.widthuseing[q][tmp*step:(tmp+1)*step])/step
        # print('wid:',wid)
        # print('sum_wid:',np.sum(wid,axis=0))
        # print('sum_pcome',sum(self.pcome))  =0.76
    '返回奖励'
    def GetReward(self, queuen, action):
        ###set reward
        re = self.queue[queuen]
        re1 = re
        re2 = re**2/20
        re3 = re**3/400
        re4 = re ** 4 / 8000
        return -re1

total_drop = 0
total_reward = 0
zerodrop_times = 0
exp_times = 1000

'重复实验exp_times次'
for i in range(exp_times):
    '单次实验'
    qu = queue_simulation(
        pcome=[0.02534504, 0.13369194, 0.09386043, 0.01754024, 0.17004173, 0.2459021, 0.03012342, 0.0451653], \
        STATE_MAX=20, \
        WI=[[0.0, 1.666668098816357, 1.6667199153630694, 1.6686374713314471, 1.7350440304350636, 3.3333333333340835, 3.3333333333612565, 3.333333334370778, 3.3333333718768436, 3.3333347654834213, 3.3333865820446213, 3.3353041385509705, 3.401710717683855, 5.000000801404234, 5.000029769238857, 5.001105207424352, 5.0413920922334725, 6.726559371182432, 130.04980538170796, 4734.132915184735], [0.0, 1.6673839112266935, 1.6723052685698487, 1.7107274318052248, 1.987511950145108, 3.3333335220742857, 3.3333348156571745, 3.333344975065387, 3.333424763177131, 3.334051527393701, 3.338979396589693, 3.377452957621525, 3.654655554319426, 5.004305306813528, 5.033843901278139, 5.273314517434123, 7.871091859488871, 51.44775464188244, 654.7901490271788, 3986.3230075783454], [0.0, 1.6668700655716562, 1.6688576709928347, 1.6901392129583757, 1.9015023031308642, 3.333333348495767, 3.3333334965155625, 3.33333508953665, 3.333352233811084, 3.3335367757211323, 3.3355248058235034, 3.356810940041324, 3.568225771578696, 5.000781780875364, 5.008413703295673, 5.091914260908652, 6.213417006713968, 27.858698634469604, 464.83575007667866, 4241.083515391283], [0.0, 1.6666670063042688, 1.666684762245803, 1.6676264768263103, 1.7144113036782898, 3.333333333333373, 3.3333333333355863, 3.3333333334531545, 3.333333339712098, 3.333333672970955, 3.3333514289130513, 3.334293143524434, 3.3810779720218136, 5.000000095470639, 5.000005082005352, 5.000270378147846, 5.014494684986822, 5.851769540147956, 91.56670409177171, 4795.247051838236], [0.0, 1.6683048304837143, 1.6771433990579583, 1.7332299571780734, 2.0600228545674817, 3.333334320653984, 3.333339640952998, 3.3333736300653065, 3.333590769845898, 3.3349783404865185, 3.3438539893361394, 3.4001855162425727, 3.728720132748407, 5.014175593625822, 5.090802037692654, 5.603981612430161, 10.472217341492325, 80.23493272852627, 823.4247381077136, 3771.546094494728], [0.0, 1.6721362202347838, 1.6925488919244103, 1.788191223752908, 2.19538715034807, 3.333344477498345, 3.333386003362163, 3.3335822623870612, 3.334509815868053, 3.3388953150359164, 3.359655249193178, 3.4569992155508587, 3.8734489394918583, 5.071147040331475, 5.355132895206268, 7.142618145609397, 20.64567303155964, 161.86820721347465, 1155.623415064906, 3370.6035165680514], [0.0, 1.6666694672045972, 1.6667547214770364, 1.669422498536008, 1.7474960540572209, 3.3333333333362063, 3.3333333334236244, 3.3333333361702415, 3.333333422461795, 3.3333361338733845, 3.3334213882108195, 3.33608916731162, 3.4141627871172275, 5.000002170108267, 5.0000681681547405, 5.002140141870008, 5.067826334406611, 7.414359922080649, 153.59196460954777, 4697.250021216081], [0.0, 1.6666799545040414, 1.666949757936044, 1.672668769790068, 1.7858266962072342, 3.3333333333980324, 3.3333333347106606, 3.333333362653132, 3.3333339574710763, 3.3333466212527902, 3.3336164263502397, 3.3393354737568295, 3.4524941987869155, 5.000022149223518, 5.00047141165971, 5.010028468736252, 5.215857071311994, 10.340444219622256, 227.57328403812198, 4583.714659175355]]
    )
    rew,drop = qu.run(5000)
    print('第',i+1,'次，drop_num:',drop)
    total_drop = total_drop + drop
    total_reward = total_reward + rew
    '获取0丢包次数'
    k = 0
    for q in range(qu.queuenum):
        if(qu.drop[q] == 0):
            k = k + 1
    if (k == 8):
        zerodrop_times = zerodrop_times + 1
    '重置'
    for q in range(qu.queuenum):
        qu.drop[q] = 0

print(exp_times,'次实验总丢包为：',total_drop)
print(exp_times,'次实验的平均奖励为：',total_reward/exp_times)
print('平均每次丢包为：',total_drop/exp_times)
print('其中零丢包次数为：',zerodrop_times)