#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com

import re
import os
import logging
logging.basicConfig(level=logging.INFO)


def replace(file_path, old_params, new_params):
    """
    替换文件中的关键字
    :param file_path: 文件路径
    :param old_params: 需要替换的旧的关键字
    :param new_params: 新的值
    :return: void
    """
    logging.info("\tfile file_path: " + file_path + "; old_params: " + ", ".join(old_params) + "; new_params: " + ", ".join(new_params))
    if len(old_params) <= 0 or len(new_params) <= 0:
        print("can't find replace params.")
        return
    read_file = open(file_path, 'r',  encoding="UTF-8")
    content = ""
    for line in read_file:
        for param in old_params:
            if re.search(param, line):
                line = re.sub(param, new_params[old_params.index(param)], line)
        content += line
    read_file.close()
    write_file = open(file_path, 'w',  encoding="UTF-8")
    write_file.write(content)
    write_file.close()


if __name__ == "__main__":
    file_path = os.path.abspath("../config/") + "hk_master-hk-bi-services\config.xml"
    replace(file_path, ["stroll_node", "stroll_service"], ["hello", "world"])
