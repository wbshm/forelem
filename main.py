import re
import sys

import requests
from urllib.parse import urlparse
import json


class login_info_obj(object):
    login_cookie = ""
    eleme_url = ""
    user_info = {}  # 用户信息
    lucky_number = 0  # 幸运的礼包码
    sn = ""
    qq = ""
    SID = ""

    def __init__(self, qq, start_url):
        self.qq = qq
        try:
            with open("./tmp/userInfo/qq_%s.json" % self.qq, 'r', encoding='utf-8') as content:
                self.user_info = json.load(content)
                if 'SID' in self.user_info:
                    self.SID = self.user_info['SID']
        except FileNotFoundError:
            print('File Not Found Error')
            exit(sys._getframe().f_lineno)
        self.eleme_url = start_url
        self.analysis_url()

    def do_it(self):
        res = self.open_page()
        try:
            result = res.json()
            # {"message":"用户验证失败","name":"PHONE_IS_EMPTY"}
            if 'name' in result and result['name'] == 'PHONE_IS_EMPTY':
                phone_num = self.check_phone()
                if phone_num == False:
                    print('phone num error')
                    exit(sys._getframe().f_lineno)
                validate_token = self.mobile_send_code(phone_num)
                code = input("输入验证码:")
                self.login_by_mobile(phone_num, code, validate_token)
                res = self.open_page()
                print(res)
            elif 'promotion_records' in result:
                count = len(result['promotion_records'])
                if count == self.lucky_number - 1:
                    print('the next one is biggest')
                    exit(0)
                elif count >= self.lucky_number - 1:
                    print('the lucky page is gone')
                    exit(-1)
                else:
                    print('current index is %s' % count)
        except ValueError:
            print('fatal error')
            exit(sys._getframe().f_lineno)
        return True

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
        # {"validate_token":"a4819b0386f4ac313dd71037bd8258e233a96b5f4ac002451f23bcc0b208c05f"}
        res = requests.post(request_url, data=request_data)
        res_data = (json.loads(res.text))
        if 'validate_token' in res_data:
            return res_data['validate_token']
        else:
            print('需要图形验证码，换个手机号')
            exit(sys._getframe().f_lineno)

    def login_by_mobile(self, mobile, code, token):
        request_url = "https://h5.ele.me/restapi/eus/login/login_by_mobile"
        request_data = {
            'mobile': mobile,
            'validate_code': code,
            'validate_token': token
        }
        request_header = {
        }
        res = requests.post(request_url, data=request_data, headers=request_header)
        self.SID = res.cookies['SID']
        self.user_info['SID'] = self.SID
        return json.loads(res.text)

    def open_page(self):
        request_url = "https://h5.ele.me/restapi/marketing/promotion/weixin/" + self.user_info['openid']
        request_data = {
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

        request_header = {
            "x-shard": self.get_xshard(self.sn),
            'cookie': "SID=%s" % str(self.SID)
        }
        res = requests.post(request_url, data=request_data, headers=request_header)
        return res

    def analysis_url(self):
        self.sn = self._get_url_params(self.eleme_url, 'sn=')
        self.lucky_number = self._get_lucky_number()
        pass

    @staticmethod
    def _get_url_params(url, pick_key):
        url_dic = urlparse(url)
        param_arr = url_dic.fragment.split('&')
        try:
            return list(filter(lambda x: pick_key == x[:len(pick_key)], param_arr)).pop()[len(pick_key):]
        except IndexError:
            print('param %s does not exist' % pick_key)
            return ""

    def check_phone(self):
        phone_pat = re.compile('^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
        count = 3  # 最大尝试次数
        while True:
            mobile = input("请输入电话号码,以获取验证短信:")
            res = re.search(phone_pat, mobile)
            if res:
                print('正常手机号')
                return mobile
            else:
                print('手机号错误')
                count -= 1
            if count <= 0:
                return False

    def write_data(self):
        with open("./tmp/userInfo/qq_%s.json" % self.qq, 'w') as f:
            f.write(json.dumps(self.user_info))

    def _get_lucky_number(self):
        url = 'https://h5.ele.me/restapi/marketing/themes/3249/group_sns/%s' % self.sn
        res = requests.get(url)
        data = json.loads(res.text)
        if 'lucky_number' in data:
            return data['lucky_number']
        else:
            print('lucky number error')
            exit(sys._getframe().f_lineno)


if __name__ == '__main__':
    # res = requests.post('http://127.0.0.1')
    # print(res.cookies['nihao1'])
    # exit(1)
    qq = 2853306388
    start_url = "https://h5.ele.me/hongbao/?from=groupmessage&isappinstalled=0#hardware_id=&is_lucky_group=True&lucky_number=0&track_id=&platform=0&sn=2a1410571cb9d875&theme_id=3321&device_id=&refer_user_id=13526990"
    # try:
    #     with open("./tmp/userInfo/qq_%s.json" % qq, 'r', encoding='utf-8') as content:
    #         print(content)
    #         user_info = json.load(content)
    #         print(user_info)
    # except FileNotFoundError:
    #     print('File Not Found Error')
    #     # exit(sys._getframe().f_lineno)
    # print()

    test = login_info_obj(qq, start_url)
    test.do_it()
    # a = login_info_obj(98709484, start_url)
