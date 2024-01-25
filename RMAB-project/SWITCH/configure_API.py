import os

import time
from simulation_zip import queue_simulation

class CONFIGURE():
    def __init__(self,pool_size):
        self.DIR_EXP_POOL = "./EXP_POOL"
        self.registration_port = []
        #======端口重新注册时，抹除原有数据标志位===========================
        self.exp_erase = False
        #============通过append函数，储存端口的WITTLE矩阵地址==============
        self.port_wittle = []
        #============通过append函数，储存端口的经验收集池地址===============
        self.port_exp = []
        self.pool_size = pool_size
    def Experience_upload(self,PORT):
        '''
            经验数据使用字典类型：
            EXP = {"PORT":2,'LEN':1000,'q0':[[s a s']....[s,a',s']],....,'q7':[s a s']}
            该函数存在文件的打开关闭，多次调用后程序速率明显减慢
        '''
        port_index = self.registration_port.index(PORT)
        exp = self.port_exp[port_index]
        port = "PORT_"+str(exp['PORT'])
        lens = exp['LEN']
        DIR = self.DIR_EXP_POOL+'./'+port+'/'
        for q in range(8):
            _q = 'q{}'.format(q)
            tim = int(time.time()*1000)
            file = open(DIR+_q+'./'+'{}.txt'.format(tim),'w')
            for j in range(lens):
                 file.write("{} {} {}\n".format(exp[_q][j][0],exp[_q][j][1],exp[_q][j][2]))
            file.close()

            file = open(DIR+'q{}'.format(q)+'./'+'conf.txt','r')
            data = []
            line = file.readline()
            while line and line!='\n':
                data.append(line)
                line = file.readline()
            file.close()
            data.append("tim:{} len:{} \n".format(tim,lens))
            size,use = data[0].split(" ")[0:2]
            size = int(size.split(":")[-1])
            use = int(use.split(":")[-1])+lens
            while use>size:
                del_size = int(data[1].split(" ")[1].split(":")[-1])
                filename = DIR+_q+'./'+data[1].split(" ")[0].split(":")[-1]+'.txt'
                os.remove(filename)
                use = use - del_size
                data.pop(1)
            file =open(DIR+_q+'./'+'conf.txt','w')
            file.write("size:{} use:{} q{}\n".format(self.pool_size,use,q))
            for d in data[1:]:
                file.write(d)
        # conf = open(DIR+"conf.txt",'r')
        # size = int(conf.readline().split("\n")[0])
        # conf.close()
        # for i in range(8):
        #     q = 'q{}'.format(i)
        #     file = open(DIR+q+'.txt','r')
        #     data = []
        #
        #     '''
        #     获取现有旧数据量，计算应该读取旧数据长度
        #     '''
        #     line = file.readline()
        #     ll = int(line.split("\n")[0])
        #
        #     line = file.readline()
        #     can_read = ll if (ll+lens)<=size else size-lens
        #     for i in range(can_read):
        #         data.append(line)
        #         line = file.readline()
        #     file = open(DIR+q+'.txt','w')
        #     file.write("{}\n".format(lens+can_read))
        #     for j in range(lens):
        #         file.write("{} {} {}\n".format(exp[q][j][0],exp[q][j][1],exp[q][j][2]))
        #     for dat in data:
        #         file.write(dat)
        #     file.close()
    def WITTLE_UPDATE(self,WT,port,q):
        port_index = self.registration_port.index(port)
        port_wt = self.port_wittle[port_index]
        # WT_row = np.size(WT, 0)  # 计算 WT 的行数
        # WT_col = np.size(WT, 1)  # 计算 WT 的列数
        # for row in range(WT_row):
        #     for col in range(WT_col):
        #         port_wt[row][col] = WT[row][col]
        vs = len(WT)
        for s in range(vs):
            port_wt[q][s] = WT[s]
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
            for q in range(8):
                os.mkdir(self.DIR_EXP_POOL + './' + s+'./'+'q{}'.format(q))
        #=========================不存在，则会创建txt,存在'w'会抹除原有数据========
        if self.exp_erase:
            for q in range(8):
                for Q_FILE in os.listdir(self.DIR_EXP_POOL + './' + s+'./'+'q{}'.format(q)):
                    os.remove(self.DIR_EXP_POOL + './' + s+'./'+'q{}'.format(q)+'./'+Q_FILE)
                file = open(self.DIR_EXP_POOL+'./'+s+'/'+"q{}".format(q)+'./'+'conf.txt','w')
                file.write("size:{} use:0 q{}\n".format(self.pool_size,q))
                file.close()
            #os.mknod(self.DIR_EXP_POOL+'./'+s+'/'+"q{}.txt".format(i))

    def registration(self,sim_queue:queue_simulation):
        self.Experience_create(sim_queue.port_index)
        if sim_queue.port_index not in self.registration_port:
            self.registration_port.append(sim_queue.port_index)
            self.port_wittle.append(sim_queue.WITTLE)
            self.port_exp.append(sim_queue.EXP_POOL)
        else:
            index = self.registration_port.index(sim_queue.port_index)
            self.port_wittle[index] = sim_queue.WITTLE
            self.port_exp[index]=sim_queue.EXP_POOL

# cof = CONFIGURE(pool_size=320000)
# cof.Experience_create(2)

