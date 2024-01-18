

#import torch
import  math
import numpy as np
import  gurobipy as gp
from gurobipy import GRB

import  matplotlib.pyplot as plt
#####

queuenum = 8
pcome = np.random.rand((queuenum))/4
while sum(pcome)>=0.7:
    pcome = np.random.rand((queuenum))/4
print(list(pcome))
pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ]

class Bandwidth_allocation():
    def __init__(self,pcome):
        self.STATE_MAX = 20
        self.pcome = pcome
        self.queuenum = len(pcome)
        self.P0 = np.zeros((self.queuenum, self.STATE_MAX, self.STATE_MAX))
        self.P1 = np.zeros((self.queuenum, self.STATE_MAX, self.STATE_MAX))
        self.m = gp.Model("width_allocation")
        self.rate =float
    def poission(self,k, expect=0.3):
        return expect ** k / math.factorial(k) * math.e ** (-expect)
    def computeP(self):
        for q in range(self.queuenum):
            for i in range(self.STATE_MAX):
                for j in range(self.STATE_MAX):
                    if j>=i and j!=self.STATE_MAX-1:
                        self.P0[q][i][j] = self.poission(j-i,expect=self.pcome[q])
                    elif j == self.STATE_MAX-1:
                        self.P0[q][i][j] = 1-sum(self.P0[q][i])
                    if i == 0:
                        self.P1[q][i][j] = self.poission(j - i,expect=self.pcome[q])
                    if j>=i-1 and j!=self.STATE_MAX-1 and i !=0:
                        self.P1[q][i][j] = self.poission(j-i+1,expect=self.pcome[q])
                    elif j==self.STATE_MAX-1:
                        self.P1[q][i][j] = 1 - sum(self.P1[q][i])

    def computeWidth(self):
        width = self.m.addMVar((self.queuenum), vtype = 'C',name="width",lb=0,ub=1)
        ps = self.m.addMVar((self.queuenum,self.STATE_MAX),vtype='C',name="ps",lb=0,ub=1)
        ES = self.m.addMVar((self.queuenum),vtype='C',name="ES")
        X = self.m.addMVar((self.queuenum,self.STATE_MAX,2),vtype='C',name="X",lb=0,ub=1)

        burst = self.m.addMVar((self.queuenum),vtype='C',name="burst",lb=0,ub=1)
        ratediff = self.m.addMVar((self.queuenum),vtype='C',name="ratediff",lb=0,ub=1)
        ratediff2 = self.m.addMVar((self.queuenum), vtype='C', name="ratediff2", lb=0, ub=1)
        for q in range(self.queuenum):
            self.m.addConstr(ratediff[q] == width[q]-pcome[q])
            self.m.addGenConstrPow(ratediff[q], ratediff2[q], 2)
            self.m.addGenConstrPow(ratediff2[q], burst[q], -1)

        for q in range(self.queuenum):
            self.m.addConstr(width[q] >= self.pcome[q])
        for q in range(self.queuenum):
            for s in range(self.STATE_MAX-1):
                self.m.addConstr(X[q][s+1][1]>=X[q][s][1])


        for q in range(self.queuenum):
            self.m.addConstr(width[q] == sum(ps[q][s]*X[q][s][1] for s in range(self.STATE_MAX)))
        self.m.addConstr(sum(width) == 1)
        for q in range(self.queuenum):
            for s in range(self.STATE_MAX):
                self.m.addConstr((sum(ps[q][i]*self.P0[q][i][s]*X[q][i][0] for i in range(self.STATE_MAX))+sum(ps[q][i]*self.P1[q][i][s]*X[q][i][1] for i in range(self.STATE_MAX))) == ps[q][s])
        for q in range(self.queuenum):
                self.m.addConstr(ES[q] == sum(ps[q][s]*s for s in range(self.STATE_MAX)))
        for q in range(self.queuenum):
            self.m.addConstr(sum(ps[q][i] for i in range(self.STATE_MAX)) == 1)
        for q in range(self.queuenum):
            for s in range(self.STATE_MAX):
                self.m.addConstr((X[q][s][0]+X[q][s][1] ) == 1)

        ###Extra


        self.m.setObjective(sum(ES), GRB.MINIMIZE)
        self.m.Params.NonConvex = 2
        self.m.optimize()

        wid = []
        for v in self.m.getVars():
            print('%s %g' % (v.varName,v.x))
            # if len(v.varName.split("width")) == 2:
            #     wid.append(round(v.x,3))

        print('Obj: %g' % self.m.objVal)
        return wid

Band = Bandwidth_allocation(pcome)

Band.computeP()
Band.computeWidth()


