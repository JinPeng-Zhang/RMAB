import numpy as np

from WITTLE_INDEX_CLASS import  MDP,W_fair_drop,wittle_index
from simulation_zip import queue_simulation
from configure_API import CONFIGURE
import time
pcome = [0.02534504,0.13369194,0.09386043,0.01754024,0.17004173,0.2459021,0.03012342,0.0451653 ]
bstart_tim = [100]
# 在线学习部分：
#     1.观察时间T,采集样本到MDP_MODEL的经验 POOL中
#     2.采集样本，并使用MDP_MODEL的exp_to_ptran计算PTRAN(转移概率矩阵)
#     3.创建数组R0 R1,对应动作0 1,循环状态空间vs,使用MDP_MODEL的函数s_to_u_qlen将状态空间映射的公平性参数u和队列长度qlen
#     4.根据公平性参数u和队列长度qlen，使用REWARD_MODEL的Wreward函数计算出RO R1
#     5.得到RO R1 PTRAN(转移概率矩阵)后，调用WITTLE_MODEL计算出WITTLE值
#     6.周期性▲t(建议5min)循环步骤2-5
#===============模块对象创建=======================
configure = CONFIGURE()
MDP_MODEL =  MDP(20,320000)
r = W_fair_drop(wf=0.2)
MDP_MODEL.Reward_matrix(r)#提前算出奖励矩阵

REWARD_MODEL = W_fair_drop(wf=0.2)
WITTLE_MODEL = wittle_index(21*21)
#==============端口模拟创建========================
simulation  = queue_simulation("MAX_QUEUE_LEN","FULL_DROP",pcome,burst=bstart_tim,burst_version='v1')
#==============端口注册，分配对应经验池=============
configure.registration(simulation)

#==============运行设置，时间、逻辑================
total_time = 100010
wittle_update_cycle = 100000
start = time.time()
for tim in range(total_time):
    print(tim)
    simulation.run(tim)
    if simulation.UP_LOAD== True:
        configure.Experience_upload(simulation.port_index)
        simulation.EXP_Clear()
    if tim !=0 and tim%wittle_update_cycle==0:
        for q in range(simulation.priority):
            MDP_MODEL.file_exp_to_ptran(simulation.port_index,q)
            WITTLE_MODEL.calculate_WITTLE(R1=MDP_MODEL.R[1],R0=MDP_MODEL.R[0],ptran=MDP_MODEL.ptran)
            configure.WITTLE_UPDATE(WITTLE_MODEL.WI,simulation.port_index,q)
            print(simulation.WITTLE[q])
        #print(simulation.WITTLE)
end = time.time()
print("simulation_times:{}s".format(end-start))
# MDP_MODEL.file_exp_to_ptran(simulation.port_index,q=1)
# print(MDP_MODEL.ptran[1][1],MDP_MODEL.ptran_len[1][1])
#
# print(simulation.EXP_POOL)