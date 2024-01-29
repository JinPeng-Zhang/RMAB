import os

import numpy as np
from heatmap.ptran import init_ptran
class wittle_index():
    def __init__(self,Vs):
        self.vs = Vs #状态空间大小
        self.va = 2#动作空间大小
        #self.ptran = ptran#状态转移概率
        # self.R1 = Reward[1]#动作1的REWARD，size = vs
        # self.R0 = Reward[0]#动作0的REWARD.size = vs
        self.gamma = 0.75
    def calculate_WITTLE(self,R1,R0,ptran):
        Q = np.random.rand(self.vs)
        WI = np.ones(self.vs)
        for s in range(self.vs):
            wittle_old = WI[s]-1
            step = 0
            more_s = 0
            while abs(wittle_old - WI[s])>0.001 and step<200:
                wittle_old = WI[s]
                WI[s] = R1[s]+np.sum(ptran[1][s][j] * Q[j] for j in range(self.vs)) - R0[s] - np.sum(ptran[0][s][j] * Q[j] for j in range(self.vs))
                for u in range(1+more_s):
                    for _s in range(self.vs):
                            Q[_s] = np.max([R1[_s]-WI[s]+self.gamma*np.sum(ptran[1][_s][j] * Q[j] for j in range(self.vs)),R0[_s] + self.gamma*np.sum(ptran[0][_s][j] * Q[j] for j in range(self.vs))])
                step = step + 1
                if step%50 == 0:
                    more_s = more_s+int(step/50)
        return WI
#REWARD计算
class W_fair_drop():
    def __init__(self,wf,queue_size,u_unit):
        self.wf = wf
        self.wecn = 1-wf
        self.max_qlen = queue_size
        #======================ECN MARK======================#
        self.kmin = self.max_qlen*0.2
        self.kmax = self.max_qlen*0.6
        self.pmax = 0.8
        self.normalization_max = 0+0.5*(self.kmax-self.kmin)*self.pmax+1*(self.max_qlen-self.kmax)#用于ECN_MARK归一化
        #=====================FARI ===========================#
        self.u_unit = u_unit
    def ECN_mark(self,qlen):
        if qlen<self.kmin:
            return 0
        elif qlen<=self.kmax:
            #################
            return (0+0.5*(qlen-self.kmin)*self.pmax*(qlen-self.kmin)/(self.kmax - self.kmin))/self.normalization_max
        else :
            return (0+0.5*(self.kmax-self.kmin)*self.pmax+1*(qlen-self.kmax))/self.normalization_max
    def fair(self,u,a):
        #向上取整改为四舍五入
        #return  1-(u-u%self.u_unit+self.u_unit)*a
        return 1 - round(u/self.u_unit)*self.u_unit * a
    def Wreward(self,u,qlen,a):
        return self.wf*self.fair(u,a)+self.wecn*(1-self.ECN_mark(qlen))
class W_fair_ecn_drop():
    def __init__(self,wf,we,wd,queue_size,u_unit):
        self.wf = wf
        self.wecn = we
        self.wdrop = wd
        self.max_qlen = queue_size
        #======================ECN MARK======================#
        self.kmin = self.max_qlen*0.2
        self.kmax = self.max_qlen*0.6
        self.pmax = 0.8
        self.normalization_max = 0+0.5*(self.kmax-self.kmin)*self.pmax+1*(self.max_qlen-self.kmax)#用于ECN_MARK归一化
        #=====================FARI ===========================#
        self.u_unit = u_unit

    def ECN_mark(self,qlen):
        if qlen<self.kmin:
            return 0
        elif qlen<=self.kmax:
            #################
            return (0+0.5*(qlen-self.kmin)*self.pmax*(qlen-self.kmin)/(self.kmax - self.kmin))/self.normalization_max
        else :
            return (0+0.5*(self.kmax-self.kmin)*self.pmax+1*(qlen-self.kmax))/self.normalization_max
    def fair(self,u,a):
        #向上取整改为四舍五入
        #return  1-(u-u%self.u_unit+self.u_unit)*a
        return 1 - round(u/self.u_unit)*self.u_unit * a
    def drop(self,qlen,flag):
        '''
        丢包率和队列长度的关系需要统计，此处先假定符合下面变化
        flag用于区分最大队列长度的状态
        '''
        return  1/(2+self.max_qlen-qlen-flag)
    def Wreward(self,u,qlen,a,drop_ready,drop_s):
        flag = 0
        if qlen>self.max_qlen:
            qlen = self.max_qlen
            flag = 1
        if not drop_ready:
            return self.wf*self.fair(u,a)+self.wecn*(1-self.ECN_mark(qlen))+self.wdrop*(1-self.drop(qlen,flag))
        else:
            return self.wf*self.fair(u,a)+self.wecn*(1-self.ECN_mark(qlen))+self.wdrop*(1-drop_s[qlen+flag])
