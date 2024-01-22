import os
import numpy as np
from simulation_zip import queue_simulation
#https://www.zhihu.com/question/584809823指针操作
class CONFIGURE():
    def __init__(self):
        self.DIR_EXP_POOL = "./EXP_POOL"
        self.registration_port = []
        #======端口重新注册时，抹除原有数据标志位===========================
        self.exp_erase = False
        #============通过append函数，储存端口的WITTLE矩阵地址==============
        self.port_wittle = []
        #============通过append函数，储存端口的经验收集池地址===============
        self.port_exp = []
    def Experience_upload(self,PORT):
        '''
            经验数据使用字典类型：
            EXP = {"PORT":2,'LEN':1000,'q0':[[s a s']....[s,a',s']],....,'q7':[s a s']}
        '''
        port_index = self.registration_port.index(PORT)
        exp = self.port_exp[port_index]
        port = "PORT_"+str(exp['PORT'])
        lens = exp['LEN']
        DIR = self.DIR_EXP_POOL+'./'+port+'/'

        conf = open(DIR+"conf.txt",'r')
        size = int(conf.readline().split("\n")[0])
        conf.close()
        for i in range(8):
            q = 'q{}'.format(i)
            file = open(DIR+q+'.txt','r')
            data = []


            line = file.readline()
            ll = int(line.split("\n")[0])

            line = file.readline()
            can_read = ll if (ll+lens)<=size else size-lens
            for i in range(can_read):
                data.append(line)
                line = file.readline()
            file = open(DIR+q+'.txt','w')
            file.write("{}\n".format(lens+can_read))
            for j in range(lens):
                file.write("{} {} {}\n".format(exp[q][j][0],exp[q][j][1],exp[q][j][2]))
            for dat in data:
                file.write(dat)
            file.close()
    def WITTLE_UPDATE(self,WT,port):
        port_index = self.registration_port.index(port)
        port_wt = self.port_wittle[port_index]
        WT_row = np.size(WT, 0)  # 计算 WT 的行数
        WT_col = np.size(WT, 1)  # 计算 WT 的列数
        for row in range(WT_row):
            for col in range(WT_col):
                port_wt[row][col] = WT[row][col]
    def Experience_create(self,port):
        '''
           检查端口经验池文件是否存在
           若存在，则抹除原有数据；若不存在，则创建经验池
        '''
        s = "PORT_"+str(port)
        #print(os.listdir(self.DIR_EXP_POOL))
        exists = False
        for PORT_FILE in os.listdir(self.DIR_EXP_POOL):
            if s == PORT_FILE:
                print("PORT{} experience pool already exists".format(port))
                exists = True
        if not exists:
            os.mkdir(self.DIR_EXP_POOL+'./'+s)
            print("PORT{} experience pool create success".format(port))
        #=========================不存在，则会创建txt,存在'w'会抹除原有数据========
        if self.exp_erase or not exists:
            for i in range(8):
                open(self.DIR_EXP_POOL+'./'+s+'/'+"q{}.txt".format(i),'w')
            file = open(self.DIR_EXP_POOL + './' + s + '/' + "conf.txt", 'w')
            file.write("320000")
            file.close()
            #os.mknod(self.DIR_EXP_POOL+'./'+s+'/'+"q{}.txt".format(i))

    def registration(self,sim_queue:queue_simulation):
        self.Experience_create(sim_queue.port_index)
        if sim_queue.port_index not in self.registration_port:
            self.registration_port.append(sim_queue.port_index)
            self.port_wittle.append(sim_queue.WITTLE)
            self.port_exp.append(sim_queue.EXP_POOL)

# cof = CONFIGURE()
# cof.Experience_create(2)

