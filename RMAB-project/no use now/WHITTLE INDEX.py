'''
Q-learning 论文例子
'''

import numpy as np

##R(S,A) (4,2)
R = [[-1,1],[0,0],[0,0],[1,-1]]
##P0 P1 (4,4)
P1 = [[0.5,0.5,0,0],[0,0.5,0.5,0],[0,0,0.5,0.5],[0,0,0,1]]
P0 = [[1,0,0,0],[0.5,0.5,0,0],[0,0.5,0.5,0],[0,0,0.5,0.5]]


V = np.random.rand(4)
beta = 0.99
#lambd = [ 0.2,1.6,-1,-1.6]
lambd = 0
#lambd = np.random.rand(4)
for p in range(4):
    for k in range(15000):
        lambd = R[p][1] + sum(P1[p][j] * V[j] for j in range(4)) - R[p][0] - sum(P0[p][j] * V[j] for j in range(4))
        for i in range(4):
                V[i]=max(R[i][1]-lambd+beta*sum(P1[i][j] * V[j] for j in range(4)),R[i][0]+beta*sum(P0[i][j] * V[j]for j in range(4)))

    print('第',p+1,'个状态的whittle index为：')
    print(lambd)
    print(V)
    print(R[p][1]-lambd+sum(P1[p][j] * V[j] for j in range(4)) , R[p][0]+sum(P0[p][j] * V[j] for j in range(4)))
#-0.5 0.5 1 -1
##[-0.5  0.5  1 -1]
#[tensor(2.9901), tensor(-0.6643), tensor(0.6645), tensor(-2.9901)]