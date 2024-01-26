import  numpy as np
from SWITCH.WITTLE_INDEX_CLASS import MDP,W_fair_drop, wittle_index
vs = 126
ptran = []
ptran.append(np.zeros((126, 126), dtype=float))
ptran.append(np.zeros((126, 126), dtype=float))
#a = 0
for s in range(vs):
    qlen = int(s/6)
    u = s%6
    if qlen!=20:
        if u!=0 and u!=5:
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
        if u == 5:
            ptran[0][s][s - 1] = 0.8 * 0.05
            ptran[0][s][s] = 0.8 * 0.95
            ptran[0][s][s + 6 - 1] = 0.2 * 0.05
            ptran[0][s][s + 6] = 0.2 * 0.95
    if qlen == 20:
        if u!=0 and u!=5:
            ptran[0][s][s-1] = 1*0.05
            ptran[0][s][s] = 1*0.9
            ptran[0][s][s+1] = 1*0.05
        if u==0:
            ptran[0][s][s] = 1 * 0.95
            ptran[0][s][s + 1] = 1 * 0.05
        if u == 5:
            ptran[0][s][s - 1] = 1 * 0.05
            ptran[0][s][s] = 1 * 0.95
#a = 1
for s in range(vs):
    qlen = int(s/6)
    u = s%6
    if qlen!=20 and qlen!=0:
        if u != 0 and u != 5:
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
        if u==5:
            ptran[1][s][s - 6 - 1] = 0.7 * 0.02
            ptran[1][s][s - 6] = 0.7 * 0.98
            ptran[1][s][s - 1] = 0.25 * 0.02
            ptran[1][s][s] = 0.25 * 0.98
            ptran[1][s][s + 6 - 1] = 0.05 * 0.02
            ptran[1][s][s + 6] = 0.05 * 0.98
    if qlen == 0:
        if u != 0 and u != 5:
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
        if u==5:
            ptran[1][s][s - 1] = 0.95 * 0.02
            ptran[1][s][s] = 0.95 * 0.98
            ptran[1][s][s + 6 - 1] = 0.05 * 0.02
            ptran[1][s][s + 6] = 0.05 * 0.98
    if qlen==20:
        if u != 0 and u != 5:
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
        if u==5:
            ptran[1][s][s - 6 - 1] = 0.7 * 0.02
            ptran[1][s][s - 6] = 0.7 * 0.98
            ptran[1][s][s - 1] = 0.3 * 0.02
            ptran[1][s][s] = 0.3 * 0.98

import  sys
np.set_printoptions(threshold=sys.maxsize)
MDP_MODEL = MDP(qlen_size=20,u_unit=0.2)
REWARD_MODEL = W_fair_drop(wf=0.2,queue_size=20,u_unit=0.2)
MDP_MODEL.Reward_matrix(REWARD_MODEL)
WITTLE_MODEL = wittle_index(126)



for q in range(8):
    #MDP_MODEL.file_exp_to_ptran(1,q)
    WI = WITTLE_MODEL.calculate_WITTLE(MDP_MODEL.R[1],MDP_MODEL.R[0],ptran)
    print(repr(WI.reshape((21,6))))