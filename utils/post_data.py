import requests.sessions


def post_check_data(ssid, captcha, uniqid, address):
    url = 'http://yiban.sust.edu.cn/v4/public/index.php/index/formtime/add.html'
    param = {
        "desgin_id": 25,
        "list_id": 12,
        "verify": captcha,
        "uniqid": uniqid
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.2; iphone 8848 Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, "
                      "like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 yiban_android/5.0",
        "Cookie": "PHPSESSID=" + ssid
    }

    data = {
        "25[0][0][name]": "form[25][field_1588750276_2934][]",
        "25[0][0][value]": "36.5",

        "25[0][1][name]": "form[25][field_1588750304_5363][]",
        "25[0][1][value]": address,

        "25[0][2][name]": "form[25][field_1588750323_2500][]",
        "25[0][2][value]": "是",

        "25[0][3][name]": "form[25][field_1588750343_3510][]",
        "25[0][3][value]": "否",

        "25[0][4][name]": "form[25][field_1588750363_5268][]",
        "25[0][4][value]": 1}
    cookies = {"PHPSESSID": ssid}
    response = requests.post(url=url, headers=headers, data=data, cookies=cookies, params=param)
    return response.json()
