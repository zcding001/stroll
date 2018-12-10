#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   模拟请求工具类

import urllib.request
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def send_request(url):
    try:
        res = urllib.request.urlopen(url)
        code = res.getcode()
        logging.info("request response code is [%s]." % code)
        if code == 200:
            return code
    except Exception:
        logging.info("Sending request fail. url is [%s]" % url)
    return -200
