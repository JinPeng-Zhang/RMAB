'''
r=-e*s+min(1,∑λ)*λ'
'''
import numpy as np
import math
queuenum = 8
STATE_MAX = 25
e = 0.04
beta = 0.4

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021+0.45,0.03012342,0.0451653]
width = [0.0421244,0.172286,0.126154,0.0314724,0.213572,0.298355,0.0484515,0.0675858]
burst = [0,0,0,0,0,0,0,0]

allpcome = sum(pcome)    #∑λ
pcomee = [0,0,0,0,0,0,0,0]  #λ'
for i in range(queuenum):
    pcomee[i]=pcome[i]/allpcome
# print(allpcome,pcomee,sum(pcomee))

def poission(k,expect=0.3,pburst=0):
    if pburst==0 or k<3:
        return (1-pburst)*expect**k/math.factorial(k)*math.e**(-expect)
    else:
        return pburst*(expect**(k-3)/math.factorial(k-3)*math.e**(-expect)) + \
               (1-pburst)*(expect**k/math.factorial(k)*math.e**(-expect))

P0 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P1 = np.zeros((queuenum,STATE_MAX,STATE_MAX))

for q in range(queuenum):
    for i in range(STATE_MAX):
        for j in range(STATE_MAX):
            if j>=i and j!=STATE_MAX-1:
                P0[q][i][j] = poission(j-i,expect=pcome[q],pburst=burst[q])
            elif j == STATE_MAX-1:
                P0[q][i][j] = 1-sum(P0[q][i])
            if i == 0:
                P1[q][i][j] = poission(j - i,expect=pcome[q],pburst=burst[q])
            if j>=i-1 and j!=STATE_MAX-1 and i !=0:
                P1[q][i][j] = poission(j-i+1,expect=pcome[q],pburst=burst[q])
            elif j==STATE_MAX-1:
                P1[q][i][j] = 1 - sum(P1[q][i])

R = np.zeros((queuenum,STATE_MAX,2))
for q in range(queuenum):
    for s in range(STATE_MAX-1):
        R[q][s][0] = -e*s + min(1,allpcome)*pcomee[q]
        R[q][s][1] = -e*s + min(1,allpcome)*pcomee[q]
    R[q][STATE_MAX - 1][0] = -2000
    R[q][STATE_MAX - 1][1] = -2000
# print(R)

V = np.random.rand(queuenum,STATE_MAX)
lam = []

re_not_eq = 0
v = np.random.rand(STATE_MAX)
for q in range(queuenum):
    lam.append([])
    for s in range(STATE_MAX):
        lambd = 0
        for step in range(3000):
            lambd = R[q][s][1] + sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)) - \
                    R[q][s][0] - sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))
            for ss in range(STATE_MAX):
                    V[q][ss]=max(R[q][ss][1]-lambd+beta*sum(P1[q][ss][j] * V[q][j] for j in range(STATE_MAX)),
                                 R[q][ss][0]+beta*sum(P0[q][ss][j] * V[q][j] for j in range(STATE_MAX)))
        print("q:{} s:{} wt:{}".format(q,s,lambd))
        lam[q].append(lambd)

print('----whittle index:')
print(lam)
