'''
ppt1,根据转移概率计算时延RTT均值，同Bandwidth allocation.py
'''
import  math
import  torch
import  matplotlib.pyplot as plt
QUEUE_NUM = 3
STATE_MAX = 10

width = 0.6 ##带宽占比
def poission(k,expect=0.3):##到达速率期望为0.3
    return expect**k/math.factorial(k)*math.e**(-expect)
P0 = torch.zeros((STATE_MAX,STATE_MAX))
P1 = torch.zeros((STATE_MAX,STATE_MAX))##转移概率

for i in range(STATE_MAX):##表示状态转移
    for j in range(STATE_MAX):
        if j>=i and j!=STATE_MAX-1:
            P0[i][j] = poission(j-i)
        elif j == STATE_MAX-1:
            P0[i][j] = 1-torch.sum(P0[i])
        if i == 0:
            P1[i][j] = poission(j - i)
        if j>=i-1 and j!=STATE_MAX-1 and i !=0:
            P1[i][j] = poission(j-i+1)
        elif j==STATE_MAX-1:
            P1[i][j] = 1 - torch.sum(P1[i])

P = width*P1+(1-width)*P0##合并转移矩阵
print(P)
ps = torch.zeros((STATE_MAX))#状态概率与计算
for i in range(STATE_MAX):
    ps[i] = 0.1
for i in range(500):
    for s in range(STATE_MAX):
        ps[s] = sum(ps[j]*P[j][s] for j in range(10))
SU = 0##平均队列长度
for i in range(STATE_MAX):
    SU = SU + ps[i]*i

print(SU)
# P1 = send_rate*P1+(1-send_rate)*P0
'''
print(P0,P1)

R = torch.zeros((STATE_MAX,2))

for i in range(STATE_MAX):
    for k in range(2):
        R[i][k] = -i/10
        # if k==1:
        #     R[i][1] = i**2
        # else:
        #     R[i][0] = - i**2

beta = 0.99


lamb = []


for s in range(STATE_MAX):
    lambd = 0
    v = torch.zeros((STATE_MAX))
    #while R[s][1] -lambd+ sum(P1[s][j] * v[j] for j in range(10)) - R[s][0] - sum(P0[s][j] * v[j] for j in range(10))>0.000001:
    for t in range(5000):
        lambd = R[s][1] + sum(P1[s][j] * v[j] for j in range(STATE_MAX)) - R[s][0] - sum(
            P0[s][j] * v[j] for j in range(STATE_MAX))
        for i in range(STATE_MAX):
            v[i] = max(R[i][1] - lambd + beta * sum(P1[i][j] * v[j] for j in range(STATE_MAX)),
                       R[i][0] + beta * sum(P0[i][j] * v[j] for j in range(STATE_MAX)))

        # print("learning {} {} {}".format(q,s,step))
    print(v)
    print("s:{}".format(s))
    print(R[s][1] -lambd+ sum(P1[s][j] * v[j] for j in range(STATE_MAX)),R[s][0] + sum(P0[s][j] * v[j] for j in range(STATE_MAX)))

    lamb.append(lambd)

print(lamb)
plt.plot(lamb,"*")
plt.show()
'''

# tensor([1.0948e-05, 3.8301e-05, 1.2797e-04, 4.2722e-04, 1.4263e-03, 4.7617e-03,
#         1.5897e-02, 5.3071e-02, 1.7718e-01, 5.9151e-01])
