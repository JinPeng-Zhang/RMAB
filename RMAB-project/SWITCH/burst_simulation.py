import  numpy as np
class burst_json_create():
    def __init__(self):
        '''
           突发设计，实际情况会有一些出入
           [start_time,end_time)
           v1:busrt = [time1,time2,...,timen]固定模式
           v2:busrt = {'len':n,'b':[[start_time,end_time,q1_index,q2_index,.....,qk_index],...,[]]}，自定义起始时间和队列，平均突发
           v3:busrt = {'len':n,'b':[{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate},...,{}]},自定义起始时间和队列，自定义队列突发速率
           v4:busrt = {'len':n,'b':[{'type':'v3','data':{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate}},{'type':'v2','data':[start_time,end_time,q1_index,q2_index,.....,qk_index]},{'type':'v1','data':200}]}v1,v2.v3混合模式
       '''
    def burst_v1(self,total_time,proportion,offset):
        '''
        固定突发模式
        '''
        burst = [offset]
        nums = round(total_time*4*proportion/(100*6))
        if nums==0:
            return []
        e = total_time/nums
        time = np.random.exponential(scale=e, size=2*nums).astype(int)
        for i in range(2*nums):
            if time[i]+burst[-1]>total_time+offset:
                break
            elif time[i]<100:
                continue
            else:
                burst.append(time[i]+burst[-1])
        burst.pop(0)
        return burst
    def burst_v2(self,total_time,proportion,offset):
        '''
        虽然自定义时间，但是最好小于100ms,除了带宽需求外，还需满足突发时间T*1.5/突发队列数<20
        该模式下，突发带宽不变，因此突发时间之和与v1一致
        busrt = {'len':n,'b':[[start_time,end_time,q1_index,q2_index,.....,qk_index],...,[]]}
        '''
        burst = {'len':0,'b':[]}
        btimes =round(np.random.uniform(0.8,1.2)*total_time*4*proportion/(6))
        tim = offset
        while tim<total_time+offset:
            q_index = np.random.randint(0,7,size=np.random.randint(1,8))
            ##去除重复数据
            q_index =list(set(q_index))
            bt_max = int(20*len(q_index)/1.5)
            bt = np.random.randint(bt_max*0.6,bt_max)
            t2_t1 = round(1.5*bt/proportion)
            start_time = np.random.randint(tim + 1, tim + t2_t1 - bt - 1)
            burst['len'] = burst['len'] + 1
            q_index.insert(0,start_time+bt)
            q_index.insert(0,start_time)
            burst['b'].append(q_index)
            tim = tim+t2_t1
        return burst
    def burst_v3(self,total_time,proportion,offset):
        '''
        自定义时间和突发速率，除了带宽需求外，需要满足（end_time-start_time）*add_rate<20
        起事时间T1,先随机8各队列的add_rate，范围为[0,1],再根据最大的add_rate计算出（end_time-start_time）上限，后随机生成(end_time-start_time）,然后根据proportion计算出前后范围时间差[T1,T2]，在区间(T1,T2-(end_time-start_time）)内生成start
        busrt = {'len':n,'b':[{'start_time':100,'end_time':150,'q1':add_rate,'q2':add_rate,.....,'q2':add_rate},...,{}]}
        '''
        tim = offset
        busrt = {'len': 0, 'b': []}
        while tim<offset+total_time:
            add_rate = np.random.rand(8)
            #计算出（end_time-start_time）上限
            max_add_rate = max(add_rate)
            et_st_max = int(20/max_add_rate)
            #随机生成(end_time-start_time）
            rand = np.random.uniform(0.6,1)
            et_st = int(et_st_max*rand)
            #根据proportion计算出前后范围时间差[T1,T2]
            t2_t1 = round(sum(add_rate)*et_st/proportion)
            #在区间[T1,T2-(end_time-start_time）]内生成start
            start_time = np.random.randint(tim+1,tim+t2_t1-et_st-1)
            busrt['len'] = busrt['len'] + 1
            busrt['b'].append({'start_time':start_time,'end_time':start_time+et_st,'q0':add_rate[0],'q1': add_rate[1],'q2': add_rate[2],'q3': add_rate[3],'q4': add_rate[4],'q5': add_rate[5],'q6': add_rate[6],'q7': add_rate[7]})
            tim = tim+t2_t1
        return busrt
    def burst_v4(self,total_time,proportion,offset):
        '''
        将total_time分成多段，每一段一个突发模式v1,v2,v3,将该段的时间和带宽占比输入，调用对应
        读取返回的结构体，将各个时间段的多次突发读出来，修改时间基数，写入v4类型结构体
        v1 100000发生大约13次，1300ms,平均10000 130ms，暂时将时间分为10000ms一段
        v1 v2 v3 概率相同
        '''
        nums = int(total_time/10000)
        time = np.random.exponential(scale=10000, size=2 * nums).astype(int)
        v= np.random.rand(2* nums)#(0,1]之间的小数
        tim = offset
        burst = {'len': 0, 'b': []}
        for i in range(2*nums):
            version = round(v[i]*3+0.5)
            print(version)
            #时间段tim->tim+time[i]
            if tim+time[i]>=total_time+offset:
                time[i] = total_time+offset-tim
            if version==1:
                _burst = self.burst_v1(time[i],proportion,tim)
                print(tim,time[i],_burst)
                for b in _burst:
                    burst['len'] = burst['len'] +1
                    burst['b'].append({'type':'v1','data':b})
            elif version==2:
                _burst = self.burst_v2(time[i],proportion,tim)
                for b in _burst['b']:
                    burst['len'] = burst['len'] +1
                    burst['b'].append({'type':'v2','data':b})
            elif version==3:
                _burst = self.burst_v3(time[i],proportion,tim)
                for b in _burst['b']:
                    burst['len'] = burst['len'] + 1
                    burst['b'].append({'type':'v3','data':b})
            tim = tim+time[i]
            if tim == total_time+offset:
                break
        return burst


b = burst_json_create()
print(b.burst_v2(total_time=100000,proportion=0.02,offset=0))