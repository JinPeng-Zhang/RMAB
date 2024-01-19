import numpy as np
class wittle_index():
    def __init__(self,Vs):
        self.vs = Vs #状态空间大小
        self.va = 2#动作空间大小
        #self.ptran = ptran#状态转移概率
        # self.R1 = Reward[1]#动作1的REWARD，size = vs
        # self.R0 = Reward[0]#动作0的REWARD.size = vs
        self.Q = np.random.rand(Vs)
        self.WI = np.zeros(Vs)
        self.gamma = 0.75
    def calculate_WITTLE(self,epoch,R1,R0,ptran):
        for s in range(self.vs):
            for step in range(epoch):
                wittle_old = self.WI[s]
                self.WI[s] = R1[s]+np.sum(ptran[1][s][j] * self.Q[j] for j in range(self.vs)) \
                                - R0[s] - np.sum(ptran[0][s][j] * self.Q[j] for j in range(self.vs))
                for _s in range(self.vs):
                        self.Q[_s] = np.max(R1[_s]+self.gamma*np.sum(ptran[1][_s][j] * self.Q[j] for j in range(self.vs)),R0[_s] + np.sum(ptran[0][_s][j] * self.Q[j] for j in range(self.vs)))
                if abs(wittle_old - self.WI[s])<0.001:
                        break
#REWARD计算
class W_fair_drop():
    def __init__(self,wf,wecn):
        self.wf = wf
        self.wecn = wecn
        self.max_qlen = 20
        #======================ECN MARK======================#
        self.kmin = self.max_qlen*0.2
        self.kmax = self.max_qlen*0.6
        self.pmax = 0.8
        self.normalization_max = 0+0.5*(self.kmax-self.kmin)*self.pmax+1*(self.max_qlen-self.kmax)#用于ECN_MARK归一化
        #=====================FARI ===========================#
        self.u_unit = 0.05
    def ECN_mark(self,qlen):
        if qlen<self.kmin:
            return 0
        elif qlen<self.kmax:
            #################
            return (0+0.5*(qlen-self.kmin)*self.pmax*(qlen-self.kmin)/(self.kmax - self.kmin))/self.normalization_max
        else :
            return (0+0.5*(self.kmax-self.kmin)*self.pmax+1*(qlen-self.kmax))/self.normalization_max
    def fair(self,u,a):
        return  1-(u-u%self.u_unit+self.u_unit)*a
    def Wreward(self,u,qlen,a):
        return self.wf*self.fair(u,a)+self.wecn*self.ECN_mark(qlen)

class MDP():
    def __init__(self,qlen_size,pool_size):
        self.qlen_size = qlen_size
        self.u_unit = 0.05
        #=================pool==================
        self.expercience_pool = []
        self.pool_size = pool_size
        #=======================================
        self.vs = int((qlen_size+1)/self.u_unit)


    def s_to_u_qlen(self,s):
        qlen = int(s/self.qlen_size)
        u = (s%self.qlen_size)*self.u_unit
        return u,qlen
    def add_exp(self,exp):
        lens = len(self.expercience_pool)
        if lens>self.pool_size:
            popexp = self.expercience_pool.pop(0)
            self.expercience_pool.append(exp)
            # s, a, ss = popexp
            # tims = np.around(self.ptran[a][s][ss] * self.ptran_len[a][s])
            # tims = tims - 1
            # self.ptran_len[a][s] = self.ptran_len[a][s] - 1
            # if self.ptran_len[a][s] == 0:
            #     self.ptran[a][s][ss] = 0
            # else:
            #     self.ptran[a][s][ss] = tims / self.ptran_len[a][s]
        else:
            self.expercience_pool.append(exp)
        # s, a, ss = popexp
        # self.ptran_len[a][s] = (np.around(self.ptran[a][s][ss] * self.ptran_len[a][s])+1)/(self.ptran_len[a][s] + 1)
        # self.ptran_len[a][s] = self.ptran_len[a][s] + 1
    def exp_to_ptran(self):
        self.ptran_len = []
        self.ptran_len.append(np.zeros(self.vs))
        self.ptran_len.append(np.zeros(self.vs))
        self.ptran = []
        self.ptran.append(np.zeros((self.vs, self.vs)))
        self.ptran.append(np.zeros((self.vs, self.vs)))
        for exp in self.expercience_pool:
            s,a,ss = exp
            self.ptran_len[a][s] = self.ptran_len[a][s] + 1
            self.ptran[a][s][ss] = self.ptran_len[a][s][ss] + 1
        for action in range(2):
            for s in range(self.qlen_size):
                for ss in range(self.qlen_size):
                    if self.ptran_len[action][s] !=0:
                        self.ptran[action][s][ss] = self.ptran[action][s][ss] /self.ptran_len[action][s]
                    else:###当没有出现(s,a)样本时，设置ptran(s,a,s)=1
                        self.ptran[action][s][ss] = 1
    def exp_to_file(self,q,type):
        pass


# MDP_MODEL =  MDP()
# REWARD_MODEL = W_fair_drop()
# WITTLE_MODEL = wittle_index()
# 在线学习部分：
#     1.观察时间T,采集样本到MDP_MODEL的经验 POOL中,元组(s,a,ss)
#     2.采集样本，并使用MDP_MODEL的exp_to_ptran计算PTRAN(转移概率矩阵)
#     3.创建数组R0 R1,对应动作0 1,循环状态空间vs,使用MDP_MODEL的函数s_to_u_qlen将状态空间映射的公平性参数u和队列长度qlen
#     4.根据公平性参数u和队列长度qlen，使用REWARD_MODEL的Wreward函数计算出RO R1
#     5.得到RO R1 PTRAN(转移概率矩阵)后，调用WITTLE_MODEL计算出WITTLE值
#     6.周期性▲t(建议5分钟更新一次)循环步骤2-5



