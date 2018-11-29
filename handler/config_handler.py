# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com

import configparser
import os
import logging
logging.basicConfig(level=logging.INFO)


def get_node_info(sec_name):
    """
    加载节点配置信息
    :param sec_name: 节点名称
    :return: 节点所有属性信息 ConfigHandler
    """
    return ConfigHandler(sec_name)


class ConfigHandler:
    """loading config.ini info
    Attributes :
        config_path : config.ini根路径
        mvn_path : mvn soft path
    """

    def __init__(self, sec_name):
        config_ini_path = os.path.abspath("../config") + "/config.ini"
        self.__config = configparser.ConfigParser()
        self.__config.read(config_ini_path)
        # 节点不在直接抛出异常
        if sec_name not in self.__config.sections():
            raise Exception("node %s no exit" % sec_name)
        # 加载全局配置
        config_path = self.__config.get("global", "config_path")
        mvn_path = self.__config.get("global", "mvn_path")
        ln_log_dst_path = self.__config.get("global", "ln_log_dst_path")
        logging.info("*****global config info*************************")
        logging.info("*config_path=%s, mvn_path=%s, ln_log_dst_path=%s" % (config_path, mvn_path, ln_log_dst_path))
        logging.info("*****global config info*************************")
        # 加载jenkins配置
        config_xml_path = self.__config.get("jenkins", "config_xml_path")
        job_path = self.__config.get("jenkins", "job_path")
        logging.info("*****jenkins config info************************")
        logging.info("*config_xml_path=%s, job_path=%s" % (config_xml_path, job_path))
        logging.info("*****jenkins config info************************")
        self.__get_config(sec_name)

    def __get_config(self, sec_name):
        """
        加载指定sec_name节点信息
        :param sec_name: 节点名称
        """
        self.sec_name = sec_name
        self.src_path = self.__config.get(sec_name, "src_path")
        self.dst_path = self.__config.get(sec_name, "dst_path")
        self.env_path = self.__config.get(sec_name, "env_path")
        self.producer_list = self.__config.get(sec_name, "producer_list").split(",")
        self.customer_list = self.__config.get(sec_name, "customer_list").split(",")
        self.customer_port_list = self.__config.get(sec_name, "customer_port_list").split(",")
        self.branch_name = self.__config.get(sec_name, "branch_name")
        self.proxy_port = self.__config.get(sec_name, "proxy_port")
        self.backup_suffix = self.__config.get(sec_name, "backup_suffix")
        logging.info("*****node config info***************************")
        logging.info("*src_path=%s, dst_path=%s, env_path=%s, producer_list=%s, customer_list=%s, "
                     "customer_port_list=%s, branch_name=%s, proxy_port=%s, backup_suffix=%s"
                     % (self.src_path, self.dst_path, self.env_path, self.producer_list, self.customer_list,
                        self.customer_port_list, self.branch_name, self.proxy_port, self.backup_suffix))
        logging.info("*****node config info***************************")
