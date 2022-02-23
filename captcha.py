import re
import threading
import time

import requests
from readcaptcha.captch_crack_service import read
from readcaptcha.config import Config
from readcaptcha.event_loop import event_loop
from readcaptcha.interface import InterfaceManager


class CaptchaRead:
    def __init__(self):
        print('加载验证码识别服务')
        self.interface_manager = InterfaceManager()
        self.CONF_PATH = "readcaptcha/config.yaml"
        self.MODEL_PATH = "readcaptcha/model"
        self.GRAPH_PATH = "readcaptcha/graph"
        self.SYSTEM_CONFIG = Config(conf_path=self.CONF_PATH, model_path=self.MODEL_PATH, graph_path=self.GRAPH_PATH)
        # 开启识别验证码服务线程
        captcha_service_thread = threading.Thread(
            target=lambda: event_loop(self.SYSTEM_CONFIG, self.MODEL_PATH, self.interface_manager))
        captcha_service_thread.daemon = True
        captcha_service_thread.start()
        time.sleep(1)
        print('验证码识别服务加载成功')

    def get_yzm(self, ssid):
        url = 'http://yiban.sust.edu.cn/v4/public/index.php/admin/login/captcha.html'
        cookies = {"PHPSESSID": ssid}
        r = requests.post(url, cookies=cookies)
        str = re.sub(r'\\', '', r.text)
        basecode = re.findall(r'"data:image/png;base64,(.+?)"', str)[0]
        uniqid = re.findall(r'"uniqid":"(.+?)"', str)[0]
        code = read(basecode, self.SYSTEM_CONFIG, self.interface_manager)
        return uniqid, code
