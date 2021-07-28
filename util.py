import re

import requests
import json


# 获取token
def get_access_token(account, password):
    url = 'https://mobile.yiban.cn/api/v3/passport/login'
    param = "mobile=" + account + "&password=" + password + "&imei=" + getIMEI(account)
    realurl = url + '?' + param

    headers = {
        "AppVersion": "4.9.11",
        "User-Agent": "YiBan/4.9.11 Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 ("
                      "KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36",
        "Host": "mobile.yiban.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    response = requests.get(realurl, headers)

    d = json.loads(response.text)
    access_token = d["data"]["user"]["access_token"]

    return access_token


def update_access_token():
    with open("data.json") as json_file:
        access_token = json.load(json_file)
    if access_token['token'] == 0:
        token = {"token": get_access_token('18696536980', '1489753lpc')}
    with open('data.json', 'a') as jf:
        json.dump(token, jf)
    print('token存储成功')


def getIMEI(account):
    return '86' + account[0:5] + account[4] + account[9] + account[7] + account[6:11]


def get_iappurl(access_token):
    url = 'https://mobile.yiban.cn/api/v3/home'
    param = '?access_token=' + str(access_token)
    realurl = url + param

    headers = {
        "Authorization": "Bearer " + str(access_token),
        "loginToken": access_token,
        "AppVersion": "4.9.11",
        "User-Agent": "YiBan/4.9.11 Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 ("
                      "KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36",
        "Host": "mobile.yiban.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    response = requests.get(realurl, headers)
    d = json.loads(response.text)

    if d['response'] != 100:
        with open("app.json") as json_file:
            date = json.load(json_file)
        date['token'] = 0
        update_access_token()

    p = 0
    for i in d['data']['hotApps']:
        p += 1
        if i['name'] == '信息上报':
            appurl = i['url']
            return appurl, p
            break


def get_sessionid(raw_cookie):
    ssid = re.findall(r"PHPSESSID=(.+?);", raw_cookie)
    return ssid[0]
