import numpy as np
from WITTLE_INDEX_CLASS import MDP
class queue_simulation():
    def __init__(self,algorithm,handling,pcome,bstart_tim):
        self.priority = 8
        self.queue = np.zeros(8)
        self.queue_size = 20
        self.Scheduling_algorithm = algorithm###优先级，WITTLE,MAX_QUEUE
        self.Congestion_handling = handling##ECN标记，AQM,drop
        self.pcome = pcome
        self.btim = list(bstart_tim)####多次突发的起始时间list类型，每个值之间差距100ms以上
        self.burst = True
        self.print_log = True
        self.handling = np.zeros(8)
        #=======================ECN AQM===============================#
        self.ECN_KMIN = 0.2*self.queue_size
        self.ECN_KMAX = 0.6*self.queue_size
        self.ECN_PMAX = 0.8
        self.AQM_MIN_THRESH = 0.4*self.queue_size
        self.AQM_MAX_THRESH = 0.8*self.queue_size
        self.AQM_PMAX = 0.2
        #========================WITTLE INDEX=========================#
        self.vs = int((self.queue_size+1)/0.05)
        self.WITTLE = np.zeros((self.priority,self.vs))  ####8*21
        #=====================throughput\capacity\unit================#
        # simulation时间单位为ms,
        # 队列容量为10MB（参照华为虚拟队列大小），最大容量（状态）单位20，因此一个状态对应500KB
        #端口处理速度为每ms一个容量单位，即500KB/MS，4Gbps
        #8个队列单位时间来包速率(无突发)小于4Gbps
        #突发时，设置突发场景为来报速率为10Gbps，持续100ms
    def inpacket(self,times):
        #服从正态（高斯）分布，均值为到达率,方差为500Mbps,即0.125个单位
        for q in range(self.priority):
            come = np.random.normal(loc=self.pcome[q], scale=self.pcome[q]/4, size=None)
            while come<=0:
                come = np.random.normal(loc=self.pcome[q], scale=self.pcome[q]/4, size=None)
            if len(self.btim) !=0:
                if times >= self.btim[0] and times <= self.btim[0]+100:###持续时间100
                    bcome = self.burst_in()
                    come = come + bcome
                    if self.print_log:
                        self.log("rate burst at {} ms,more {}  in queue{}".format(times,bcome,q))
                elif  times > self.btim[0] + 100:
                    self.btim.pop(0)
            if self.Congestion_handling == "ECN":
                self.ECN_handle(q,come)
            elif self.Congestion_handling == "AQM":
                self.AQM_handle(q,come)
            elif self.Congestion_handling == "FULL_DROP":
                self.DROP_handle(q,come)
            if self.print_log:
                self.log("time{}ms queue {} come {}".format(times,q,come))

    '返回选择的一个发包队列'
    def outpacket(self,times):
        num = -1
        q = -1
        if self.Scheduling_algorithm == "SP":
            q,num = self.Strict_priority_algorithm()
        elif self.Scheduling_algorithm == "WITTLE":
            q,num = self.WITTLE_algorithm()
        elif self.Scheduling_algorithm == "MAX_QUEUE_LEN":
            q,num = self.MAX_QUEUE_LEN_algorithm()
        if num>0:
            self.queue[q] = self.queue[q]-num
        if self.print_log:
            if num >0:
                self.log("time:{} send queue{} {} packets".format(times,q,num))
            elif num == 0:
                self.log("time:{} queues if empty".format(times))
            else:
                self.log("Scheduling_algorithm name {} is error".format(self.Scheduling_algorithm))
    def log(self,str):
        print(str+"\n")
    def burst_in(self):
        bcome = 1.5*np.random.normal(loc=1, scale=0.2, size=None)/8
        return bcome
    def ECN_handle(self,q,come):
        if self.queue[q]+come>self.queue_size:
            drop = self.queue[q]+come-self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q,drop))
        self.queue[q] = self.queue[q]+come
        for qlen in range(int(self.queue[q])):
            ECN_MARK = self.ECN_MARK_probability(qlen)
            if ECN_MARK == True and self.print_log:
                self.log("queue{} {}th packet is ecn marked".format(q,qlen))
    def ECN_MARK_probability(self,qlen):
        if qlen<=self.ECN_KMIN:
            return False
        elif qlen>=self.ECN_KMAX:
            return  True
        else:
            p = self.ECN_PMAX*(qlen-self.ECN_KMIN)/(self.ECN_KMAX-self.ECN_KMIN)
            RAND = np.random.random()
            if RAND>=p:
                return False
            else:
                return True
    def AQM_handle(self,q,come):
        if self.queue[q] + come > self.queue_size:
            drop = self.queue[q] + come - self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q, drop))
        self.queue[q] = (self.queue[q] + come)
        DROP = 0
        for qlen in range(int(self.queue[q])):
            AQM_DROP = self.AQM_DROP_probability(qlen)
            if AQM_DROP == True and self.print_log:
                DROP = DROP + 1
                self.log("queue{} {}th packet is AQM droped".format(q, qlen))
        self.queue[q] = self.queue[q] - DROP
    def AQM_DROP_probability(self,qlen):
        if qlen <= self.AQM_MIN_THRESH:
            return False
        elif qlen >= self.AQM_MAX_THRESH:
            return True
        else:
            p = self.AQM_PMAX * (qlen - self.AQM_MIN_THRESH) / (self.AQM_MAX_THRESH - self.AQM_MIN_THRESH)
            RAND = np.random.random()
            if RAND >= p:
                return False
            else:
                return True
    def DROP_handle(self,q,come):
        if self.queue[q] + come > self.queue_size:
            drop = self.queue[q] + come - self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q, drop))
        self.queue[q] = self.queue[q] + come
    def Strict_priority_algorithm(self):
        q = 0
        for _q in range(self.priority):
            if self.queue[_q]>1:
                return _q,1
        return q,self.queue[q]
    def WITTLE_algorithm(self):
        WI = self.WITTLE[0][self.queue[0]]
        q = 0
        for _q in range(self.priority-1):
            if self.WITTLE[_q+1][self.queue[_q+1]]>WI:
                WI = self.WITTLE[_q+1][self.queue[_q+1]]
                q = _q+1
        if self.queue[q]>1:
            return q,1
        return q,self.queue[q]
    def MAX_QUEUE_LEN_algorithm(self):
        QLEN = self.queue[0]
        q = 0
        for _q in range(self.priority-1):
            if self.queue[_q+1]>QLEN:
                QLEN = self.queue[_q+1]
                q = _q+1
        if self.queue[q]>1:
            return q,1
        return q,self.queue[q]
    def WITTLE_INSERT(self,WITTLE):
        for q in range(self.priority):
            for s in range(self.vs):
                self.WITTLE[q][s] = WITTLE[q][s]
    def run(self,times):
        self.inpacket(times)
        if self.print_log:
            self.log("queuelen:{}".format(self.queue))
        self.outpacket(times)
    def exp_store(self,exp,exp_pool:MDP):
        exp_pool.add_exp(exp)



