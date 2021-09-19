# coding=utf-8

import base64
import requests
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from bs4 import BeautifulSoup


# 获取通过加密的密码
def get_crypt_password(private_key, password):
    rsa = RSA.importKey(private_key)
    cipher = PKCS1_v1_5.new(rsa)
    ciphertext = encrypt(password, cipher)
    return ciphertext


def encrypt(msg, cipher):
    ciphertext = cipher.encrypt(msg.encode('utf8'))
    return base64.b64encode(ciphertext).decode('ascii')


def login_request(username, encrypt_password, code, data_keys_time):
    form_data = {
        'account': username,
        'password': encrypt_password,
        'captcha': code,
        'keysTime': data_keys_time
    }
    r = requests.post("https://www.yiban.cn/login/doLoginAjax",
                      data=form_data, allow_redirects=False)
    return r.cookies


def get_cookies(account, passwd):
    raw = requests.post('https://www.yiban.cn/login?go=https://f.yiban.cn/iapp610661').text
    soup = BeautifulSoup(raw, "html.parser")
    ul = soup.find("ul", id="login-pr")
    # data_keys = ul['data-keys']
    data_keys_time = ul['data-keys-time']
    # print(data_keys, data_keys_time)
    # basepasswd = get_crypt_password(data_keys, "1489753lpc")
    cookies = login_request(account, passwd, "", data_keys_time)
    # print(cookies)
    # access_token = re.findall(r'yiban_user_token=(.+?);', cookies['Set-Cookie'])[0]
    # print(access_token)
    return cookies
