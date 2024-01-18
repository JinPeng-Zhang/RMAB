'''
从考虑赋予REWARD权值的角度使得控制带宽
到达速率为二值分布，计算WITTLE INDEX
'''
import torch

#####param

QUEUE_NUM = 3
STATE_MAX = 10#每个队列的最大状态数，队列数据包容量

###MDP model
###reward,Q(s,a)
####八个优先级队列 RMAB
##下个时刻数据包到来的概率服从二项分布 pcome = 0.3
pcome = 0.3
P0 =  torch.zeros((10,10))##action == 0
P1 =  torch.zeros((10,10))##action == 1
for i in range(STATE_MAX):
    for j in range(STATE_MAX):
        if i == j and i != STATE_MAX-1:
            P0[i][j] = 1-pcome
        elif i == j and i== STATE_MAX-1:
            P0[i][j] = 1
        elif i == j-1:
            P0[i][j] = pcome

        if i == j and i != 0:
            P1[i][j] = pcome
        elif i == j and i== 0:
            P1[i][j] = 1
        elif i == j+1:
            P1[i][j] = 1-pcome

print(P0,P1)
width = [0.4,0.3,0.3]
R = torch.zeros((3,10,2))##奖励(包数*权重的负值，越大越好)
for q in range(QUEUE_NUM):
    for i in range(STATE_MAX):
        for k in range(2):
            R[q][i][k] = -width[q]*(i+1)

print(R)
beta = 0.99
lam = []
for q in range(QUEUE_NUM-2):
    lamb = []
    for s in range(STATE_MAX):
        lambd = 0
        v = torch.zeros((STATE_MAX))
        for l in range(5000):
            lambd = R[q][s][1] + sum(P1[s][j] * v[j] for j in range(10)) - R[q][s][0] - sum(P0[s][j] * v[j] for j in range(10))
            for i in range(STATE_MAX):
                v[i] = max(R[q][i][1] - lambd + beta * sum(P1[i][j] * v[j] for j in range(10)),
                           R[q][i][0] + beta * sum(P0[i][j] * v[j] for j in range(10)))
            # print("learning {} {} {}".format(q,s,step))
        lamb.append(lambd)
        print(v,lambd)
        print("s:{}".format(s))
        print(R[q][s][1]-lambd + sum(P1[s][j] * v[j] for j in range(10)) , R[q][s][0] + sum(P0[s][j] * v[j] for j in range(10)))
    lam.append(lamb)
    print(lamb)
print(lam)

####result
