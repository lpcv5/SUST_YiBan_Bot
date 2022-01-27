import time
import traceback

import util
import post_data
import captcha


# 分别填入你的账号密码以及要提交的地址
def auto_check():
    account = ""
    passwd = ""
    address = ""
    print(account, passwd, address)
    try:
        ssid = util.getssid(account, passwd)
        captchas = captcha.get_yzm(ssid)
        result = post_data.post_check_data(ssid, captchas[1], captchas[0], address)
        if int(result['code']) == 1:
            print(1)
        else:
            pass
    except Exception as e:
        err = {'err': e.args, 'traceback': traceback.format_exc()}
        print(str(err))


if __name__ == "__main__":
    auto_check()
