import json

import goto_checkpage
import util

with open("data.json") as json_file:
    d = json.load(json_file)
    if d["token"] != 0:
        access_token = d['token']
    else:
        util.update_access_token()

temp = util.get_iappurl(access_token)
print("appurl:", temp[0])
print("token:", access_token)
set_cookies = goto_checkpage.goto_home_page(access_token, temp[0])
print(set_cookies)
print(util.get_sessionid(set_cookies))

ssid = util.get_sessionid(set_cookies)
# with open("sessionid.json",'w') as sid:
#     sessid = {"ssid": util.get_sessionid(set_cookies, access_token)}
#     json.dump(sessid, sessid)
#     print("sessionid存储成功")

with open("url.json") as c_url:
    i_url = json.load(c_url)
    check_url = i_url["url_noon"]

goto_checkpage.post_check_data(ssid)



