# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   初始化web、services运行环境

from script.handler import config_handler
from script.utils import cmd_util, file_util
import os
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def build_running_env(sec_name):
    """
    初始化web、service运行环境
    :param sec_name: 节点名称
    :return: None
    """
    bre = RunningEnvHandler(config_handler.get_node_info(sec_name))
    bre.build_web_env()
    bre.build_service_env()


class RunningEnvHandler:
    """
    构建项目运行环境
    """

    def __init__(self, data):
        logging.debug("begin")
        self.__init_config = data
        self.__root_path = os.path.abspath("/data/www/" + self.__init_config.sec_name)
        self.__src_tomcat_path = "/data/www/tomcat"
        self.__src_agent_path = "/data/www/agent"
        self.__src_catalina_path = os.path.abspath("./config/catalina.sh")
        self.__src_server_path = os.path.abspath("./config/server.xml")
        self.__service_template_path = os.path.abspath("./config/service-template")
        self.__port1 = 8030
        self.__port3 = 8060

    def build_web_env(self):
        """
        初始化web项目运行环境
        :return: None
        """
        customer_list = self.__init_config.customer_list
        for o in customer_list:
            dst_path = self.__root_path + os.path.sep + self.__init_config.get_module_name(o)
            self.__copy_web_env(o, dst_path)
            self.__copy_web_env(o, dst_path + self.__init_config.backup_suffix)

    def __copy_web_env(self, name, path):
        """
        初始化tomcat配置信息：并动态配置tomcat端口、debug端口、apm的探针信息
        :param name: web项目简称
        :param path: tomcat目的路径
        :return: None
        """
        file_util.copy_path(self.__src_tomcat_path, path)
        file_util.copy_file(self.__src_server_path, path + "/conf/")
        port_list = self.__get_port_list(name, path)
        # 替换tomcat的server.xml中默认8005, 8080, 8009端口
        file_util.replace(path + "/conf/server.xml",
                          ["stroll_port1", "stroll_port2", "stroll_port3"],
                          [port_list[0], port_list[1], port_list[2]])
        file_util.copy_file(self.__src_catalina_path, path + "/bin/")
        stroll_sec_name = "stroll_sec_name"
        stroll_customer_name = "stroll_customer_name"
        stroll_debug_port = "stroll_debug_port"
        # 判断是否开启apm的监控agent探针
        self.__copy_agent_env(name, path)
        if self.__init_config.agent == "1":
            stroll_sec_name = self.__init_config.sec_name
            stroll_customer_name = self.__init_config.get_module_name(name)
        # 判断是否开启debug端口
        if self.__init_config.debug == "1":
            stroll_debug_port = port_list[3]
        # 替换代理路径、debug端口
        file_util.replace(path + "/bin/catalina.sh",
                          ["stroll_sec_name", "stroll_customer_name", "stroll_debug_port"],
                          [stroll_sec_name, stroll_customer_name, stroll_debug_port])

    def __get_port_list(self, name, path):
        """
        获取端口列表集合
        :param name: 应用名称
        :param path: tomcat路径
        :return: 端口集合
        """
        index = self.__init_config.customer_list.index(name)
        interval = index
        if path.endswith(self.__init_config.backup_suffix):
            interval = index + 100
        port1 = cmd_util.get_usable_port(self.__port1 + interval)
        port2 = cmd_util.get_usable_port(int(self.__init_config.customer_port_start) + interval)
        port3 = cmd_util.get_usable_port(self.__port3 + interval)
        debug_port = cmd_util.get_usable_port(self.__init_config.customer_debug_port_start + interval)
        return [str(port1), str(port2), str(port3), str(debug_port)]

    def build_service_env(self):
        """
        初始化服务提供者运行环境
        :return: None
        """
        producer_list = self.__init_config.producer_list
        for o in producer_list:
            dst_path = self.__root_path + os.path.sep + self.__init_config.get_module_name(o)
            self.__copy_service_env(o, dst_path)
            self.__copy_service_env(o, dst_path + self.__init_config.backup_suffix)

    def __copy_service_env(self, name, path):
        """
        初始化服务提供者配置信息
        :param name: 服务名称
        :param path: 运行路径
        :return: None
        """
        file_util.copy_path(self.__service_template_path, path)
        self.__copy_agent_env(name, path)

    def __copy_agent_env(self, name, path):
        """
        配置APM探针信息
        :param name: 服务名称
        :param path: 探针路径
        :return: None
        """
        # 判断是否开启apm的监控agent探针
        if self.__init_config.agent == "1":
            file_util.copy_path(self.__src_agent_path, path + "/agent")
            # 替换探针内配置信息
            file_util.replace(path + "/agent/config/agent.config",
                              ["Your_ApplicationName", "stroll_agent_ip"],
                              [name, self.__init_config.agent_ip])
