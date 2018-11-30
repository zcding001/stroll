# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   编译jar

from handler import config_handler
from utils import file_utils
import os
import shutil
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class BuildHandler:
    """
    构建war、jar等资源
    """
    def __init__(self, data):
        self.__ini_config = data
        self.__env_path = os.path.abspath(self.__ini_config.env_path)
        self.__copy_properties()

    def __copy_properties(self):
        # 复制公共资源
        common_file_list = file_utils.list_files(self.__env_path, root_name="common")
        for common_file in common_file_list:
            logging.debug(common_file)
            shutil.copy(common_file, os.path.abspath(self.__ini_config.env_path + os.path.sep + "env"))

        # 复制服务的properties到对应资源路径
        service_file_list = file_utils.list_files(self.__env_path, child=False)
        for service_file in service_file_list:
            name = os.path.basename(service_file).split(".").pop(0)
            arr = name.split("_")
            logging.debug(arr)


if __name__ == "__main__":
    buildHandler = BuildHandler(config_handler.ConfigHandler("template"))






