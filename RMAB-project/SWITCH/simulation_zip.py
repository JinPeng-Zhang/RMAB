import numpy as np
class queue_simulation():
    def __init__(self,queue_size,u_unit,algorithm,handling,pcome,burst,burst_version='v1'):
        self.port_index = 1
        self.priority = 8
        self.queue = np.zeros(8)
        self.queue_size = queue_size
        self.Scheduling_algorithm = algorithm###优先级，WITTLE,MAX_QUEUE
        self.Congestion_handling = handling##ECN标记，AQM,drop
        self.pcome = pcome
        #====================burst===============================
        self.burst_version = burst_version
        self.burst = []
        if burst_version=='v1':
            self.burst = list(burst)
        else:
            self.burst = dict(burst)
        '''
        突发设计，实际情况会有一些出入
        [start_time,end_time)
        v1:busrt = [time1,time2,...,timen]固定模式
        v2:busrt = {'len':n,'b':[[start_time,end_time,q1_index,q2_index,.....,qk_index],...,[]]}，自定义起始时间和队列，平均突发
        v3:busrt = {'len':n,'b':[{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate},...,{}]},自定义起始时间和队列，自定义队列突发速率
        v4:busrt = {'len':n,'b':[{'type':'v3','data':{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate}},{'type':'v2','data':[start_time,end_time,q1_index,q2_index,.....,qk_index]},{'type':'v1','data':200}]}v1,v2.v3混合模式
        '''
        #========================================================
        self.print_log = False
        self.handling = np.zeros(8)
        #=======================ECN AQM===============================#
        self.ECN_KMIN = 0.2*self.queue_size
        self.ECN_KMAX = 0.6*self.queue_size
        self.ECN_PMAX = 0.8
        self.AQM_MIN_THRESH = 0.4*self.queue_size
        self.AQM_MAX_THRESH = 0.8*self.queue_size
        self.AQM_PMAX = 0.2
        #========================WITTLE INDEX BDP=========================#
        self.u_unit = u_unit
        self.vs = int((self.queue_size+1)*(1+1/u_unit))
        self.WITTLE = np.zeros((self.priority,self.vs))  ####8*(21*21)
        '''
           经验数据使用字典类型：
           EXP = {"PORT":2,'LEN':1000,'q0':[[s a s']....[s,a',s']],....,'q7':[s a s']}
        '''
        self.EXP_POOL = {'PORT':self.port_index,'LEN':0,'q0':[],'q1':[],'q2':[],'q3':[],'q4':[],'q5':[],'q6':[],'q7':[]}
        self.EXP_cache = {'q0':[],'q1':[],'q2':[],'q3':[],'q4':[],'q5':[],'q6':[],'q7':[]}
        self.UP_LOAD = False
        #=====================throughput\capacity\unit================#
        # simulation时间单位为ms,
        # 队列容量为10MB（参照华为虚拟队列大小），最大容量（状态）单位20，因此一个状态对应500KB
        #端口处理速度为每ms一个容量单位，即500KB/MS，4Gbps
        #8个队列单位时间来包速率(无突发)小于4Gbps
        #突发时，设置突发场景为来报速率为10Gbps，持续100ms
        #====================performance============================#
        self.performance = {'q0':{'len':0,'drop':0,'ecn':0,'time':0},'q1':{'len':0,'drop':0,'ecn':0,'time':0},
                            'q2':{'len':0,'drop':0,'ecn':0,'time':0},'q3':{'len':0,'drop':0,'ecn':0,'time':0},
                            'q4':{'len':0,'drop':0,'ecn':0,'time':0},'q5':{'len':0,'drop':0,'ecn':0,'time':0},
                            'q6':{'len':0,'drop':0,'ecn':0,'time':0},'q7':{'len':0,'drop':0,'ecn':0,'time':0}}
        self.performance_update_flag = False
    def inpacket(self,times):
        #服从正态（高斯）分布，均值为到达率,方差为500Mbps,即0.125个单位
        for q in range(self.priority):
            come = np.random.normal(loc=self.pcome[q], scale=self.pcome[q]/4, size=None)
            while come<=0:
                come = np.random.normal(loc=self.pcome[q], scale=self.pcome[q]/4, size=None)
            '''
            if len(self.btim) !=0:
                if times >= self.btim[0] and times <= self.btim[0]+100:###持续时间100
                    bcome = self.burst_in()
                    come = come + bcome
                    if self.print_log:
                        self.log("rate burst at {} ms,more {}  in queue{}".format(times,bcome,q))
                elif  times > self.btim[0] + 100:
                    self.btim.pop(0)
            '''
            burst_come =self.burst_add_rate(times,q)
            come = come+burst_come
            drop = 0
            ecn = 0
            if self.Congestion_handling == "ECN":
                drop,ecn = self.ECN_handle(q,come)
            elif self.Congestion_handling == "AQM":
                drop,ecn =self.AQM_handle(q,come)
            elif self.Congestion_handling == "FULL_DROP":
                drop,ecn =self.DROP_handle(q,come)
            if self.print_log:
                self.log("time{}ms queue {} come {}".format(times,q,come))
            self.performance_update(drop=drop,ecn=ecn,q=q)
    def outpacket(self,times):
        '''
        返回选择的一个发包队列
        '''
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
            self.action_Collect(times,q)
        if self.print_log:
            if num >0:
                self.log("time:{} send queue{} {} packets".format(times,q,num))
            elif num == 0:
                self.log("time:{} queues if empty".format(times))
            else:
                self.log("Scheduling_algorithm name {} is error".format(self.Scheduling_algorithm))

    def log(self,str):
        print(str)

    def burst_add_rate(self,times,q):
        bcome = 0
        if self.burst_version == 'v1':
            if len(self.burst) != 0:
                if times >= self.burst[0] and times < self.burst[0] + 100:  ###持续时间100
                    bcome = 1.5*np.random.normal(loc=1, scale=0.2, size=None)/8
                elif times == self.burst[0] + 100:
                    self.burst.pop(0)
        elif self.burst_version == 'v2':
            '''
            busrt = {'len':n,'b':[[start_time,end_time,q1_index,q2_index,.....,qk_index],...,[]]}
            '''
            if self.burst['len'] == 0 or times<self.burst['b'][0][0]:
                return 0
            elif times==self.burst['b'][0][1]:
                self.burst['b'].pop(0)
                self.burst['len'] = self.burst['len'] - 1
                return 0
            elif q in self.burst['b'][0][2:]:
                bcome = 1.5*np.random.normal(loc=1, scale=0.2, size=None)/len(self.burst['b'][0][2:])
        elif self.burst_version == 'v3':
            '''
            {'len':n,'b':[{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate},...,{}]}
            '''
            if self.burst['len'] == 0 or times<self.burst['b'][0]['start_time']:
                return 0
            elif times == self.burst['b'][0]['end_time']:
                self.burst['b'].pop(0)
                self.burst['len'] = self.burst['len'] - 1
                return 0
            else:
                bcome = self.burst['b'][0]['q{}'.format(q)]*np.random.normal(loc=1, scale=0.2, size=None)
        elif self.burst_version == 'v4':
            '''
            busrt ={'len':n,'b':[{'type':'v3','data':{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate}},{'type':'v2','data':[start_time,end_time,q1_index,q2_index,.....,qk_index]},{'type':'v1','data':200}]}
            '''
            if self.burst['len'] == 0:
                return 0
            elif self.burst['b'][0]['type'] == 'v1':
                if times>=self.burst['b'][0]['data'] and times<self.burst['b'][0]['data']+100:
                    bcome = 1.5 * np.random.normal(loc=1, scale=0.2, size=None) / 8
                elif times == self.burst['b'][0]['data'] + 100:
                    self.burst['b'].pop(0)
                    self.burst['len'] = self.burst['len'] -1
            elif self.burst['b'][0]['type'] == 'v2':
                if times>=self.burst['b'][0]['data'][0] and times<self.burst['b'][0]['data'][1]:
                    bcome = 1.5 * np.random.normal(loc=1, scale=0.2, size=None) / len(self.burst['b'][0]['data'][2:])
                elif times==self.burst['b'][0]['data'][1]:
                    self.burst['b'].pop(0)
                    self.burst['len'] = self.burst['len'] - 1
            elif self.burst['b'][0]['type'] == 'v3':
                if times>=self.burst['b'][0]['data']['start_time'] and times<self.burst['b'][0]['data']['end_time']:
                    bcome = self.burst['b'][0]['data']['q{}'.format(q)] * np.random.normal(loc=1, scale=0.2, size=None)
                elif times == self.burst['b'][0]['data']['end_time']:
                    self.burst['b'].pop(0)
                    self.burst['len'] = self.burst['len'] - 1
        if bcome<0:
            return 0
        elif self.print_log and bcome:
            self.log("rate burst at {} ms,more {}  in queue{}".format(times, bcome, q))
        return bcome

    def ECN_handle(self,q,come):
        drop = 0
        if self.queue[q]+come>self.queue_size:
            drop = self.queue[q]+come-self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q,drop))
        '''
        目前队列为queue[q],接收该时刻的来包后为queue[q]+come,应该在范围[queue[q],queue[q]+come]对ECN_mark函数积分
        离散
        '''
        '''
        start_q = int(self.queue[q])
        self.queue[q] = self.queue[q]+come
        end_q = int(self.queue[q])
        for qlen in range(start_q,end_q+1):
            ECN_MARK = self.ECN_MARK_probability(qlen)
            if ECN_MARK == True and self.print_log:
                self.log("queue{} {}th packet is ecn marked".format(q,qlen))
        '''
        '''
        连续
        '''
        before = self.ECN_MARK_probability(self.queue[q])
        self.queue[q] = self.queue[q]+come
        after =self.ECN_MARK_probability(self.queue[q])
        ECN_MARK = (after-before)*np.random.normal(loc=1, scale=0.2, size=None)
        if ECN_MARK>come:
            ECN_MARK = come
        elif ECN_MARK<0:
            ECN_MARK = 0
        if self.print_log and ECN_MARK!=0:
            self.log("queue{} come {} packets and {} packets is ecn marked".format(q,come,ECN_MARK))
        return drop,ECN_MARK
    def ECN_MARK_probability(self,qlen):
        #=======================离散化计算=========================#
        '''
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
        '''
        #======================连续函数积分==========================#
        if qlen<=self.ECN_KMIN:
            return 0
        elif qlen<=self.ECN_KMAX:
            #################
            return (0+0.5*(qlen-self.ECN_KMIN)*self.ECN_PMAX*(qlen-self.ECN_KMIN)/(self.ECN_KMAX - self.ECN_KMIN))
        else :
            return (0+0.5*(self.ECN_KMAX-self.ECN_KMIN)*self.ECN_PMAX+1*(qlen-self.ECN_KMAX))

    def AQM_handle(self,q,come):
        if self.queue[q] + come > self.queue_size:
            drop = self.queue[q] + come - self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q, drop))
        '''
        start_q = int(self.queue[q])
        self.queue[q] = (self.queue[q] + come)
        end_q = int(self.queue[q])
        DROP = 0
        for qlen in range(start_q,end_q+1):
            AQM_DROP = self.AQM_DROP_probability(qlen)
            if AQM_DROP == True and self.print_log:
                DROP = DROP + 1
                self.log("queue{} {}th packet is AQM droped".format(q, qlen))
        '''
        before = self.ECN_MARK_probability(self.queue[q])
        self.queue[q] = self.queue[q] + come
        after = self.ECN_MARK_probability(self.queue[q])
        DROP = (after - before) * np.random.normal(loc=1, scale=0.1, size=None)
        if  DROP > come:
            DROP = come
        elif  DROP < 0:
            DROP = 0
        if self.print_log and  DROP != 0:
            self.log("queue{} come {} packets and {} packets is ecn marked".format(q, come,  DROP))
        self.queue[q] = self.queue[q] - DROP
        return DROP,0
    def AQM_DROP_probability(self,qlen):
        '''
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
        '''
        if qlen <= self.AQM_MIN_THRESH:
            return 0
        elif qlen <= self.AQM_MAX_THRESH:
            #################
            return (0 + 0.5 * (qlen - self.AQM_MIN_THRESH) * self.AQM_PMAX * (qlen - self.AQM_MIN_THRESH) / (self.AQM_MAX_THRESH - self.AQM_MIN_THRESH))
        else:
            return (0 + 0.5 * (self.AQM_MAX_THRESH - self.AQM_MIN_THRESH) * self.AQM_PMAX + 1 * (qlen - self.AQM_MAX_THRESH))
    def DROP_handle(self,q,come):
        drop = 0
        if self.queue[q] + come > self.queue_size:
            drop = self.queue[q] + come - self.queue_size
            come = self.queue_size - self.queue[q]
            if self.print_log:
                self.log("queue{} if full,drop {}packets".format(q, drop))
        self.queue[q] = self.queue[q] + come
        return  drop,0
    def Strict_priority_algorithm(self):
        q = 0
        for _q in range(self.priority):
            if self.queue[_q]>0.5:
                return _q,min(self.queue[_q],1)
        return q,self.queue[q]

    def WITTLE_algorithm(self):
        WI = self.WITTLE[0][self.EXP_cache['q0'][0]]
        q = 0
        for _q in range(self.priority-1):
            if self.WITTLE[_q+1][self.EXP_cache[f'q{_q+1}'][0]]>WI:
                WI = self.WITTLE[_q+1][self.EXP_cache[f'q{_q+1}'][0]]
                q = _q+1
        return q,min(self.queue[q],1)

    def MAX_QUEUE_LEN_algorithm(self):
        QLEN = self.queue[0]
        q = 0
        for _q in range(self.priority-1):
            if self.queue[_q+1]>QLEN:
                QLEN = self.queue[_q+1]
                q = _q+1
        # if self.queue[q]>1:
        #     return q,1
        return q,min(self.queue[q],1)

    # def WITTLE_INSERT(self,WITTLE):
    #     for q in range(self.priority):
    #         for s in range(self.vs):
    #             self.WITTLE[q][s] = WITTLE[q][s]

    def run(self,times):
        self.inpacket(times)
        if self.print_log or 1:
            self.log("queuelen:{}".format(self.queue))
        self.state_Collect(times)
        self.outpacket(times)

    def state_Collect(self,times):
        data = {'TIME':times,'TYPE':'S','DATA':[]}
        for q in range(self.priority):
            QLEN = round(self.queue[q])
            U = np.sum(self.queue[0:q])/np.sum(self.queue)
            U = round(U/self.u_unit)
            S = QLEN*int(1+1/self.u_unit)+U
            data['DATA'].append(S)
        self.EXP_Collect(data)

    def action_Collect(self,times,q):
        data = {'TIME':times,'TYPE':'A','DATA':[0,0,0,0,0,0,0,0]}
        data['DATA'][q] = 1
        self.EXP_Collect(data)

    def EXP_Collect(self,data:dict):
        '''
        函数接收字典类型：
        DATA = {'TIME':0,'TYPE':'S'or'A','DATA':[]}
        cache数据类型：
        EXP_cache = {'q0':[],'q1':[],'q2':[],'q3':[],'q4':[],'q5':[],'q6':[],'q7':[]}
        经验数据使用字典类型：
        EXP = {"PORT":2,'LEN':1000,'q0':[[s a s']....[s,a',s']],....,'q7':[s a s']}
        '''
        for q in range(self.priority):
            self.EXP_cache['q{}'.format(q)].append(data['DATA'][q])
        if data['TYPE'] == 'S' and len(self.EXP_cache['q0']) == 3:
            for q in range(self.priority):

                self.EXP_POOL['q{}'.format(q)].append(self.EXP_cache['q{}'.format(q)])
                if self.print_log:
                    self.log(f"S：q{q}:{self.EXP_cache['q{}'.format(q)]}")
                self.EXP_cache['q{}'.format(q)] = []
                self.EXP_cache['q{}'.format(q)].append(data['DATA'][q])
            self.EXP_POOL['LEN'] = self.EXP_POOL['LEN'] + 1
        if self.EXP_POOL['LEN'] == 1000:
            self.UP_LOAD = True


    def EXP_Clear(self):
        for q in range(self.priority):
            self.EXP_POOL['q{}'.format(q)].clear()
        self.EXP_POOL['LEN'] = 0
        self.UP_LOAD = 0
    def performance_update(self,drop,ecn,q):
        '''
        {'len':0,'drop':0,'ecn':0,'time':0}
        '''
        if  self.performance_update_flag:

            drops = self.performance[f'q{q}']['drop']
            ecns = self.performance[f'q{q}']['ecn']
            times = self.performance[f'q{q}']['time']
            lens = self.performance[f'q{q}']['len']
            self.performance[f'q{q}']['drop'] = (drops*times+drop)/(times+1)
            self.performance[f'q{q}']['ecn'] = (ecns*times+ecn)/(times+1)
            self.performance[f'q{q}']['len'] = (lens*times+self.queue[q])/(times+1)
            self.performance[f'q{q}']['time'] = times +1


