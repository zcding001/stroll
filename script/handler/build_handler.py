# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   编译jar、war

from handler import config_handler
from utils import cmd_util, file_util
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def build_project(sec_name, service_name=""):
    """
    构建jar、war并将war、jar拷贝到config.ini中指定的配置路径下
    :param sec_name: config.ini中节点名称
    :param service_name: customer_list或是producer_list中值，可以为空
    :return: None
    """
    build_handler = BuildHandler(config_handler.ConfigHandler(sec_name))
    build_handler._git_pull()
    build_handler._copy_properties()
    build_handler._build_project(service_name)


class BuildHandler:
    """
    构建war、jar等资源
    """
    def __init__(self, data):
        self.__ini_config = data
        self.__env_path = os.path.abspath(self.__ini_config.env_path)
        self.__common_env_path = self.__ini_config.src_path + os.path.sep + "env"
        self.__service_path = self.__ini_config.src_path + "/fiance-#/finance-#-services/src/main/resources/env"
        self.__mvn_cmd = "cd " + self.__ini_config.src_path + " && " + self.__ini_config.mvn_path
        self.__mvn_cmd += " clean package -pl # -am resources:resources -Dmaven.test.skip=true -Penv-test"

    def _git_pull(self):
        """
        拉取最新代码
        :return: None
        """
        cmd = "cd " + self.__ini_config.src_path + " && git checkout . && git checkout " + self.__ini_config.branch_name + " && git pull"
        if cmd_util.exec_cmd(cmd) != 0:
            raise Exception("command " + cmd + " execute fail. can't pull ")

    def _copy_properties(self):
        """
        复制编译需要的资源文件
        :return: None
        """
        # 复制公共资源
        common_file_list = file_util.list_files(self.__env_path, root_name="common")
        logging.debug("copy common resources")
        for common_file in common_file_list:
            file_util.copy_file(common_file, os.path.abspath(self.__common_env_path))

        # 复制服务的properties到对应资源路径
        service_file_list = file_util.list_files(self.__env_path, child=False)
        logging.debug("copy service resources")
        for service_file in service_file_list:
            name = str(os.path.basename(service_file).split(".").pop(0))[4:]
            dst_path = os.path.abspath(self.__ini_config.get_service_resources_path(name))
            file_util.del_path(dst_path)
            file_util.copy_file(service_file, dst_path)

        # 复制web资源
        web_file_list = file_util.list_files(self.__env_path, root_name="web-conf")
        logging.debug("copy web resources")
        for web_file in web_file_list:
            name = os.path.basename(file_util.get_parent_path(web_file))
            dst_path = os.path.abspath(self.__ini_config.get_web_resources_path(name))
            file_util.del_path(dst_path)
            file_util.copy_file(web_file, dst_path)

    def _build_project(self, service_name=""):
        """
        构建jar、war并把资源放到指定路径
        :param service_name: 指定服务名称
        :return: None
        """
        cmd = self.__mvn_cmd.replace("#", self.__ini_config.get_module_name(service_name))
        if cmd_util.exec_cmd(cmd) != 0:
            raise Exception("command " + cmd + " execute fail.")
        # 复制构建后的资源
        for f in self.__ini_config.producer_list + self.__ini_config.customer_list:
            flag = False
            if service_name and service_name == f:
                flag = True
            elif not service_name:
                flag = True
            if flag:
                src_path = self.__ini_config.get_copy_src_path(f)
                dst_path = self.__ini_config.get_copy_dst_path(f)
                file_util.copy_file(src_path, dst_path)
                if str(src_path).endswith(".jar"):
                    src_lib_path = file_util.get_parent_path(src_path) + "/lib"
                    dst_lib_path = file_util.get_parent_path(dst_path) + "/lib"
                    file_util.copy_path(src_lib_path, dst_lib_path, remove=True)
