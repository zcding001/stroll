# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   初始化web、services运行环境

from handler import config_handler
from utils import cmd_util, file_util
import os
import logging
import coloredlogs

coloredlogs.install(level=logging.DEBUG, fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def build_running_env(sec_name):
    """
    初始化web、service运行环境
    :param sec_name: 节点名称
    :return: None
    """
    bre = RunningEnvHandler(config_handler.get_node_info(sec_name))
    bre.build_web_env()
    bre.build_service_env()
    bre.config_jdk()
    bre.config_zk()


class RunningEnvHandler:
    """
    构建项目运行环境
    """

    def __init__(self, data):
        self.__ini_config = data
        self.__parent_path = os.path.abspath(self.__ini_config.container_root_path) + os.path.sep
        self.__root_path = self.__parent_path + self.__ini_config.sec_name + os.path.sep
        self.__src_tomcat_path = self.__parent_path + "soft/tomcat"
        self.__src_agent_path = self.__parent_path + "soft/agent"
        self.__jdk_path = self.__parent_path + "soft/jdk"
        self.__zk_path = self.__parent_path + "soft/zookeeper"
        self.__service_template_path = os.path.abspath("./config/service-template")

    def build_web_env(self):
        """
        初始化web项目运行环境
        :return: None
        """
        customer_list = self.__ini_config.customer_list
        for o in customer_list:
            dst_path = self.__root_path + self.__ini_config.get_module_name(o)
            self.__copy_web_env(o, dst_path)
            self.__copy_web_env(o, dst_path + self.__ini_config.backup_suffix)

    def __copy_web_env(self, name, path):
        """
        初始化tomcat配置信息：并动态配置tomcat端口、debug端口、apm的探针信息
        :param name: web项目简称
        :param path: tomcat目的路径
        :return: None
        """
        file_util.copy_path(self.__src_tomcat_path, path)
        port_list = self.__ini_config.get_tomcat_port_list(name, path)
        # 替换tomcat的server.xml中默认8005, 8080, 8009端口
        file_util.replace(path + "/conf/server.xml",
                          ["stroll_port1", "stroll_port2", "stroll_port3"],
                          [port_list[0], port_list[1], port_list[2]])
        stroll_sec_name = "stroll_sec_name"
        stroll_customer_name = "stroll_customer_name"
        stroll_debug_port = "stroll_debug_port"
        # 判断是否开启apm的监控agent探针
        self.__copy_agent_env(name, path)
        if self.__ini_config.agent == "1":
            stroll_sec_name = self.__ini_config.sec_name
            stroll_customer_name = self.__ini_config.get_module_name(name)
        # 判断是否开启debug端口
        if self.__ini_config.debug == "1":
            stroll_debug_port = port_list[3]
        # 替换代理路径、debug端口
        file_util.replace(path + "/bin/catalina.sh",
                          ["stroll_sec_name", "stroll_customer_name", "stroll_debug_port"],
                          [stroll_sec_name, stroll_customer_name, stroll_debug_port])

    def build_service_env(self):
        """
        初始化服务提供者运行环境
        :return: None
        """
        producer_list = self.__ini_config.producer_list
        for o in producer_list:
            dst_path = self.__root_path + self.__ini_config.get_module_name(o)
            self.__copy_service_env(o, dst_path)
            self.__copy_service_env(o, dst_path + self.__ini_config.backup_suffix)

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
        if self.__ini_config.agent == "1":
            file_util.copy_path(self.__src_agent_path, path + "/agent")
            # 替换探针内配置信息
            file_util.replace(path + "/agent/config/agent.config",
                              ["Your_ApplicationName", "stroll_agent_ip"],
                              [name, self.__ini_config.agent_ip])

    def config_jdk(self):
        """
        配置jdk及环境及环境变量
        :return: None
        """
        content = "\n"
        content += "export JAVA_HOME=/opt/jdk \n"
        content += "export PATH=$JAVA_HOME/bin:$PATH \n"
        content += "export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar\n"
        file_util.append_file("/etc/profile", content)
        cmd = "cp -rf " + self.__jdk_path + " /opt/"
        cmd += " && source /etc/profile"
        cmd_util.exec_cmd(cmd)

    def config_zk(self):
        """
        配置并启动zookeeper
        :return: None
        """
        cmd = "cp -rf " + self.__zk_path + " /opt/"
        cmd += " && source /etc/profile"
        cmd += " && cd /opt/zookeeper/bin && bash ./zkServer.sh restart"
        cmd_util.exec_cmd(cmd)
