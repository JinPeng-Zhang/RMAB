from WITTLE_INDEX_CLASS import  MDP,W_fair_drop,wittle_index
from simulation_zip import queue_simulation
MDP_MODEL =  MDP(25,1000)
REWARD_MODEL = W_fair_drop(0.4,0.6)

# 在线学习部分：
#     1.观察时间T,采集样本到MDP_MODEL的经验 POOL中
#     2.采集样本，并使用MDP_MODEL的exp_to_ptran计算PTRAN(转移概率矩阵)
#     3.创建数组R0 R1,对应动作0 1,循环状态空间vs,使用MDP_MODEL的函数s_to_u_qlen将状态空间映射的公平性参数u和队列长度qlen
#     4.根据公平性参数u和队列长度qlen，使用REWARD_MODEL的Wreward函数计算出RO R1
#     5.得到RO R1 PTRAN(转移概率矩阵)后，调用WITTLE_MODEL计算出WITTLE值
#     6.周期性▲t(建议200ms)循环步骤2-5

WITTLE_MODEL = wittle_index(20*21)###u [0.05]


pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ]
bstart_tim = []
simulation  = queue_simulation("SP","FULL_DROP",pcome,bstart_tim)

total_time = 100
for tim in range(total_time):
    simulation.run(tim)