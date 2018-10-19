import requests

baseUrl = {
    # {"mobile":"15659663812","captcha_value":"","captcha_hash":""}
    'send_code': 'https://h5.ele.me/restapi/eus/login/mobile_send_code',

    # {"mobile":"15659663812","validate_code":"772605","validate_token":"003dd9da70846255f81e8f3605ec568e6326e40619ceaa34b3ce90a5e1d92e3e"}
    'login_mobile':
        "https://h5.ele.me/restapi/eus/login/login_by_mobile",

    'userinfo':
        'https://waltz.ele.me/qq/userinfo/?code=71804A0678A3780983791B0C5A324674',
}

#code: 71804A0678A3780983791B0C5A324674
headers = {
    "user-agent":
        "Mozilla/5.0 (Linux; Android 7.0; MIX Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044004 Mobile Safari/537.36 V1_AND_SQ_7.5.0_794_YYB_D QQ/7.5.0.3430 NetType/WIFI WebP/0.3.0 Pixel/1080",

}

data = {}
res = requests.get('http://baidu.com', headers=headers, data=data)


class login_info_obj(object):
    login_cookie = ""

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


if __name__ == '__main__':
    print(login_info_obj.get_xshard())
