import  gurobipy as gp
from gurobipy import GRB
import  numpy as np
'初始化8个队列的到达概率'
queuenum = 8
pcome = np.random.rand((queuenum))/4
while sum(pcome)>=0.8:
    pcome = np.random.rand((queuenum))/4

pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653]
m = gp.Model("m/m/1")##载入线性规划模型
m.Params.MIPGap = 10**(-3)##最优解容忍误差范围

width = m.addMVar((queuenum), vtype = 'C',name="width",lb=0,ub=1)##队列总长度，上界下界为1和0
Ls = m.addMVar((queuenum), vtype = 'C',name="ls",lb=0)##排队长度，下界为0，不设置上界

for q in range(queuenum):
    m.addConstr(Ls[q]*(width[q]-pcome[q]) == pcome[q])##添加约束条件：出的等于进的，即保持流量平衡
for q in range(queuenum):
    m.addConstr(width[q]>=pcome[q])##添加约束条件：出队列的比进队列的多

m.addConstr(sum(width)==1)##添加约束条件：交换机分配的总带宽为1
m.setObjective(sum(Ls), GRB.MINIMIZE)##设置目标函数，最小化所有队列排队之和

m.Params.NonConvex = 2##设置变量为2，表示用非凸算法求解（因为存在非线性约束）
m.optimize()##求解

for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

# width[0] 0.267899 1.254
# width[1] 0.0749846 1.5311
# width[2] 0.125146 1.39
# width[3] 0.290538
# width[4] 0.021543
# width[5] 0.141766
# width[6] 0.0670508
# width[7] 0.0110734