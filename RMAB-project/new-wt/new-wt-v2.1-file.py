'''
r=-e*s+min(1,∑λ)*λ',r[last]=-(smax*weight)*λ
'''
import numpy as np
import math
queuenum = 8
STATE_MAX = 24
beta = 0.2
d1 = 25000
d2 = 1000
'lam维的起始位置与间距'
lambda_min = 0.01
lambda_gap = 0.01
M = 70  ##来包率范围为lambda_min+1*lambda_gap~(M+1)*1*lambda_gap = 0.01~0.71

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021+0.45,0.03012342,0.0451653]
burst = [0,0,0,0,0,0,0,0]

def poission(k, expect=0.3, pburst=0):
    if pburst == 0 or k < 3:
        return (1-pburst)*expect**k/math.factorial(k)*math.e**(-expect)
    else:
        return pburst*(expect**(k-3)/math.factorial(k-3)*math.e**(-expect)) + \
               (1-pburst)*(expect**k/math.factorial(k)*math.e**(-expect))

'先计算不同lambda下的来包概率P(come,lambda_n)，分别表示在来包率为lambda_n来come个包的概率'
P_come = np.zeros((STATE_MAX+1,M+1))
for i in range(STATE_MAX+1):
    for j in range(M+1):
        P_come[i][j] = poission(i, expect=lambda_min+j*lambda_gap, pburst=burst[0])
# print(P_come[2])

'从P_come为基础构造P0和P1，P0为只关注来包过程，P1则是将其状态-1再关注来包'
P0 = np.zeros((M+1,STATE_MAX+1,STATE_MAX+1))
P1 = np.zeros((M+1,STATE_MAX+1,STATE_MAX+1))
for m in range(M + 1):
    for i in range(STATE_MAX+1):
        for j in range(STATE_MAX+1):
            if j>=i and j!=STATE_MAX:
                P0[m][i][j] = P_come[j-i][m]
            elif j == STATE_MAX:
                P0[m][i][j] = 1 - sum(P0[m][i])
for m in range(M + 1):
    for i in range(STATE_MAX + 1):
        for j in range(STATE_MAX + 1):
            if i == 0 and j == 0:
                P1[m][i][j] = P_come[j-i+1][m] + P_come[j-i][m]
            if j>=i-1 and j!=STATE_MAX:
                P1[m][i][j] = P_come[j-i+1][m]
            elif j==STATE_MAX:
                P1[m][i][j] = 1 - sum(P1[m][i])
# print(P0[109][23],P1[109][23])

'g函数，计算ls开始之后的泊松求和概率*e^lambda'
def g(lamb,ls):
    sum = math.e ** lamb
    for n in range(ls):
        sum = sum - (lamb**n)/math.factorial(n)
    return sum
#aa = g(0.5,0)
#print(aa,math.e**0.5)
'构造{reward}，为(M+1)*(S+1)*2维'
def getR(STATE_MAX, lambda_min, lambda_gap, M):
    R = np.zeros((M+1,STATE_MAX+1,2))
    for m in range(M+1):
        mlambda = lambda_min + m * lambda_gap
        for s in range(STATE_MAX+1):
            ls = STATE_MAX - s + 1
            R[m][s][0] = -(math.e ** (-mlambda))*(d1*g(mlambda,ls) + mlambda*d2*g(mlambda,ls-1) + d2*(1-ls)*g(mlambda,ls))
        R[m][0][1] = R[m][0][0]
        for s in range(STATE_MAX):
            ss = s + 1
            R[m][ss][1] = R[m][ss-1][0]
    # print(R[109])
    return R


V = np.random.rand(M+1,STATE_MAX+1)
v = np.random.rand(STATE_MAX+1)


lam = []
R = getR(STATE_MAX, lambda_min, lambda_gap, M)
file_path = '/home/test/Desktop/RMAB/data/new-wt/' + 'beta=' + str(beta) + '/' + 'd=' + str(d1) + '-' + str(d2) + '.txt'
for m in range(M+1):
    lam.append([])
    # m=39
    for s in range(STATE_MAX+1):
        lambd = 0
        for step in range(3000):
            lambd = R[m][s][1] + sum(P1[m][s][j] * V[m][j] for j in range(STATE_MAX+1)) - \
                    R[m][s][0] - sum(P0[m][s][j] * V[m][j] for j in range(STATE_MAX+1))
            for ss in range(STATE_MAX+1):
                    V[m][ss]=max(R[m][ss][1]-lambd+beta*sum(P1[m][ss][j] * V[m][j] for j in range(STATE_MAX+1)),
                                R[m][ss][0]+beta*sum(P0[m][ss][j] * V[m][j] for j in range(STATE_MAX+1)))
        print("mlambda:{} s:{} wt:{}".format(lambda_min+m*lambda_gap,s,lambd))
        lam[m].append(lambd)
print('----whittle index:')
print(lam)
with open(file_path, 'w') as file:
        file.write(str(lam))


