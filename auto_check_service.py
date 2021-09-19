import time
import traceback

import util
from utils import captcha, post_data, send_mails
from utils.sql import Sql


def auto_check():
    userList = Sql.list_user(Sql())
    for i in userList:
        account = i[1]
        passwd = i[2]
        address = i[3]
        mail = i[4]
        # print(account,passwd,address)
        try:
            ssid = util.getssid(account, passwd)
            captchas = captcha.get_yzm(ssid)
            result = post_data.post_check_data(ssid, captchas[1], captchas[0], address)
            if int(result['code']) == 1:
                # send_mails.send_result(account+"打卡成功，第一次使用建议检查结果", mail)
                print(1)
            else:
                # send_mails.send_result(account + "打卡失败，请联系我", mail)
                pass
        except Exception as e:
            err = {'err': e.args, 'traceback': traceback.format_exc()}
            send_mails.send_result(account + "打卡过程中发生错误，错误信息为：" + str(err), '1830910357@qq.com')

            time.sleep(30)


if __name__ == "__main__":
    auto_check()
