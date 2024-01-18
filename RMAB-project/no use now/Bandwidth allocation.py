#import torch
import  math
import numpy as np
import  gurobipy as gp
from gurobipy import GRB
#####

queuenum = 8
STATE_MAX = 30
pcome = np.random.rand((queuenum))/4
while sum(pcome)>=1:
    pcome = np.random.rand((queuenum))/1.5
pcome = [0.45055527,0.61662127,0.00071802,0.27875661,0.4501263, 0.34989907,0.16383102,0.58007069]
def poission(k,expect=0.3):
    return expect**k/math.factorial(k)*math.e**(-expect)
P0 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P1 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
for q in range(queuenum):
    for i in range(STATE_MAX):
        for j in range(STATE_MAX):
            if j>=i and j!=STATE_MAX-1:
                P0[q][i][j] = poission(j-i,expect=pcome[q])
            elif j == STATE_MAX-1:
                P0[q][i][j] = 1-sum(P0[q][i])
            if i == 0:
                P1[q][i][j] = poission(j - i,expect=pcome[q])
            if j>=i-1 and j!=STATE_MAX-1 and i !=0:
                P1[q][i][j] = poission(j-i+1,expect=pcome[q])
            elif j==STATE_MAX-1:
                P1[q][i][j] = 1 - sum(P1[q][i])

m = gp.Model("width_allocation")
m.Params.MIPGap = 10**(-3)
ptran = m.addMVar((queuenum,STATE_MAX,STATE_MAX),vtype = 'C',name="ptran",lb=0,ub=1)

width = m.addMVar((queuenum), vtype = 'C',name="width",lb=0,ub=1)
ps = m.addMVar((queuenum,STATE_MAX),vtype='C',name="ps",lb=0,ub=1)
ES = m.addMVar((queuenum),vtype='C',name="ES")

for q in range(queuenum):
    for s in range(STATE_MAX):
        for ss in range(STATE_MAX):
            m.addConstr(ptran[q][s][ss] == width[q]*P1[q][s][ss]+(1-width[q])*P0[q][s][ss])
m.addConstr(sum(width) == 1)
for q in range(queuenum):
    for s in range(STATE_MAX):
        m.addConstr(sum(ps[q][i]*ptran[q][i][s] for i in range(STATE_MAX)) == ps[q][s])
for q in range(queuenum):
        m.addConstr(ES[q] == sum(ps[q][s]*s for s in range(STATE_MAX)))
for q in range(queuenum):
    m.addConstr(sum(ps[q][i] for i in range(STATE_MAX)) == 1)
m.setObjective(sum(ES[i] for i in range(queuenum)), GRB.MINIMIZE)

m.Params.NonConvex = 2
m.optimize()

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
#S = 10
#[0.45055527,0.61662127,0.00071802,0.27875661,0.4501263, 0.34989907,0.16383102,0.58007069]
# width[0] 0
# width[1] 0
# width[2] 0.00654217
# width[3] 0.348534
# width[4] 0
# width[5] 0.410281
# width[6] 0.234643
# width[7] 0
# ES[0] 9
# ES[1] 9
# ES[2] 0.121263
# ES[3] 2.65571
# ES[4] 9
# ES[5] 3.1139
# ES[6] 1.92896
# ES[7] 9

#S = 20
#[0.45055527,0.61662127,0.00071802,0.27875661,0.4501263, 0.34989907,0.16383102,0.58007069]
# width[0] 0
# width[1] 0
# width[2] 0.00469047
# width[3] 0.349632
# width[4] -1.97872e-07
# width[5] 0.423355
# width[6] 0.222323
# width[7] 0
# ES[0] 19
# ES[1] 18.9998
# ES[2] 0.179602
# ES[3] 3.27696 3,933
# ES[4] 19
# ES[5] 3.74191 4.76
# ES[6] 2.54114 2.8
# ES[7] 18.9999
# Obj: 85.7393

#S = 25
#[0.45055527,0.61662127,0.00071802,0.27875661,0.4501263, 0.34989907,0.16383102,0.58007069]
# width[0] 0
# width[1] -1.31019e-06
# width[2] 0.00467455
# width[3] 0.34886
# width[4] 0
# width[5] 0.42497
# width[6] 0.221496
# width[7] 1.93981e-10
#
# ES[0] 24
# ES[1] 24
# ES[2] 0.181727 0.181477
# ES[3] 3.3773 3.976
# ES[4] 23.9999
# ES[5] 3.77347  4.66
# ES[6] 2.58707  2.84
# ES[7] 23.9999
# Obj: 105.919


#S = 30
#[0.45055527,0.61662127,0.00071802,0.27875661,0.4501263, 0.34989907,0.16383102,0.58007069]V
# width[0] 3.9964e-11
# width[1] 3.38565e-11
# width[2] 0.00453163
# width[3] 0.348775
# width[4] 4.1298e-11
# width[5] 0.426169
# width[6] 0.220524
# width[7] 0
#
# ES[0] 28.9999
# ES[1] 28.9999
# ES[2] 0.188198 0.188278
# ES[3] 3.39651  3.98
# ES[4] 28.9999
# ES[5] 3.74756 4.5876
# ES[6] 2.62067 2.88979
# ES[7] 28.9999
# Obj: 125.953

