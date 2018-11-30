# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   加载config.ini配置你信息

import configparser
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


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
        config_ini_path = os.path.abspath("../config/config.ini")
        self.__config = configparser.ConfigParser()
        self.__config.read(config_ini_path)
        # 节点不在直接抛出异常
        if sec_name not in self.__config.sections():
            raise Exception("node %s no exit" % sec_name)
        # 加载全局配置
        self.config_path = self.__config.get("global", "config_path")
        self.mvn_path = self.__config.get("global", "mvn_path")
        self.ln_log_dst_path = self.__config.get("global", "ln_log_dst_path")
        logging.debug("*****global config info*************************")
        logging.debug("*config_path=%s, mvn_path=%s, ln_log_dst_path=%s" % (self.config_path, self.mvn_path, self.ln_log_dst_path))
        logging.debug("*****global config info*************************")
        # 加载jenkins配置
        self.config_xml_path = os.path.abspath(self.__config.get("jenkins", "config_xml_path"))
        self.job_dst_path = os.path.abspath(self.__config.get("jenkins", "job_dst_path"))
        logging.debug("*****jenkins config info************************")
        logging.debug("*config_xml_path=%s, job_path=%s" % (self.config_xml_path, self.job_dst_path))
        logging.debug("*****jenkins config info************************")
        self.__get_config(sec_name)

    def __get_config(self, sec_name):
        """
        加载指定sec_name节点信息
        :param sec_name: 节点名称
        """
        self.sec_name = sec_name
        self.src_path = os.path.abspath(self.__config.get(sec_name, "src_path"))
        self.dst_path = os.path.abspath(self.__config.get(sec_name, "dst_path"))
        self.env_path = os.path.abspath(self.__config.get(sec_name, "env_path"))
        self.producer_list = self.__config.get(sec_name, "producer_list").split(",")
        self.customer_list = self.__config.get(sec_name, "customer_list").split(",")
        self.customer_port_list = self.__config.get(sec_name, "customer_port_list").split(",")
        self.branch_name = self.__config.get(sec_name, "branch_name")
        self.proxy_port = self.__config.get(sec_name, "proxy_port")
        self.backup_suffix = self.__config.get(sec_name, "backup_suffix")
        logging.debug("*****node config info***************************")
        logging.debug("*src_path=%s, dst_path=%s, env_path=%s, producer_list=%s, customer_list=%s, "
                      "customer_port_list=%s, branch_name=%s, proxy_port=%s, backup_suffix=%s"
                        % (self.src_path, self.dst_path, self.env_path, self.producer_list, self.customer_list,
                         self.customer_port_list, self.branch_name, self.proxy_port, self.backup_suffix))
        logging.debug("*****node config info***************************")


if __name__ == "__main__":
    get_node_info("template")