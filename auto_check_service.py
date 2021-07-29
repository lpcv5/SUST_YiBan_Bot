import util
from utils import captcha, post_data, send_mails
from utils.sql import Sql


def auto_check():
    userList = Sql.list_user(Sql())
    result_dict = {}
    for i in userList:
        account = i[1]
        passwd = i[2]
        address = i[3]
        # print(account,passwd,address)
        ssid = util.getssid(account, passwd)
        captchas = captcha.get_yzm(ssid)
        result = str(post_data.post_check_data(ssid, captchas[1], captchas[0], address))
        result_dict[account] = result
    send_mails.send_result(str(result_dict))

auto_check()