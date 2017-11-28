#!/usr/bin/env python3
# encoding: utf-8

"""
@version: v1.0
@author: Zyx-A
@license: Apache Licence
@contact: 448031904@qq.com
@site: http://laiyx.cc
@software: PyCharm
@file: baidu_fanyi.py
@time: 17-11-27 上午2:19
"""

import hashlib
import json
import random
import sys
import urllib.request
from string import Template

# 指定自己百度账号的API信息
appid = 'myAppid'  # 替换为您的APPID
secretKey = 'mySecretKey'  # 替换为您的密钥

# 是否以HTML格式显示
SHOW_HTML = True  # may change this

# 应用于GoldenDick显示的HTML代码
HTML_TEMPLATE = Template(r'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
<style>
div.fanyi {
    background-color: transparent;
}
p.translation {
    margin-left: 0.3em;
    margin-right: 0.3em;
}
span.water {
    float:right;
    font-size: 120%;
    font-family: Sans-Serif;
    color:#b9b9b9;
}
</style>
</head>
<body>
<span class="water">百度翻译</span>
<div class="fanyi">
<h3>${word}</h3>
<hr/>
<p class="translation">${translation}</p>
</div>
</body>
</html>''')


class FanyiError(Exception):
    pass


def judge_pure_english(keyword):
    # 判断是否为纯英文
    return all(ord(c) < 128 for c in keyword)


def judge_mix_chinese(keyword):
    # 判断是否含中文
    return any(True for i in str(keyword) if u'\u4e00' <= i <= u'\u9fff')


def fanyi(sentence):
    # 指定拼装信息
    apiurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    # sentence='I love you.\nAnd so on.'
    # 判断待翻译内容中是否有中文
    if judge_mix_chinese(sentence):
        if sentence.__len__() <= 2000:
            fromLang = 'zh'
            toLang = 'en'
        else:
            print('[ERROR] This sentence is too long. It must be less than 2000 words.')
            exit()
    else:
        if judge_pure_english(sentence):
            if sentence.__len__() <= 6000:
                fromLang = 'auto'
                toLang = 'zh'
            else:
                print('[ERROR] This sentence is too long. It must be less than 6000 bytes.')
                exit()
        else:
            if sentence.__len__() <= 2000:
                fromLang = 'auto'
                toLang = 'zh'
            else:
                print('[ERROR] This sentence is too long. It must be less than 2000 words.')
                exit()

    # 计算MD5签名
    signMd5 = appid + sentence + str(salt) + secretKey
    m = hashlib.md5()
    m.update(signMd5.encode(encoding='utf8'))
    sign = m.hexdigest()

    # 拼装api链接
    myurl = apiurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        sentence) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
    api_url = "http://api.fanyi.baidu.com" + myurl

    try:
        # 发起解析请求
        request = urllib.request.Request(api_url)
        # 获取返回结果
        response = urllib.request.urlopen(request)
        # 获取Reponse的返回码（状态码）
        # responseStatus=response.code
        # 获取API返回内容，并对JSON格式内容做重组
        responseRead = (response.read())
        jsResponse = json.loads(responseRead)
    except ValueError:
        raise FanyiError('[ERROR] invalid input')

    if not "error_code" in jsResponse.keys():
        word_src = None
        for i in jsResponse['trans_result']:
            # print(i['src']+' : '+i['dst'])
            if word_src is None:
                word_src = i['src']
                translation = i['dst']
            else:
                word_src = word_src + '\n' + i['src']
                translation = translation + '\n' + i['dst']
        # print('\n\n')
        # print(word_src.encode('utf8') + '\n\n' + translation.encode('utf8'))
        return translation
        response.close()
    else:
        print('[ERROR] error_code: ' + jsResponse['error_code'] + '\n[ERROR] error_msg:  ' + jsResponse['error_msg'])
        response.close()
        exit()


if __name__ == '__main__':
    try:
        word = ' '.join(sys.argv[1:])
        # word = 'I love you.\nAnd so on.'
        if not SHOW_HTML:
            print(fanyi(word))
        else:
            if sys.platform.startswith('win'):
                word = word.decode('gbk').encode('utf8')
            title = word
            trans = fanyi(word)
            sys.stdout.write(HTML_TEMPLATE.substitute(
                {'word': word.replace('\n', '<br>'),
                 'translation': trans.replace('\n', '<br>')}))
    except FanyiError:
        pass
