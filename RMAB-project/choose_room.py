from selenium.webdriver import Firefox
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

XUE_HAO = "202322011336"  # 学号
MI_MA = "BZX45926"  # 密码

driver = webdriver.Firefox()
driver.get("https://hq.uestc.edu.cn/dormitory/dormitoryOnlineChooseRoom")
driver.implicitly_wait(0.3)
# 学号
driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/input").send_keys(XUE_HAO)
# 密码
driver.find_element(By.XPATH, "/html/body/div/div[2]/div[3]/input").send_keys(MI_MA)
# 登陆
driver.find_element(By.XPATH, "/html/body/div/div[2]/div[5]/img").click()

# 方案二
JSESSIONID=driver.get_cookies()[0]['value']

cookies = {
    'JSESSIONID': JSESSIONID
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://hq.uestc.edu.cn',
    'Connection': 'keep-alive',
    'Referer': 'https://hq.uestc.edu.cn/dormitory/dormitoryOnlineChooseRoom/dormitoryChooseBed',
    # 'Cookie': 'JSESSIONID=C3443DF86919DCA7157B7E14915642E1',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

data = {
    'bed_id': '61264',
    'choose_bed_auth_counsellor_id': '25805',
}

response = requests.post('https://hq.uestc.edu.cn/dormitory/dormitoryOnlineChooseRoom/studentChooseBed', cookies=cookies, headers=headers, data=data)
print(response.text)








# 方案一

# # 还没定,随便写的
# TARGET_ROOM = "清水河校区-硕士27栋-6楼603号"
# # HTML路径
# XPATH = "/html/body/div[2]/div[2]/div[{}]"
# ROME_NAME = "/div[1]/div"
# BED_NUM = "/div[4]/span"
# IM_AGGRE = "/html/body/div[5]/div[3]/a[1]"
# NEXT_PAGE = "layui-laypage-next"
# LOADING_PAGE = "layui-layer-shade"
# LOADING_BED = "layui-layer-shade1"

# def Is_Exist(element):
#     try:
#         driver.find_element(By.CLASS_NAME, element)
#     except:
#         return False
#     else:
#         return True


# def Waiting_Loading(element, reverse=False):
#     while True:
#         if Is_Exist(element) == reverse:
#             break


# flag_find = False
# while True:
#     for i in range(1, 19):
#         room = driver.find_element(By.XPATH, (XPATH + ROME_NAME).format(i))
#         bed = driver.find_element(By.XPATH, (XPATH + BED_NUM).format(i))
#         # 清水河校区-硕士27栋-6楼603号
#         print(room.text)
#         # 无剩余床位
#         # 剩余床位:1
#         # 剩余床位:2
#         print(bed.text)
#         if room.text == TARGET_ROOM :
#             room.click()
#             Waiting_Loading(LOADING_BED)
#             if Is_Exist("room"):
#                 driver.find_element(By.CLASS_NAME, "room").find_element(
#                     By.XPATH, "img[2]"
#                 ).click()
#                 driver.find_element(By.XPATH, IM_AGGRE).click()
#                 flag_find = True
#                 break
#     if flag_find:
#         break
#     else:
#         driver.find_element(By.CLASS_NAME, NEXT_PAGE).click()
#         Waiting_Loading(LOADING_PAGE)

