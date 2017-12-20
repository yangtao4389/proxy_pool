"""
该文件实现了从proxy_pool这个项目中调用api接口,然后访问
http://httpbin.org/ip
得到的结果为请求的ip,进行验证.
发现成功率并不高

"""

import requests
from fake_useragent import UserAgent
import random
import json

class UseProxy():
    def __init__(self):
        self.valid_url = 'http://httpbin.org/ip'
        _ua = UserAgent()
        self.user_agent = _ua.random

    def get_headers(self):
        headers = {}
        headers['User-Agent'] = self.user_agent
        return headers

    def get_proxies(self):
        #                       调用ip代理池的get_all方法,返回list形式的json
        response = requests.get('http://127.0.0.1:5010/get_all/')
        list_proxy = json.loads(response.content.decode())

        if len(list_proxy) > 0:
            random_proxy = random.choice(list_proxy)
        else:
            # 如果为空,返回字典,这个代理是被允许的
            return {}

        proxy = {"http": "http://{proxy}".format(proxy=random_proxy)}

        return proxy



    def request(self):
        print(self.get_proxies())
        response = requests.get(self.valid_url,headers=self.get_headers(),proxies=self.get_proxies())
        print(response.content)


    def run(self):
        # 主函数
        # 1.构造url请求,调用代理
        # 2.校验响应结果
        self.request()


if __name__ == '__main__':
    while True:
        try:
            u = UseProxy()
            u.run()
        except Exception:
            pass
        