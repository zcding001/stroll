#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   锁工具类

import os
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def try_lock(key, try_times=30):
    """
    创建锁
    :param key: 锁的key
    :param try_times: 尝试次数，每次等待1秒，默认30次
    :return: True 获取锁成功 False 失败
    """
    times = 1
    path = os.path.abspath("./output/lock") + os.path.sep + key
    while times <= try_times:
        logging.info("第[%s]次获取[%s]锁", times, key)
        try:
            if not os.path.exists(path) and not os.path.isdir(path):
                os.makedirs(path)
                return True
        except Exception as e:
            logging.error(e)
            pass
        times += 1
        time.sleep(1)
    return False


def free_lock(key):
    """
    释放锁
    :param key: 锁的key
    :return: None
    """
    logging.info("释放锁[%s]", key)
    path = os.path.abspath("./output/lock") + os.path.sep + key
    if os.path.exists(path) and os.path.isdir(path):
        os.rmdir(path)

