'''
未来视野,视野长度为derta
'''
import numpy as np
import math
queuenum = 8
STATE_MAX = 25
detra = 3
beta = 1

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
P00 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P10 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P000 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P100 = np.zeros((queuenum,STATE_MAX,STATE_MAX))

for q in range(queuenum):
    for i in range(STATE_MAX):
        for j in range(STATE_MAX):
            if j>=i and j!=STATE_MAX-1:
                P0[q][i][j] = poission(j-i,expect=pcome[q],pburst=burst[q])
                P00[q][i][j] = poission(j - i, expect=(pcome[q]*2), pburst=burst[q])
                P000[q][i][j] = poission(j - i, expect=(pcome[q]*3), pburst=burst[q])
            elif j == STATE_MAX-1:
                P0[q][i][j] = 1 - sum(P0[q][i])
                P00[q][i][j] = 1 - sum(P00[q][i])
                P000[q][i][j] = 1 - sum(P000[q][i])
            if i == 0:
                P1[q][i][j] = poission(j - i,expect=pcome[q],pburst=burst[q])
                P10[q][i][j] = poission(j - i, expect=(pcome[q]*2), pburst=burst[q])
                P100[q][i][j] = poission(j - i, expect=(pcome[q]*3), pburst=burst[q])
            if j>=i-1 and j!=STATE_MAX-1 and i !=0:
                P1[q][i][j] = poission(j-i+1,expect=pcome[q],pburst=burst[q])
                P10[q][i][j] = poission(j - i + 1, expect=(pcome[q]*2), pburst=burst[q])
                P100[q][i][j] = poission(j - i + 1, expect=(pcome[q]*3), pburst=burst[q])
            elif j==STATE_MAX-1:
                P1[q][i][j] = 1 - sum(P1[q][i])
                P10[q][i][j] = 1 - sum(P10[q][i])
                P100[q][i][j] = 1 - sum(P100[q][i])

#print(P0[0][5])
#print(P1[0][5])
k1 = 0.9
k2 = 0.09
k3 = 0.01
print(P1[5][17])
P0[5] = k1*P0[5] + k2*P00[5] + k3*P000[5]
P1[5] = k1*P1[5] + k2*P10[5] + k3*P100[5]
print(P1[5][17])

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

    R[q][STATE_MAX - 1][0] = -(1 - P0[q][0][0])/0.0001
    R[q][STATE_MAX - 1][1] = -(1 - P1[q][0][0]) / 0.0001
print(R[4])
print(R[5])

V = np.random.rand(queuenum,STATE_MAX)
lam = []

re_not_eq = 0
v = np.random.rand(STATE_MAX)
for q in range(1):
    lam.append([])
    for s in range(STATE_MAX):
        lambd = 0
        for step in range(10000):
            lambd = R[q][s][1] + sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)) - \
                    R[q][s][0] - sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))
            for ss in range(STATE_MAX):
                    V[q][ss]=max(R[q][ss][1]-lambd+beta*sum(P1[q][ss][j] * V[q][j] for j in range(STATE_MAX)),
                                 R[q][ss][0]+beta*sum(P0[q][ss][j] * V[q][j] for j in range(STATE_MAX)))
        #print(V[q])#
        print("q:{} s:{} wt:{},V1{},V0{}".format(q,s,lambd,R[q][s][1]-lambd+sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)), R[q][s][0]+sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))))
        lam[q].append(lambd)
# [-2.55069871e-02 -1.02550699e+00 -2.53188304e+00 -4.28821846e+00
#  -6.16794118e+00 -8.10873204e+00 -1.10922571e+01 -1.45905007e+01
#  -1.83428218e+01 -2.22205615e+01 -2.61602109e+01 -3.01304204e+01
#  -3.41157151e+01 -3.81084563e+01 -4.21048745e+01 -4.61032691e+01
#  -5.11152287e+01 -5.66275083e+01 -6.23867579e+01 -6.82679177e+01
#  -7.42092553e+01 -8.01803000e+01 -8.61662808e+01 -9.21911796e+01
#  -2.98948307e+02]
# q:0 s:0 wt:0.0,V1-0.02550698710442087,V0-0.02550698710442087
# [-5.06900829e-02 -2.05069016e+00 -4.05069240e+00 -6.05075574e+00
#  -8.05254913e+00 -1.01013802e+01 -1.41013802e+01 -1.81013802e+01
#  -2.21013802e+01 -2.61013802e+01 -3.01013802e+01 -3.41013802e+01
#  -3.81013802e+01 -4.21013803e+01 -4.61013818e+01 -5.01015451e+01
#  -5.51143779e+01 -6.06270885e+01 -6.63865508e+01 -7.22678156e+01
#  -7.82092051e+01 -8.41802753e+01 -9.01662688e+01 -9.61911738e+01
#  -3.02948305e+02]
# q:0 s:1 wt:2.0000001576005233,V1-3.0506902404818765,V0-2.0506901616816147
# [-5.06900829e-02 -2.05069016e+00 -4.05069240e+00 -6.05075574e+00
#  -8.05254913e+00 -1.01013802e+01 -1.41013802e+01 -1.81013802e+01
#  -2.21013802e+01 -2.61013802e+01 -3.01013802e+01 -3.41013802e+01
#  -3.81013802e+01 -4.21013830e+01 -4.61013875e+01 -5.01015523e+01
#  -5.51143858e+01 -6.06270968e+01 -6.63865592e+01 -7.22678241e+01
#  -7.82092137e+01 -8.41802839e+01 -9.01662774e+01 -9.61911824e+01
#  -3.02948313e+02]
print('----whittle index:')
print(lam)

# print(lam_nr)

for q in range(queuenum):
    for i in range(STATE_MAX-1):
        if lam[q][i+1] < lam[q][i]:
            decline_flag = 1

print('是否非完全递增：',decline_flag)