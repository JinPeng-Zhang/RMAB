在此对各个py文件的内容和功能进行阐释：
1.Qlearning.py：论文I（Qlearning）的实验（老师辅导学生）
2.WHITTLE INDEX.py：论文I（Qlearning）中例子的whittle值求取（一共四个状态的那个）
3.mm1.py：使用Gurobi求解器对线性规划问题进行求解（要先转化为LP问题）
4.Queue_WIDTH.py：给定带宽，计算平均队列长度
5.Queue scheduling.py：定义奖励和转移矩阵，计算各个队列的whittle值，先不看
6.queue simulation.py：
7.QUEUE WHITTLE INDEX.py：对队列进行MDP建模，计算whittle值
8.Bandwidth allocation.py：有问题
9.Bandwidth allocation2.py：有问题

实际使用的文件：
1.QUEUE WHITTLE INDEX.py：计算whittle
2.whittle simulation.py：通过whittle模拟过程得到reward曲线
3.priority simulation.py：优先级调度

1-v1.2：三段式reward，节点为20%，60%
1-v1.3：五段式reward，节点为20%，40%，60%，80%
1-v2.1：reward=(s^2+s)/2
1-v3.1：加入动作，R[s][1]=R[s-1][0]

2-v1：初版，无用
2-v2.1：忘了
2-v2.2：现在使用的无问题的whittle仿真