import random
'误码率与传输延时'
p1 = 0.01
p2 = 0.1
T1 = 1
T2 = 10
'数据包与窗口'
N = 500
w = 5
'初始化'
r1 = [0, 0, 0, 0, 0]  #1表示数据包成功收到，0表示误码
ack1 = [0, 0, 0, 0, 0]  #1表示收到ack，0表示没收到
t1 = 1  #回退N协议和选择重传协议的时间
win1 = [1, 2, 3, 4, 5]  #窗口起始位置
send1 = 5  #累计发送包数
'网络环境参数'
p_error = 0.1
T = T1

'回退N仿真'
max = 1000000
while win1[0] <= N:
    first_wrong = 0  # 第一个错的的窗口位置:1,2,3,4,5
    for i in range(w):
        a = random.randint(0, max) / max
        b = random.randint(0, max) / max
        if a <= p_error or b <= p_error:  #出错
            if first_wrong == 0:
                first_wrong = i + 1
    if first_wrong == 0:  #无差错
        for i in range(w):
            win1[i] = win1[i] + w
    else:
        for i in range(w):
            win1[i] = win1[i] + first_wrong - 1
    print('t:',t1,'lasttime_firstwrong:',first_wrong,'now_win:',win1)
    send1 = send1 + 5
    t1 = t1 + 1

print('回退N协议的发送效率：',N/send1,'  总延时：',t1*T)

