import json
import re
import requests


# 破解验证码
def get_yzm(ssid):
    url = 'http://yiban.sust.edu.cn/v4/public/index.php/admin/login/captcha.html'
    cookies = {"PHPSESSID": ssid}
    r = requests.post(url, cookies=cookies)
    str1 = re.sub(r'\\', '', r.text)
    # print(str1)
    basecode = re.findall(r'"data:image/png;base64,(.+?)"', str1)[0]
    # print(basecode)
    uniqid = re.findall(r'"uniqid":"(.+?)"', str1)[0]
    data = {
        "image": basecode
    }
    coder = requests.post("http://216.127.186.79:19952/captcha/v1", data=data)
    d = json.loads(coder.text)
    code = d["message"]
    return uniqid, code
