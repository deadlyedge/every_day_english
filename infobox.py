import hashlib
import uuid
from datetime import datetime

import requests


class InfoBox:
    NUMBERS_API = 'http://numbersapi.com/'
    BAIDU_TRANS_URL = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    BAIDU_TRANS_APPID = '20200210000382049'
    BAIDU_TRANS_KEY = 's4cyY4IsA6X8oNJMLMzj'

    def __init__(self):
        self.date = datetime.now()
        self.numbersURL = self.NUMBERS_API + '%s/%s/date' % (self.date.month, self.date.day)
        self.dayInHistory = requests.get(self.numbersURL).text
        self.translation = self.baiduTrans(self.dayInHistory)

    def baiduTrans(self, srcText):
        params = {
            'q': srcText,
            'from': 'auto',
            'to': 'zh',
            'appid': self.BAIDU_TRANS_APPID,
            'salt': str(uuid.uuid4()),
        }
        pre_sign = params['appid'] + params['q'] + params['salt'] + self.BAIDU_TRANS_KEY
        params['sign'] = hashlib.md5(pre_sign.encode()).hexdigest()
        try:
            # 直接将 params 和 apiURL 一起传入 requests.get() 函数
            response = requests.get(self.BAIDU_TRANS_URL, params=params)
            # 获取返回的 json 数据
            result_dict = response.json()
            # 得到的结果正常则 return
            if 'trans_result' in result_dict:
                return result_dict['trans_result'][0]['dst']
            else:
                return '百度翻译API故障，请尝试直接访问 %s' % self.BAIDU_TRANS_URL
        except Exception as e:
            print('Some errors: ', e)


if __name__ == '__main__':
    ib = InfoBox()
    print(ib.dayInHistory)
    print(ib.translation)
