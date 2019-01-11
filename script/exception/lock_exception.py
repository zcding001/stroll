#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   获取锁、释放锁


class LockException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
