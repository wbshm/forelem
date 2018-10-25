import re
import sys

import requests
from urllib.parse import urlparse
import json

baseUrl = {
    # {"mobile":"15659663812","captcha_value":"","captcha_hash":""}
    'send_code': 'https://h5.ele.me/restapi/eus/login/mobile_send_code',

    # {"mobile":"15659663812","validate_code":"772605","validate_token":"003dd9da70846255f81e8f3605ec568e6326e40619ceaa34b3ce90a5e1d92e3e"}
    'login_mobile':
        "https://h5.ele.me/restapi/eus/login/login_by_mobile",

    'userinfo':
        'https://waltz.ele.me/qq/userinfo/?code=71804A0678A3780983791B0C5A324674',
}

# code: 71804A0678A3780983791B0C5A324674
headers = {
    "user-agent":
        "Mozilla/5.0 (Linux; Android 7.0; MIX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044004 Mobile Safari/537.36 V1_AND_SQ_7.5.0_794_YYB_D QQ/7.5.0.3430 NetType/WIFI WebP/0.3.0 Pixel/1080",

}

data = {}
res = requests.get('http://baidu.com', headers=headers, data=data)



class login_info_obj(object):
    login_cookie = ""
    eleme_url = ""
    user_info = {}  # 用户信息
    luck_number = 0  # 幸运的礼包码
    sn = ""

    def __init__(self, qq, start_url):
        try:
            with open("./tmp/userInfo/qq_%s.json" % qq, 'r', encoding='utf-8') as content:
                print(content)
                self.user_info = json.load(content)
        except FileNotFoundError:
            print('File Not Found Error')
            exit(sys._getframe().f_lineno)
        self.eleme_url = start_url
        self.analysis_url()

    def do_it(self):
        res = self.open_page()
        try:
            result = res.json()
            #{"message":"用户验证失败","name":"PHONE_IS_EMPTY"}
            if 'name' in result and result['name'] == 'PHONE_IS_EMPTY':
                self.check_phone()
        except ValueError:
            print('fatal error')
            exit(sys._getframe().f_lineno)

    def get_cookie(self):
        return self.login_cookie

    def set_cookie(self, cookie):
        self.login_cookie = cookie.strip()

    def clean_cookie(self, cookie):
        if (cookie[-1:] == '"' and cookie[0:1] == '"') or (cookie[-1:] == "'" and cookie[:1] == "'"):
            cookie = cookie[1:-1]
        return cookie

    def get_red_packet(self):
        pass

    def get_request_body(self, sn, headimgurl=0, nickname=0):
        body_info = {
            'device_id': '',
            'group_sn': sn,
            'hardware_id': '',
            'method': 'phone',
            'phone': '',
            'platform': 4,
            'sign': 'this.cookie.sign',
            'track_id': '',
            'unionid': 'fuck',
            'weixin_avatar': headimgurl,
            'weixin_username': nickname,
        }
        return body_info

    def get_header(self):
        headers = {
            'x-shard': self.get_xshard(),
            'cookie': "SID=" + self.login_cookie.sid
        }
        return headers

    @staticmethod
    def get_xshard(sn=''):
        if sn == '':
            sn = '29e47b57971c1c9d'
        return "eosid=" + str(int(sn, 16))

    def mobile_send_code(self, mobile):
        request_url = "https://h5.ele.me/restapi/eus/login/mobile_send_code"
        request_data = {
            'captcha_hash': '',
            'captcha_value': '',
            'mobile': mobile
        }
        request_header = {
            'cookie': self.get_cookie()
        }
        # {"validate_token":"a4819b0386f4ac313dd71037bd8258e233a96b5f4ac002451f23bcc0b208c05f"}
        res = requests.post(request_url, data=request_data, headers=request_header)
        return json.loads(res)['validate_token']

    def login_by_mobile(self, code):
        request_url = "https://h5.ele.me/restapi/eus/login/login_by_mobile"
        request_data = {
            'mobile': "15659663812",
            'validate_code': code,
            'validate_token': "a4819b0386f4ac313dd71037bd8258e233a96b5f4ac002451f23bcc0b208c05f"
        }
        request_header = {
            'cookie': self.get_cookie()
        }
        res = requests.post(request_url, data=request_data, headers=request_header)
        self.set_cookie(requests.cookies.RequestsCookieJar())  # sid
        return json.loads(res.text)

    def open_page(self):
        request_url = "https://h5.ele.me/restapi/marketing/promotion/weixin/" + self.user_info['openid']
        request_data = {
            {
                'device_id': "",
                'group_sn': self.sn,
                'hardware_id': "",
                'method': "phone",
                'phone': "",
                'platform': 4,
                'sign': self.user_info['eleme_key'],
                'track_id': "",
                'unionid': "fuck",
                'weixin_avatar': self.user_info['figureurl_2'],
                'weixin_username': self.user_info['nickname']
            }
        }
        request_header = {
            "x-shard": self.get_xshard(self.sn),
            'cookie': "SID=" + self.cookie.sid
        }
        res = requests.post(request_url, data=request_data, headers=request_header)
        return res

    def analysis_url(self):
        self.sn = self._get_url_params(self.eleme_url, 'sn=')
        self.luck_number = self._get_url_params(self.eleme_url, 'luck_number=')
        is_lucky_group = self._get_url_params(self.eleme_url, 'is_lucky_group=')
        pass

    @staticmethod
    def _get_url_params(url, pick_key):
        url_dic = urlparse(url)
        param_arr = url_dic.fragment.split('&')
        try:
            return list(filter(lambda x: pick_key == x[:len(pick_key)], param_arr)).pop()[len(pick_key):]
        except IndexError:
            print('param does not exist')
            return ""

    def check_phone(self):
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        count = 3
        while True:
            mobile = input("请输入电话号码,以获取验证短信:")
            res = re.search(phone_pat, mobile)
            if res:
                print('正常手机号')
                return True
            else:
                print('手机号错误')
                count -= 1
            if count <= 0:
                return False

if __name__ == '__main__':
    start_url = "https://h5.ele.me/hongbao/#hardware_id=&is_lucky_group=True&lucky_number=8&track_id=&platform=0&sn=10fcda587ea2d807&theme_id=1969&device_id=&refer_user_id=1097914722"
    qq = 987094841
    try:
        with open("./tmp/userInfo/qq_%s.json" % qq, 'r', encoding='utf-8') as content:
            print(content)
            user_info = json.load(content)
            print(user_info)
    except FileNotFoundError:
        print('File Not Found Error')
        # exit(sys._getframe().f_lineno)
    print()
    # a = login_info_obj(98709484, start_url)
