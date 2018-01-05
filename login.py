#!/Users/wenlong/PycharmProjects/scrapy_tutorial/venv/bin python3
# -*- coding: utf-8 -*-

import requests
import time
from PIL import Image
import json
import re


def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=headers)
    match_obj = re.match('[\s\S]*name="_xsrf" value="(.*?)"', response.text)
    if match_obj:
        return match_obj.group(1)
    return ''


# 获取验证码参数
def get_captcha():
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login&lang=cn" % (int(time.time() * 1000))
    response = session.get(captcha_url, headers=headers)

    # 保存验证码到当前目录
    with open('captcha.gif', 'wb') as f:
        f.write(response.content)
        f.close()

    # 自动打开刚获取的验证码
    try:
        img = Image.open('captcha.gif')
        img.show()
        img.close()
    except:
        pass

    captcha = {
        'img_size': [200, 44],
        'input_points': [],
    }
    points = [[19, 19], [48, 22], [67, 28], [102, 25], [126, 26], [133, 19], [168, 23]]
    location = input('请输入倒立字的位置\n>')
    for i in location:
        captcha['input_points'].append(points[int(i) - 1])

    return json.dumps(captcha)


def zhifu_login(phone, password):
    post_url = 'https://www.zhihu.com/login/phone_num'
    post_data = {
        'captcha_type': 'cn',
        '_xsrf': get_xsrf(),
        'phone_num': phone,
        'password': password,
        'captcha': get_captcha(),
    }
    response = session.post(post_url, data=post_data, headers=headers)
    response_json = json.loads(response.text)
    print(response.text)
    if 'msg' in response_json and response_json['msg'] == '登录成功':
        print('登录成功！')
    else:
        print('登录失败')


if __name__ == '__main__':
    session = requests.session()
    headers = {
        "Host": "www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/63.0.3239.84 Safari/537.36"
    }
    zhifu_login("18613178137", "111111")
