import json
from Simulation_parameter import sim_dict
from WITTLE_INDEX_CLASS import  MDP,W_fair_drop,wittle_index
from simulation_zip import queue_simulation
from configure_API import CONFIGURE
import time

# 在线学习部分：
#     1.观察时间T,采集样本到MDP_MODEL的经验 POOL中
#     2.采集样本，并使用MDP_MODEL的exp_to_ptran计算PTRAN(转移概率矩阵)
#     3.创建数组R0 R1,对应动作0 1,循环状态空间vs,使用MDP_MODEL的函数s_to_u_qlen将状态空间映射的公平性参数u和队列长度qlen
#     4.根据公平性参数u和队列长度qlen，使用REWARD_MODEL的Wreward函数计算出RO R1
#     5.得到RO R1 PTRAN(转移概率矩阵)后，调用WITTLE_MODEL计算出WITTLE值
#     6.周期性▲t(建议5min)循环步骤2-5

#===========自定义数据=========================
with open("simulation.json", encoding="utf-8") as f:
    simulation_parameter = json.load(f)
pcome = simulation_parameter['pcome']
bstart_tim = simulation_parameter['bstart_tim']
queue_size= simulation_parameter['queue_size']
u_unit = simulation_parameter['u_unit']
fair = 1+1/u_unit
pool_size = simulation_parameter['pool_size']
total_time = simulation_parameter['total_time']
wittle_update_cycle = simulation_parameter['wittle_update_cycle']
Scheduling_algorithm = simulation_parameter['Scheduling_algorithm']
Congestion_handling = simulation_parameter['Congestion_handling']
burst_version = simulation_parameter['burst_version']
wf = simulation_parameter['wf']
#===============模块对象创建=======================
configure = CONFIGURE(pool_size=pool_size)
MDP_MODEL = MDP(queue_size,u_unit)
REWARD_MODEL = W_fair_drop(wf=wf,queue_size=queue_size,u_unit=u_unit)
MDP_MODEL.Reward_matrix(REWARD_MODEL)#提前算出奖励矩阵

WITTLE_MODEL = wittle_index((queue_size+1)*fair)
#==============端口模拟创建========================
simulation  = queue_simulation(queue_size,Scheduling_algorithm,Congestion_handling,pcome,burst=bstart_tim,burst_version=burst_version)
#==============端口注册，分配对应经验池=============
configure.registration(simulation)


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