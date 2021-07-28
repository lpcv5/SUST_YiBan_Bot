import json
import re
import time
import requests.sessions


def goto_home_page(access_token, appurl):
    headers = {
        "Host": "f.yiban.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 yiban_android/4.9.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "appversion": "4.9.11",
        "signature": "A3oHcLhQ8OBEArl1cUn0WkS5O/fgCaFWBI/4UcHzLRrDQc4SsVnb5hfd+Pd6qx5MY7Ll7iWdkVMRee2H0Z/3AQ",
        "logintoken": access_token,
        "authorization": "Bearer " + access_token,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "loginToken=" + access_token + "; client=android",
        "X-Requested-With": "com.yiban.app"
    }
    Cookie1 = {
        "loginToken": access_token,
        'client': 'android'
    }
    response1 = requests.get(appurl, headers=headers, cookies=Cookie1, allow_redirects=False)
    print('第一次重定向结果:', response1)

    # 二次重定向
    url = 'https://f.yiban.cn/iapp/index'
    param = 'act=' + re.findall(r"https://f.yiban.cn/(.+?)\?", appurl)[0]
    realurl = url + '?' + param

    set_cookie = re.findall(r"https_waf_cookie=(.+?);", response1.headers['Set-Cookie'])[0]
    headers1 = {
        "Host": "f.yiban.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 yiban_android/4.9.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "appversion": "4.9.11",
        "signature": "A3oHcLhQ8OBEArl1cUn0WkS5O/fgCaFWBI/4UcHzLRrDQc4SsVnb5hfd+Pd6qx5MuJ/wO3yVjoJeh+nx8GEr6A",
        "logintoken": access_token,
        "authorization": "Bearer " + access_token,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "loginToken=" + access_token + "; client=android; https_waf_cookie=" + set_cookie + "; "
                                                                                                      "_YB_OPEN_V2_0=402RD0lohV9g4Ef0; yibanM_user_token=" + access_token,
        "X-Requested-With": "com.yiban.app"
    }
    # print(headers)

    # 获取主页认证地址
    Cookie2 = {
        "loginToken": access_token,
        'client': 'android',
        "https_waf_cookie": set_cookie,
        "_YB_OPEN_V2_0": "402RD0lohV9g4Ef0",
        "yibanM_user_token": access_token
    }
    response2 = requests.get(realurl, headers=headers1, cookies=Cookie2, allow_redirects=False)
    redirects_url = response2.headers['location']
    print('第二次重定向结果:', response2)

    # 跳转到信息上报主页
    headers2 = {
        "Host": "yiban.sust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Geck"
                      "o) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 yiban_android/4.9.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "appversion": "4.9.11",
        "signature": "A3oHcLhQ8OBEArl1cUn0WkS5O/fgCaFWBI/4UcHzLRrDQc4SsVnb5inwKOvXf/MFBgHAvYRbEOnTPMeJb/In6Q",
        "logintoken": access_token,
        "authorization": "Bearer " + access_token,
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.yiban.app"
    }
    response3 = requests.get(redirects_url, headers=headers2, allow_redirects=True)
    # page_url = response3.headers['location']
    # print(page_url)
    print(response3.headers['Set-Cookie'])

    return response3.headers['Set-Cookie']


# def get_check_page(select):
#     with open("url.json") as url:
#         if

def post_check_data(ssid):
    url = 'http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/add.html'
    param = {
        "desgin_id": 25,
        "list_id": 12,
        "verify": "tw2r",
        "uniqid": "captcha6100f32d8fe043627"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; vivo v3 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 yiban_android/4.9.11",
        "Cookie": "PHPSESSID=" + ssid
    }

    data = {
        "25[0][0][name]": "form[25][field_1588750276_2934][]",
        "25[0][0][value]": "36.5",

        "25[0][1][name]": "form[25][field_1588750304_5363][]",
        "25[0][1][value]": "陕西省+西安市+未央区+111县道+111县+靠近陕西科技大学学生生活区+",

        "25[0][2][name]": "form[25][field_1588750323_2500][]",
        "25[0][2][value]": "是",

        "25[0][3][name]": "form[25][field_1588750343_3510][]",
        "25[0][3][value]": "否",

        "25[0][4][name]": "form[25][field_1588750363_5268][]",
        "25[0][4][value]": 1
    }
    cookies = {"PHPSESSID": ssid}
    response = requests.post(url=url, headers=headers, data=data, cookies=cookies, params=param)
    print(response)
    print('---------------------------------------------------------------------------------')
    print(response.text)
