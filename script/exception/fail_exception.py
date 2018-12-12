#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   执行失败


class FailException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
