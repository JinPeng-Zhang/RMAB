'''
目标为E[T]-eE[Q],re=-P(q,s)*s
'''
import numpy as np
import math
queuenum = 8
STATE_MAX = 20
beta = 0.4

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
width = [0,0,0,0,0,0,0,0]
burst = [0,0,0,0,0,0,0,0]
decline_flag = 0
for i in range(queuenum):
    width[i] = pcome[i]/sum(pcome)

def poission(k,expect=0.3,pburst=0):
    if pburst==0 or k<3:
        return (1-pburst)*expect**k/math.factorial(k)*math.e**(-expect)
    else:
        return pburst*(expect**(k-3)/math.factorial(k-3)*math.e**(-expect)) + \
               (1-pburst)*(expect**k/math.factorial(k)*math.e**(-expect))

P0 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P1 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
Ptran = np.zeros((queuenum,STATE_MAX,STATE_MAX))
Ps = np.zeros((queuenum,STATE_MAX))

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

for q in range(queuenum):
    Ptran[q] = width[q]*P1[q] + (1 - width[q])*P0[q]
for q in range(queuenum):
    eigenvalues, eigenvectors = np.linalg.eig(Ptran[q].T)
    idx = np.argmax(eigenvalues.real)
    Ps[q] = np.abs(eigenvectors[:, idx].real) / np.sum(np.abs(eigenvectors[:, idx].real))

print(P0[2])

R = np.zeros((queuenum,STATE_MAX,2))
for q in range(queuenum):
    R[q][0][0] = 0
    R[q][0][1] = 0
    for s in range(STATE_MAX):
        R[q][s][0] = -s * Ps[q][s]
        R[q][s][1] = -s * Ps[q][s]
    R[q][STATE_MAX - 1][0] = -pcome[q] / 0.001
    R[q][STATE_MAX - 1][1] = -pcome[q] / 0.001
#print(R)
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
# print(lam_nr)

for q in range(queuenum):
    for i in range(STATE_MAX-1):
        if lam[q][i+1] < lam[q][i]:
            decline_flag = 1

print('是否非完全递增：',decline_flag)