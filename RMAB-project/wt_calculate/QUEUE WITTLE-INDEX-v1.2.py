'''
对队列进行MDP建模，计算WITTLE INDEX值，reward采用20%、60%梯度变换
'''
import numpy as np
import  math
queuenum = 8
STATE_MAX = 30
beta = 0.96

pcome = np.random.rand((queuenum))/4
while sum(pcome)>=0.8:
    pcome = np.random.rand((queuenum))/4

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
width = [0.0421244,0.172286,0.126154,0.0314724,0.213572,0.298355,0.0484515,0.0675858]
burst = [0,0,0,0,0,0,0,0]
decline_flag = 0

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
    R[q][0][0] = 0
    R[q][0][1] = 0
    for s in range(STATE_MAX-1):
        if s < 0.2*STATE_MAX:
            d = -1
        elif s < 0.6*STATE_MAX:
            d = -2
        else:
            d = -3
        R[q][s + 1][0] = R[q][s][0] + d
        R[q][s + 1][1] = R[q][s][1] + d

    R[q][STATE_MAX - 1][0] = -3000
    R[q][STATE_MAX - 1][1] = -3000
    #R[q][STATE_MAX - 1][1] = 300#min(-100,-10/pcome[q])
    #R[q][STATE_MAX-1][0] = -pcome[q]

V = np.random.rand(queuenum,STATE_MAX)
lam = []

re_not_eq = 0
# lam_nr=[]
# p1 = P1[5]
# p0 = P0[5]
# r = R[5]
v = np.random.rand(STATE_MAX)
for q in range(queuenum):
    lam.append([])
    # lam_nr.append([])
    for s in range(STATE_MAX):
        lambd = 0
        # lambd_nr = 0
        for step in range(3000):
            lambd = R[q][s][1] + sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)) - \
                    R[q][s][0] - sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))
            # lambd_nr = sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)) - \
            #         sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))
            for ss in range(STATE_MAX):
                    V[q][ss]=max(R[q][ss][1]-lambd+beta*sum(P1[q][ss][j] * V[q][j] for j in range(STATE_MAX)),
                                 R[q][ss][0]+beta*sum(P0[q][ss][j] * V[q][j] for j in range(STATE_MAX)))
        print("q:{} s:{} wt:{}".format(q,s,lambd))
        # print(lambd_nr)
        lam[q].append(lambd)
        # lam_nr[q].append(lambd_nr)

print('----whittle index:')
print(lam)
# print(lam_nr)

for q in range(queuenum):
    for i in range(STATE_MAX-1):
        if lam[q][i+1] < lam[q][i]:
            decline_flag = 1

print('是否非完全递增：',decline_flag)
# print(p0)
#
# for s in range(STATE_MAX):
#     lambd = 0
#     for step in range(7000):
#         lambd = r[s][1] + sum(p1[s][j] * v[j] for j in range(STATE_MAX)) - r[s][0] - sum(p0[s][j] * v[j] for j in range(STATE_MAX))
#         for ss in range(STATE_MAX):
#                 v[ss]=max(r[ss][1]-lambd+beta*sum(p1[ss][j] * v[j] for j in range(STATE_MAX)),
#                       r[ss][0]+beta*sum(p0[ss][j] * v[j]for j in range(STATE_MAX)))
#     print("s:{} wt:{}".format(s,lambd))
#     lam.append(lambd)
#
# # print(lam)
