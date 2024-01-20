import os
import numpy as np
from simulation_zip import queue_simulation
#https://www.zhihu.com/question/584809823指针操作
class CONFIGURE():
    def __init__(self):
        self.DIR_EXP_POOL = "./EXP_POOL"
        self.registration_port = []
        self.port_wittle_addr = []

    '''
    经验数据使用字典类型：
    EXP = {"PORT":2,'LEN':1000,'q0':[[s a s']....[s,a',s']],....,'q7':[s a s']}
    '''
    def Experience_upload(self,exp:dict):
        port = "PORT_"+exp['PORT']
        len = exp['LEN']
        DIR = self.DIR_EXP_POOL+'./'+port+'/'

        conf = open("DIR"+"conf.txt",'r')
        size = int(conf.readline().split("\n")[0])
        conf.close()
        for i in range(8):
            q = 'q{}'.format(i)
            file = open(DIR+q+'.txt','r')
            data = []
            l = 0
            line = file.readline()
            while line or l<=size-len:
                data.append(line)
                l = l + 1
                line = file.readline()
            file = open(DIR+"q{}.txt".format(i),'w')
            for j in range(len):
                file.write("{} {} {}".format(exp[q][j][0],exp[q][j][1],exp[q][j][2]))
            for dat in data:
                file.write(dat)
            file.close()
    def WITTLE_UPDATE(self,WT,port):
        port_index = self.registration_port.index(port)
        wittle_addr = self.port_wittle_addr[port_index]
        WT_row = np.size(WT, 0)  # 计算 WT 的行数
        WT_col = np.size(WT, 1)  # 计算 WT 的列数
        for row in range(WT_row):
            for col in range(WT_col):
                np.ctypeslib.as_array(wittle_addr, shape=(row,col))[row][col] = WT[row][col]
    '''
    检查端口经验池文件是否存在
    若存在，则抹除原有数据；若不存在，则创建经验池
    '''
    def Experience_create(self,port):
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
        for i in range(8):
            open(self.DIR_EXP_POOL+'./'+s+'/'+"q{}.txt".format(i),'w')
        file = open(self.DIR_EXP_POOL + './' + s + '/' + "conf.txt", 'w')
        file.write("320000")
        file.close()
            #os.mknod(self.DIR_EXP_POOL+'./'+s+'/'+"q{}.txt".format(i))

    def registration(self,port,sim_queue:queue_simulation):
        self.Experience_create(port)
        if port not in self.registration_port:
            self.registration_port.append(port)
            self.port_wittle_addr.append(sim_queue.WITTLE.ctypes.data)

cof = CONFIGURE()
cof.Experience_create(2)

