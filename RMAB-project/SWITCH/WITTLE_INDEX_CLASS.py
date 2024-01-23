import os

import numpy as np
class wittle_index():
    def __init__(self,Vs):
        self.vs = Vs #状态空间大小
        self.va = 2#动作空间大小
        #self.ptran = ptran#状态转移概率
        # self.R1 = Reward[1]#动作1的REWARD，size = vs
        # self.R0 = Reward[0]#动作0的REWARD.size = vs
        self.Q = np.random.rand(Vs)
        self.WI = np.ones(Vs)
        self.gamma = 0.99
    def calculate_WITTLE(self,R1,R0,ptran):
        print(len(R1),len(R0),np.shape(ptran))
        for s in range(self.vs):
            wittle_old = self.WI[s]-1
            step = 0
            while abs(wittle_old - self.WI[s])>0.001:
                wittle_old = self.WI[s]
                self.WI[s] = R1[s]+np.sum(ptran[1][s][j] * self.Q[j] for j in range(self.vs)) - R0[s] - np.sum(ptran[0][s][j] * self.Q[j] for j in range(self.vs))
                for _s in range(self.vs):
                        self.Q[_s] = np.max([R1[_s]-self.WI[s]+self.gamma*np.sum(ptran[1][_s][j] * self.Q[j] for j in range(self.vs)),R0[_s] + self.gamma*np.sum(ptran[0][_s][j] * self.Q[j] for j in range(self.vs))])
                step = step + 1
            print(s,self.WI[s],step)
#REWARD计算
class W_fair_drop():
    def __init__(self,wf):
        self.wf = wf
        self.wecn = 1-wf
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

class MDP():
    def __init__(self,qlen_size,pool_size):
        self.qlen_size = qlen_size
        self.u_unit = 0.05
        #=================pool==================
        self.expercience_pool = []
        self.pool_size = pool_size
        #=======================================
        self.vs = int((qlen_size+1)*(1+1/self.u_unit))
        self.va = 2  # 动作空间大小
        self.DIR_EXP_POOL = "./EXP_POOL"
        #====================ptran R===================
        self.ptran = []
        self.ptran_len = []
        self.R = []
        #===================update flag================
        self.update = False
    def s_to_u_qlen(self,s):
        qlen = int(s/(self.qlen_size+1))
        u = (s%(self.qlen_size+1))*self.u_unit
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

            self.ptran_len.clear()
            self.ptran_len.append(np.zeros(self.vs))
            self.ptran_len.append(np.zeros(self.vs))
            self.ptran.clear()
            self.ptran.append(np.zeros((self.vs, self.vs),dtype=float))
            self.ptran.append(np.zeros((self.vs, self.vs),dtype=float))
            #==========当size_num=size时已经说明处理了将经验全部读取================
            while line and line!="\n":

                s = int(line.split(" ")[0])
                a = int(line.split(" ")[1])
                ss = int(line.split(" ")[2].split("\n")[0])
                self.ptran_len[a][s] = self.ptran_len[a][s] + 1
                self.ptran[a][s][ss] = self.ptran[a][s][ss] + 1
                line = file.readline()
            file.close()
        for action in range(2):
            for s in range(self.vs):
                for ss in range(self.vs):
                    if self.ptran_len[action][s] !=0:
                        self.ptran[action][s][ss] = self.ptran[action][s][ss] /self.ptran_len[action][s]
                    elif s == ss:###当没有出现(s,a)样本时，设置ptran(s,a,s)=1
                        self.ptran[action][s][ss] = 1

    def Reward_matrix(self,reward:W_fair_drop):
        '''
        返回Reward矩阵，
        '''
        self.R.clear()
        self.R.append(np.zeros(self.vs))
        self.R.append(np.zeros(self.vs))
        for a in range(self.va):
            for s in range(self.vs):
                u,qlen = self.s_to_u_qlen(s)
                self.R[a][s] = reward.Wreward(u,qlen,a)


# MDP_MODEL = MDP(qlen_size=20,pool_size=320000)
# r = W_fair_drop(wf=0.2)
# MDP_MODEL.Reward_matrix(reward=r)
# MDP_MODEL.file_exp_to_ptran(PORT=1,q=0)
# WITTLE_MODEL = wittle_index(21*21)
# WITTLE_MODEL.calculate_WITTLE(epoch=2000, R1=MDP_MODEL.R[1], R0=MDP_MODEL.R[0], ptran=MDP_MODEL.ptran)
# for j in range(441):
#     print(MDP_MODEL.ptran[0][j], np.sum(MDP_MODEL.ptran[0][j]), MDP_MODEL.ptran_len[0][j])
#     print(MDP_MODEL.ptran[1][j], np.sum(MDP_MODEL.ptran[1][j]), MDP_MODEL.ptran_len[1][j])
# # print(mdp.R[0],len(mdp.R[0]))




