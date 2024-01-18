import random
'误码率与传输延时'
p1 = 0.01
p2 = 0.1
T1 = 1
T2 = 10
'数据包与窗口'
N = 500
w = 5
r2 = [0, 0, 0, 0, 0]
ack2 = [0, 0, 0, 0, 0]
t2 = 1
win2 = [0, 1, 2, 3, 4]
send2 = 5
allack = []  #总应答
for i in range(N+5):  #预防溢出
    allack.append(0)
'网络环境参数'
p_error = 0.1
T = T1
max = 1000000

def getrandom(win):
    ran = []
    ww = w
    num_wrong = 0
    first_wrong = 0
    if N - win[0] < w:
        ww = N - win[0] + 1
    for i in range(ww):
        if allack[win[i]] == 1:  #判断是否已经收到
            ran.append(1)
        else:
            a = random.randint(0, max) / max
            b = random.randint(0, max) / max
            if a > p_error or b > p_error:
                ran.append(1)
            else:
                ran.append(0)
                num_wrong = num_wrong + 1  #记录错误个数
                if first_wrong == 0:
                    first_wrong = i+1  #记录第一个错误位置1/2/3/4/5
    return ran, num_wrong, first_wrong

'选择重传仿真'
begin = 0  #发送窗口的开始位置
while win2[4] < N - 1:
    '调整发送窗口'
    for i in range(w):
        win2[i] = begin + i
    '随机差错'
    ran, num, fir = getrandom(win2)

    '判断有无差错'
    if num == 0:
        for i in range(w):
            allack[begin + i] = 1
            win2[i] = win2[i] + w
        begin = begin + w
        send2 =send2 + w
        now_send = 5
    else:
        '收到，窗口向前移动'
        for i in range(w):
            if ran[i] == 1:
                allack[begin+i] = 1
            win2[i] = win2[i] + fir - 1
        begin = begin + fir - 1
        '计算下轮发包'
        now_send = 0
        for i in range(w):
           if allack[begin+i] == 0:
               now_send = now_send + 1
        send2 = send2 + now_send
    t2 = t2 + 1

    print('success?:',ran,'t:',t2,'win:',win2,'nowsend:',now_send)

    if(win2[4] >= N):
        more = win2[4]-N+1  #窗口超出界限多发的包
        send2 = send2 - more
        break

print('选择重传协议的发送效率：',N/send2,'  总延时：',t2*T)