class MDP():
    def __init__(self,qlen_size,u_unit,drop_size,R_class):
        self.qlen_size = qlen_size
        self.drop_size = drop_size
        self.u_unit = u_unit
        #=================pool==================
        #self.expercience_pool = []
        #self.pool_size = pool_size
        #=======================================
        self.vs = int((self.qlen_size+drop_size+1)*(1+1/self.u_unit))
        self.va = 2  # 动作空间大小
        self.DIR_EXP_POOL = "./EXP_POOL"
        #====================ptran R===================
        self.ptran = []
        self.ptran_len = []
        self.R = []
        self.RF = R_class
        #===================update flag================
        self.update = False
        #==================丢包率统计===================
        self.drop_s = np.zeros(1+self.qlen_size+1)
        self.drop_s[-1] = 1
        self.drop_ready = False
    def s_to_u_qlen(self,s):
        fair = 1+1/self.u_unit
        qlen = int(s/fair)
        u = (s%fair)*self.u_unit
        return u,qlen
    # def add_exp(self,exp):
    #     lens = len(self.expercience_pool)
    #     if lens>self.pool_size:
    #         popexp = self.expercience_pool.pop(0)
    #         self.expercience_pool.append(exp)
    #         # s, a, ss = popexp
    #         # tims = np.around(self.ptran[a][s][ss] * self.ptran_len[a][s])
    #         # tims = tims - 1
    #         # self.ptran_len[a][s] = self.ptran_len[a][s] - 1
    #         # if self.ptran_len[a][s] == 0:
    #         #     self.ptran[a][s][ss] = 0
    #         # else:
    #         #     self.ptran[a][s][ss] = tims / self.ptran_len[a][s]
    #     else:
    #         self.expercience_pool.append(exp)
    #     # s, a, ss = popexp
    #     # self.ptran_len[a][s] = (np.around(self.ptran[a][s][ss] * self.ptran_len[a][s])+1)/(self.ptran_len[a][s] + 1)
    #     # self.ptran_len[a][s] = self.ptran_len[a][s] + 1

    def file_exp_to_ptran(self,PORT,q):
        '''
           从EXP文件池中读取数据，计算转移概率
        '''
        fair = 1 + 1 / self.u_unit
        init_p = init_ptran(qlen_size=self.qlen_size,drop_size=self.drop_size,u_unit=self.u_unit)
        self.ptran_len.clear()
        self.ptran_len.append(np.zeros(self.vs))
        self.ptran_len.append(np.zeros(self.vs))
        self.ptran.clear()
        self.ptran.append(np.zeros((self.vs, self.vs), dtype=float))
        self.ptran.append(np.zeros((self.vs, self.vs), dtype=float))
        port = "PORT_"+str(PORT)
        file_path = self.DIR_EXP_POOL + './' + port + '/'+'q{}'.format(q)+'./'


        for file_name in os.listdir(file_path):
            if file_name == "conf.txt":
                continue
            '''
            conf_name = self.DIR_EXP_POOL + './' + port + '/'+'conf.txt'
            conf = open(conf_name)
            #size = int(conf.readline().split('\n')[0])
            conf.close()
            '''
            file = open(file_path+file_name,'r')

            line = file.readline()


            #==========当size_num=size时已经说明处理了将经验全部读取================
            while line and line!="\n":

                s = int(line.split(" ")[0])
                a = int(line.split(" ")[1])
                d = float(line.split(" ")[2])
                ss = int(line.split(" ")[3].split("\n")[0])
                self.drop_s[int(s / fair)] = 0.8*self.drop_s[int(s / fair)]+0.2*d
                self.ptran_len[a][s] = self.ptran_len[a][s] + 1
                self.ptran[a][s][ss] = self.ptran[a][s][ss] + 1
                line = file.readline()
            file.close()
        self.drop_ready = True
        for action in range(2):
            for s in range(self.vs):
                for ss in range(self.vs):
                    if self.ptran_len[action][s] !=0:
                        self.ptran[action][s][ss] = self.ptran[action][s][ss] /self.ptran_len[action][s]
                    # elif s == ss:###当没有出现(s,a)样本时，设置ptran(s,a,s)=1
                    #     self.ptran[action][s][ss] = 1
                    else:####当没有出现（s，a）样本时，设置为初始转移矩阵
                        self.ptran[action][s][ss] = init_p[action][s][ss]

    def Reward_matrix(self):
        '''
        返回Reward矩阵，
        '''
        if self.RF.__class__.__name__ == "W_fair_drop":
            self.R.clear()
            self.R.append(np.zeros(self.vs))
            self.R.append(np.zeros(self.vs))
            for a in range(self.va):
                for s in range(self.vs):
                    u,qlen = self.s_to_u_qlen(s)
                    self.R[a][s] = self.RF.Wreward(u,qlen,a)
        elif self.RF.__class__.__name__ == "W_fair_ecn_drop":
            self.R.clear()
            self.R.append(np.zeros(self.vs))
            self.R.append(np.zeros(self.vs))
            for a in range(self.va):
                for s in range(self.vs):
                    u, qlen = self.s_to_u_qlen(s)
                    self.R[a][s] = self.RF.Wreward(u, qlen, a,self.drop_ready,self.drop_s)
            self.drop_ready = False








