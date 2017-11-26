#!/usr/bin/env python2.7
# encoding: utf-8

"""
@author: meow
@site: http://code.taobao.org/p/youdao_translate/src/
@software: PyCharm
@file: youdao_fanyi.py
"""


import urllib2, urllib
import json
import zlib
from string import Template
import cgi
import sys

SHOW_HTML = True #may change this

HTML_TEMPLATE = Template(r'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
<style>
div.youdao_fanyi {
    background-color: #f9f9f9;
}
p.youdao_translation {
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
<span class="water">有道翻译</span>
<div class="youdao_fanyi">
<h3>${word}</h3>
<hr/>
<p class="youdao_translation">${translation}</p>
</div>
</body>
</html>'''.decode('utf8'))

class FanyiError(Exception):
    pass

def fanyi(sentence):

    if any(True for i in str(sentence) if i > '\x7f'):
        trans_type = 'ZH_CN2EN'
    else:
        trans_type = 'EN2ZH_CN'

    url = 'http://fanyi.youdao.com/translate?'
    param = (('smartresult', 'dict'),
                ('smartresult', 'rule'),
                ('smartresult', 'ugc'))
    query = {'type': trans_type, 'i': sentence,
            'doctype':'json', 'xmlVersion':'1.6',
            'keyfrom':'fanyi_web', 'ue':'UTF-8',
            'typoResult':'true', 'flag':'false'}

    req = urllib2.Request(
            url+urllib.urlencode(param),
            urllib.urlencode(query)
            )

    req.add_header('connection', 'close')
    #req.add_header('content-type', 'application/x-www-form-urlencoded; charset=utf-8')
    req.add_header('accept', '*/*')
    req.add_header('accept-charset', 'utf-8')
    req.add_header('accept-encoding', 'gzip,deflate')
    req.add_header('accept-language', 'en;q=0.8,en-US;q=0.6,en;q=0.4')
    req.add_header('user-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)')
    req.add_header('host', 'fanyi.youdao.com')

    respData = urllib2.urlopen(req).read()

    result = zlib.decompress(respData, zlib.MAX_WBITS|16)

    try:
        data = json.loads(result)
    except ValueError:
        raise FanyiError('invalid input')

    if data['errorCode'] == 0:
        try:
            return data['translateResult'][0][0]['tgt']
        except IndexError, KeyError:
            raise FanyiError('no result')
    else:
        raise FanyiError('non zero error code')

if __name__ == '__main__':
    import sys
    try:
        word = ' '.join(sys.argv[1:])
        if not SHOW_HTML:
            print fanyi(word).encode('utf8')
        else:
            if sys.platform.startswith('win'):
                word = word.decode('gbk').encode('utf8')
            title = cgi.escape(word)
            trans = cgi.escape(fanyi(word))
            sys.stdout.write(HTML_TEMPLATE.substitute(
                    {'word':word.decode('utf8'),
                    'translation':trans}).encode('utf8'))
    except FanyiError:
        pass
