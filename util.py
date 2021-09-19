import os
import re

import requests

from utils import login


def getpath():
    return os.path.split(os.path.realpath(__file__))[0]


# 随机生成手机imei
def getIMEI(account):
    return '86' + account[0:5] + account[4] + account[9] + account[7] + account[6:11]


def getssid(account, passwd):
    try:
        appurl = "https://f.yiban.cn/iapp610661"
        cookies = login.get_cookies(account, passwd)
        response1 = requests.get(appurl, cookies=cookies, allow_redirects=False)
        # print(response1.headers)
        # print('第一次重定向结果:', response1.headers['location'])
        response2 = requests.get(response1.headers['location'], cookies=cookies,
                                 allow_redirects=False)
        # print(response2.headers)
        response3 = requests.get(response2.headers['location'], cookies=response2.cookies,
                                 allow_redirects=True)
        ssid = re.findall(r'PHPSESSID=(.+?);', response3.headers['Set-Cookie'])[0]
        # print(response3.headers)
        # print(ssid)
        return ssid
    except:
        getssid(account, passwd)
