# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   编译jar、war

from script.handler import config_handler
from script.utils import cmd_util, file_util
import os
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


class BuildRunningEnv:
    """
    构建项目运行环境
    """

    def __init(self, data):
        logging.debug("begin")
        self.__init_config = data
        self.__root_path = os.path.abspath("/data/www/" + self.__init_config.sec_name)
        self.__tomcat_path = "/data/www/tomcat"
        self.__src_catalina_path = os.path.abspath("./config/catalina.sh")
        self.__src_server_path = os.path.abspath("./config/server.xml")

    def __build_web_env(self):
        customer_list = self.__init_config.customer_list
        for c in customer_list:
            dst_path = self.__root_path + os.path.sep + self.__init_config.get_module_name(c)
            file_util.copy_path(self.__tomcat_path, dst_path)
            file_util.copy_file(self.__src_catalina_path, dst_path + "/bin/")
            file_util.copy_file(self.__src_catalina_path, dst_path + "/conf/")
            backup_dst_path = dst_path + self.__init_config.backup_suffix
            file_util.copy_path(self.__tomcat_path, backup_dst_path)
            file_util.copy_file(self.__src_catalina_path, backup_dst_path + "/bin/")
            file_util.copy_file(self.__src_catalina_path, backup_dst_path + "/conf/")


    def __build_agent(self):
        logging.debug("")
