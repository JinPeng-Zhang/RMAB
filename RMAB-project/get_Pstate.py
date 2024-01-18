import math
import numpy as np
queuenum = 8
STATE_MAX = 20
burst = [0,0,0,0,0,0,0,0]
width = [0,0,0,0,0,0,0,0]
pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
for i in range(queuenum):
    width[i] = pcome[i]/sum(pcome)
# print(width)
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

print(P0[3][18])
for q in range(queuenum):
    Ptran[q] = width[q]*P1[q] + (1 - width[q])*P0[q]

summ = 0
for q in range(queuenum):
    eigenvalues, eigenvectors = np.linalg.eig(Ptran[q].T)
    idx = np.argmax(eigenvalues.real)
    stationary_distribution = np.abs(eigenvectors[:, idx].real) / np.sum(np.abs(eigenvectors[:, idx].real))
    print('队列：', q)
    sum = 0
    for i in range(STATE_MAX):
        print(f"状态s={i}的出现概率为：{stationary_distribution[i]}")
        sum = sum + stationary_distribution[i]*i
    print('------------------------------------',sum)
    summ = summ + sum
print('ssdssdsdsd',summ)