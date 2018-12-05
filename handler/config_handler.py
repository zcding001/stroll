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
        dst_path : 资源目标路径
        mvn_path : mvn soft path
    """

    __default_options = {"producer_prefix": "finance-",
                         "producer_suffix": "-service",
                         "customer_prefix": "hk-",
                         "customer_suffix": "-services",
                         "version": "-1.0-SNAPSHOT",
                         "proxy_ssh_port": "22"}

    def __init__(self, sec_name):
        config_ini_path = os.path.abspath("./config/config.ini")
        self.__config = configparser.ConfigParser()
        self.__config.read(config_ini_path)
        # 节点不在直接抛出异常
        if sec_name not in self.__config.sections():
            raise Exception("node %s no exit" % sec_name)
        # 加载全局配置
        self.dst_path = os.path.abspath(self.__config.get("global", "dst_path"))
        self.mvn_path = self.__config.get("global", "mvn_path")
        self.ln_log_dst_path = self.__config.get("global", "ln_log_dst_path")
        logging.debug("*****global config info*************************")
        logging.debug("*dst_path=%s, mvn_path=%s, ln_log_dst_path=%s" % (self.dst_path, self.mvn_path, self.ln_log_dst_path))
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
        self.env_path = os.path.abspath(self.__config.get(sec_name, "env_path"))
        self.producer_list = self.__config.get(sec_name, "producer_list").split(",")
        self.customer_list = self.__config.get(sec_name, "customer_list").split(",")
        self.customer_port_list = self.__config.get(sec_name, "customer_port_list").split(",")
        self.proxy_tomcat_port = self.__config.get(sec_name, "proxy_tomcat_port")
        self.proxy_ssh_port = self.__config.get(sec_name, "proxy_ssh_port", vars=self.__default_options)
        self.branch_name = self.__config.get(sec_name, "branch_name", vars=self.__default_options)
        if not self.branch_name:
            self.branch_name = "master"
        self.backup_suffix = self.__config.get(sec_name, "backup_suffix", vars=self.__default_options)
        if not self.backup_suffix:
            self.backup_suffix = "_backup"
        self.producer_prefix = self.__config.get(sec_name, "producer_prefix", vars=self.__default_options)
        if not self.producer_prefix:
            self.backup_suffix = "finance-"
        self.producer_suffix = self.__config.get(sec_name, "producer_suffix", vars=self.__default_options)
        if not self.producer_suffix:
            self.producer_suffix = "-service"
        self.customer_prefix = self.__config.get(sec_name, "customer_prefix", vars=self.__default_options)
        if not self.customer_prefix:
            self.customer_prefix = "hk-"
        self.customer_suffix = self.__config.get(sec_name, "customer_suffix", vars=self.__default_options)
        if not self.customer_suffix:
            self.customer_suffix = "-services"
        self.version = self.__config.get(sec_name, "version", vars=self.__default_options)
        if not self.version:
            self.version = "-1.0-SNAPSHOT"
        logging.debug("*****node config info***************************")
        logging.debug("*src_path=%s, env_path=%s, producer_list=%s, customer_list=%s, "
                      "customer_port_list=%s, branch_name=%s, proxy_tomcat_port=%s, backup_suffix=%s"
                        % (self.src_path, self.env_path, self.producer_list, self.customer_list,
                         self.customer_port_list, self.branch_name, self.proxy_tomcat_port, self.backup_suffix))
        logging.debug("*****node config info***************************")

    def get_module_name(self, service_name):
        """
        获取服务模块名称
        :param service_name: 服务简称
        :return: 服务名称
        """
        if self.producer_list.count(service_name):
            return "finance-" + service_name
        return "hk-" + service_name + "-services"

    def get_pom_path(self, service_name):
        """
        获取服务对应的pom文件
        :param service_name: 服务简称
        :return: pom.xml绝对路径
        """
        if not service_name:
            return self.src_path + "/pom.xml"
        if self.producer_list.count(service_name):
            return self.src_path + "/finance-" + service_name + "/pom.xml"
        return self.src_path + "/hk-" + service_name + "-services/pom.xml"

    def get_copy_src_path(self, service_name):
        """
        获取指定服务jar、war绝对路径
        :param service_name: 服务简称
        :return: jar、war路径
        """
        if self.producer_list.count(service_name):
            return self.src_path + "/finance-" + service_name + "/finance-" + service_name + "-service/target/" + service_name + "-1.0-SNAPSHOT.jar"
        return self.src_path + "/hk-" + service_name + "-services/target/hk-" + service_name + "-services.war"

    def get_copy_dst_path(self, service_name):
        """
        获取指定服务目标路径
        :param service_name: 服务简称 
        :return: 路径
        """
        if self.producer_list.count(service_name):
            return self.dst_path + "/finance-" + service_name + "-service/" + service_name + ".jar"
        return self.src_path + "/hk-" + service_name + "-services/webapps/" + service_name + ".war"

    def get_common_resources_path(self):
        """
        获取源码项目公共资源路径
        :return: 资源绝对路径
        """
        return self.src_path + os.path.sep + "env"

    def get_service_resources_path(self, service_name):
        """
        获取指定服务源码项目的资源路径
        :param service_name: 服务名称
        :return: 资源绝对路径
        """
        return str(self.src_path + "/fiance-#/finance-#-services/src/main/resources/env").replace("#", service_name)

    def get_web_resources_path(self, service_name):
        """
        获取指定web服务源码项目的资源路径
        :param service_name: 服务名称
        :return: 资源绝对路径
        """
        return str(self.src_path + "/hk-#-services/src/main/resources/env").replace("#", service_name)
