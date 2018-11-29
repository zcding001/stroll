#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com

import re


def replace(path, old_params, new_params):
    """
    替换文件中的关键字
    :param path: 文件路径
    :param old_params: 需要替换的旧的关键字
    :param new_params: 新的值
    :return: void
    """
    if len(old_params) <= 0 or len(new_params) <= 0:
        print("can't find replace params.")
        return
    read_file = open(path, 'r')
    content = ""
    for line in read_file:
        for param in old_params:
            if re.search(param, line):
                line = re.sub(param, new_params[old_params.index(param)], line)
                content += line
            else:
                content += line
    read_file.close()
    print(content)
    write_file = open(path, 'w')
    write_file.write(content)
    write_file.close()
