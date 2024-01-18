'''
对队列进行MDP建模，计算WITTLE INDEX值
'''
import numpy as np
import  math
queuenum = 8
STATE_MAX = 20

'初始化到达概率并避免过大'
pcome = np.random.rand((queuenum))/4
while sum(pcome)>=0.8:
    pcome = np.random.rand((queuenum))/4

'具体仿真用的到达概率和带宽'
pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
width = [0.0421244,0.172286,0.126154,0.0314724,0.213572,0.298355,0.0484515,0.0675847]

'该函数返回期望为0.3时发送次数为k的泊松分布概率'
def poission(k,expect=0.3):
    return expect**k/math.factorial(k)*math.e**(-expect)

'概率转移矩阵，P0为不发，P1为发'
P0 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
P1 = np.zeros((queuenum,STATE_MAX,STATE_MAX))
for q in range(queuenum):
    for i in range(STATE_MAX):
        for j in range(STATE_MAX):
            if j>=i and j!=STATE_MAX-1:
                P0[q][i][j] = poission(j-i,expect=pcome[q])##到达j-i个
            elif j == STATE_MAX-1:
                P0[q][i][j] = 1-sum(P0[q][i])
            if i == 0:
                P1[q][i][j] = poission(j - i,expect=pcome[q])
            if j>=i-1 and j!=STATE_MAX-1 and i !=0:
                P1[q][i][j] = poission(j-i+1,expect=pcome[q])
            elif j==STATE_MAX-1:
                P1[q][i][j] = 1 - sum(P1[q][i])

'奖励矩阵'
R = np.zeros((queuenum,STATE_MAX,2))
for q in range(queuenum):
    for s in range(STATE_MAX):
        R[q][s][0] = -s
        R[q][s][1] = -s
    R[q][STATE_MAX - 1][0] = min(-100, -10 / pcome[q])  ##200
    R[q][STATE_MAX - 1][1] = min(-100, -10 / pcome[q])
    #R[q][STATE_MAX-1][0] = -pcome[q]

'折扣因子β，价值矩阵与whittle'
beta = 0.96
V = np.random.rand(queuenum,STATE_MAX)
lam = []

'迭代价值函数得到whittle，并更新价值函数'
for q in range(queuenum):
    lam.append([])
    for s in range(STATE_MAX):
        lambd = 0
        for step in range(3000):
            lambd = R[q][s][1] + sum(P1[q][s][j] * V[q][j] for j in range(STATE_MAX)) - R[q][s][0] - sum(P0[q][s][j] * V[q][j] for j in range(STATE_MAX))
            for ss in range(STATE_MAX):
                    V[q][ss]=max(R[q][ss][1]+(width[q]-1)*lambd+beta*sum(P1[q][ss][j] * V[q][j] for j in range(STATE_MAX)),R[q][ss][0]+(width[q]-0)*lambd+beta*sum(P0[q][ss][j] * V[q][j]for j in range(STATE_MAX)))
        print("队列:{}  状态:{}  whittle index:{}".format(q,s,lambd))
        lam[q].append(lambd)

for q in range(queuenum):
    print('队列', q, '的whittle为：', lam[q])
print('----whittle index:')
print(lam)