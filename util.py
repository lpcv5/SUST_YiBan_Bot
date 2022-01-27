import base64
import os
import re

import requests
import rsa


key = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzAAjffez4G4A" \
      "/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegICXC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx" \
      "+WasvbS0HuYpF8+KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bPA9/I5kwfyZ/mM5m8" \
      "+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7" \
      "/2vgq7kw2qSmRAGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOpd2rEpX0/8YE0dRXxukrM7i" \
      "+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/7QT4SZrnRBEo" \
      "++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/hmfJYekb3GEV+10xLOvpe" \
      "/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNUAYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg" \
      "/IVv6HkFEuCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbRZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ" \
      "==\n-----END PUBLIC KEY-----"


def encrpty_password(password):
    data = password.encode('utf-8')
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
    enc = rsa.encrypt(data, pubkey)
    ret = base64.b64encode(enc).decode(encoding='utf-8')
    return ret


def get_token(acount, password):
    params = {
        "mobile": acount,
        "password": encrpty_password(password),
        "ct": "2",
        "app": "1",
        "v": "5.0.4",
        "apn": "wifi",
        "identify": "123123123123123",
        "sig": "2asdasd",
        "token": "",
        "device": "xiaomi",
        "sversion": "30",
        "authCode": ""
    }
    headers = {
        "AppVersion": "5.0"
    }
    r = requests.post("https://m.yiban.cn/api/v4/passport/login",
                      data=params, headers=headers)
    return r.json()["data"]["access_token"]


def getpath():
    return os.path.split(os.path.realpath(__file__))[0]


def getssid(account, passwd):
    try:
        print(account, passwd)
        token = get_token(account, passwd)
        appurl = "https://f.yiban.cn/iapp610661"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10.0; xiaomi 10 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 yiban_android/5.0.3',
            'appversion': '5.0.3',
            'signature': 'A3oHcLhQ8OCmXLuxOy4Y66TXyG/FrDhG+sCFRM1gXheN+LB0a9f3nVsnAgblO/0g7rPlHtfSob28RrKpwkdv9A',
            'logintoken': token,
            'authorization': 'Bearer ' + token,
            'Cookie': 'loginToken=' + token + '; client=android'

        }
        response1 = requests.get(appurl, headers=headers, allow_redirects=False)
        print('第一次重定向结果:', response1.headers["location"])
        print(response1.cookies["https_waf_cookie"])
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10.0; xiaomi 10 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 yiban_android/5.0.3',
            'appversion': '5.0.3',
            'signature': 'A3oHcLhQ8OCmXLuxOy4Y66TXyG/FrDhG+sCFRM1gXheN+LB0a9f3nVsnAgblO/0g7rPlHtfSob28RrKpwkdv9A',
            'logintoken': token,
            'authorization': 'Bearer ' + token,
            'Cookie': 'loginToken=' + token + '; client=android;https_waf_cookie=' + response1.cookies["https_waf_cookie"]
        }
        response2 = requests.get(response1.headers['location'], headers=headers,
                                 allow_redirects=False)
        print('第二次重定向结果:', response2.headers['location'])

        response3 = requests.get(response2.headers['location'], allow_redirects=False)
        final_url = 'http://yiban.sust.edu.cn/v4/yibanapi/' + response3.headers['location']
        print(final_url)

        response4 = requests.get(final_url, allow_redirects=False)
        print(response4.headers)
        ssid = re.findall(r'PHPSESSID=(.+?);', response4.headers['Set-Cookie'])[0]
        print(ssid)
        return ssid
    except:
        pass


