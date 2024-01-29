import  numpy as np
class init_ptran():
    def __init__(self,qlen_size,drop_size,u_unit):
        self.vs = int((qlen_size+drop_size+1)*(1+1/u_unit))
        self.u_num = int(1+1/u_unit)
        self.q_num = int(qlen_size+drop_size+1)
        ptran = []

        ptran.append(np.zeros((self.vs, self.vs), dtype=float))
        ptran.append(np.zeros((self.vs, self.vs), dtype=float))
        #a = 0
        for s in range(self.vs):
            qlen = int(s/self.u_num)
            u = s%self.u_num
            if qlen!=self.q_num-1:
                if u!=0 and u!=self.u_num-1:
                    ptran[0][s][s-1] = 0.8*0.05
                    ptran[0][s][s] = 0.8*0.9
                    ptran[0][s][s+1] = 0.8*0.05
                    ptran[0][s][s+6-1] = 0.2*0.05
                    ptran[0][s][s+6] = 0.2*0.9
                    ptran[0][s][s+6+1] = 0.2*0.05
                if u==0:
                    ptran[0][s][s] = 0.8 * 0.95
                    ptran[0][s][s + 1] = 0.8 * 0.05
                    ptran[0][s][s + 6] = 0.2 * 0.95
                    ptran[0][s][s + 6 + 1] = 0.2 * 0.05
                if u == self.u_num-1:
                    ptran[0][s][s - 1] = 0.8 * 0.05
                    ptran[0][s][s] = 0.8 * 0.95
                    ptran[0][s][s + 6 - 1] = 0.2 * 0.05
                    ptran[0][s][s + 6] = 0.2 * 0.95
            if qlen == self.q_num-1:
                if u!=0 and u!=self.u_num-1:
                    ptran[0][s][s-1] = 1*0.05
                    ptran[0][s][s] = 1*0.9
                    ptran[0][s][s+1] = 1*0.05
                if u==0:
                    ptran[0][s][s] = 1 * 0.95
                    ptran[0][s][s + 1] = 1 * 0.05
                if u == self.u_num-1:
                    ptran[0][s][s - 1] = 1 * 0.05
                    ptran[0][s][s] = 1 * 0.95
        #a = 1
        for s in range(self.vs):
            qlen = int(s/self.u_num)
            u = s%self.u_num
            if qlen!=self.q_num-1 and qlen!=0:
                if u != 0 and u != self.u_num-1:
                    ptran[1][s][s-6-1] = 0.7*0.02
                    ptran[1][s][s-6] = 0.7*0.9
                    ptran[1][s][s-6+1] = 0.7*0.08
                    ptran[1][s][s  - 1] = 0.25 * 0.02
                    ptran[1][s][s] = 0.25  * 0.9
                    ptran[1][s][s  + 1] = 0.25  * 0.08
                    ptran[1][s][s +6- 1] = 0.05 * 0.02
                    ptran[1][s][s+6] = 0.05 * 0.9
                    ptran[1][s][s +6+ 1] = 0.05 * 0.08
                if u==0:
                    ptran[1][s][s - 6] = 0.7 * 0.92
                    ptran[1][s][s - 6 + 1] = 0.7 * 0.08
                    ptran[1][s][s] = 0.25 * 0.92
                    ptran[1][s][s + 1] = 0.25 * 0.08
                    ptran[1][s][s + 6] = 0.05 * 0.92
                    ptran[1][s][s + 6 + 1] = 0.05 * 0.08
                if u==self.u_num-1:
                    ptran[1][s][s - 6 - 1] = 0.7 * 0.02
                    ptran[1][s][s - 6] = 0.7 * 0.98
                    ptran[1][s][s - 1] = 0.25 * 0.02
                    ptran[1][s][s] = 0.25 * 0.98
                    ptran[1][s][s + 6 - 1] = 0.05 * 0.02
                    ptran[1][s][s + 6] = 0.05 * 0.98
            if qlen == 0:
                if u != 0 and u != self.u_num-1:
                    ptran[1][s][s - 1] = 0.95 * 0.02
                    ptran[1][s][s] = 0.95 * 0.9
                    ptran[1][s][s + 1] = 0.95 * 0.08
                    ptran[1][s][s + 6 - 1] = 0.05 * 0.02
                    ptran[1][s][s + 6] = 0.05 * 0.9
                    ptran[1][s][s + 6 + 1] = 0.05 * 0.08
                if u==0:
                    ptran[1][s][s] = 0.95 * 0.92
                    ptran[1][s][s + 1] = 0.95 * 0.08
                    ptran[1][s][s + 6] = 0.05 * 0.92
                    ptran[1][s][s + 6 + 1] = 0.05 * 0.08
                if u==self.u_num-1:
                    ptran[1][s][s - 1] = 0.95 * 0.02
                    ptran[1][s][s] = 0.95 * 0.98
                    ptran[1][s][s + 6 - 1] = 0.05 * 0.02
                    ptran[1][s][s + 6] = 0.05 * 0.98
            if qlen==self.q_num-1:
                if u != 0 and u != self.u_num-1:
                    ptran[1][s][s - 6 - 1] = 0.7 * 0.02
                    ptran[1][s][s - 6] = 0.7 * 0.9
                    ptran[1][s][s - 6 + 1] = 0.7 * 0.08
                    ptran[1][s][s - 1] = 0.3 * 0.02
                    ptran[1][s][s] = 0.3 * 0.9
                    ptran[1][s][s + 1] = 0.3 * 0.08
                if u==0:
                    ptran[1][s][s - 6] = 0.7 * 0.92
                    ptran[1][s][s - 6 + 1] = 0.7 * 0.08
                    ptran[1][s][s] = 0.3 * 0.92
                    ptran[1][s][s + 1] = 0.3 * 0.08
                if u==self.u_num-1:
                    ptran[1][s][s - 6 - 1] = 0.7 * 0.02
                    ptran[1][s][s - 6] = 0.7 * 0.98
                    ptran[1][s][s - 1] = 0.3 * 0.02
                    ptran[1][s][s] = 0.3 * 0.98

# import  sys
# np.set_printoptions(threshold=sys.maxsize)
# MDP_MODEL = MDP(qlen_size=20,u_unit=0.2,drop_size=1)
# REWARD_MODEL = W_fair_ecn_drop(wf=0.2,we=0.6,wd=0.2,queue_size=20,u_unit=0.2)
# MDP_MODEL.Reward_matrix(REWARD_MODEL)
# print(MDP_MODEL.R[1])
#
# WITTLE_MODEL = wittle_index(vs)
#
#
#
# for q in range(1):
#     #MDP_MODEL.file_exp_to_ptran(1,q)
#     WI = WITTLE_MODEL.calculate_WITTLE(MDP_MODEL.R[1],MDP_MODEL.R[0],ptran)
#     print(repr(WI.reshape((22,6))))