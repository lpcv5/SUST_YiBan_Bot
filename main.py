import traceback

import post_data
import util
import captcha


def auto_check(account, token, address, capt):
    print('当前用户{}开始打卡'.format(account))
    try:
        ssid = util.get_ssid(token)
        # 晨检
        morningresult = post_data.morning_check(ssid, address, capt)
        # 午检
        afternoonresult = post_data.afternoon_check(ssid, address, capt)
        if int(morningresult['code']) == 1 & int(afternoonresult['code']) == 1:
            print('打卡成功')
        else:
            print(morningresult, afternoonresult)
    except Exception as e:
        err = {'err': e.args, 'traceback': traceback.format_exc()}
        print(str(err))
        print('打卡失败')


if __name__ == '__main__':
    captchacheck = captcha.CaptchaRead()
    data = util.read_account_data()
    for i in data['user']:
        ID = i['id']
        acc = i['account']
        passwd = i['passwd']
        address = i['address']
        token = i['token']
        if util.check_token(i['token'] if i['token'] is not None else "0"):
            print('开始自动晨午检')
            auto_check(acc, token, address, captchacheck)
        else:
            print('更新token')
            data['user'][ID]['token'] = util.get_token(acc, passwd)
            util.write_account_token(data)
