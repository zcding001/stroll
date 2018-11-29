# -*- coding: UTF-8 -*-
# !/usr/bin/python3
import configparser
import os


class ConfigParser:
    __config = configparser.ConfigParser()
    # global config
    config_path = ""
    mvn_path = ""
    ln_log_dst_path = ""

    # nodes config
    src_path = ""
    dst_path = ""
    env_path = ""
    # user,loan,payment,invest,secondary
    producer_list = set()
    # management,financial,api,bi
    customer_list = set()
    # 8080,8081,8082,8083
    customer_port_list = set()
    branch_name = "mater"
    proxy_port = ""
    backup_suffix = "_backup"

    def __init__(self, sec_name):
        config_ini_path = os.path.abspath("../config") + "/config.ini"
        self.__config.read(config_ini_path)
        # 判断节点是否存在
        if sec_name not in self.__config.sections():
            raise Exception("node %s no exit" % sec_name)
        # 加载全局配置
        config_path = self.__config.get("global", "config_path")
        mvn_path = self.__config.get("global", "mvn_path")
        ln_log_dst_path = self.__config.get("global", "ln_log_dst_path")
        print("*****global config info*******")
        print("config_path=%s, mvn_path=%s, ln_log_dst_path=%s" % (config_path, mvn_path, ln_log_dst_path))
        self.__get_config(sec_name)

    def __get_config(self, sec_name):
        src_path = self.__config.get(sec_name, "src_path")
        dst_path = self.__config.get(sec_name, "dst_path")
        env_path = self.__config.get(sec_name, "env_path")
        producer_list = self.__config.get(sec_name, "producer_list").split(",")
        customer_list = self.__config.get(sec_name, "customer_list").split(",")
        customer_port_list = self.__config.get(sec_name, "customer_port_list").split(",")
        branch_name = self.__config.get(sec_name, "branch_name")
        proxy_port = self.__config.get(sec_name, "proxy_port")
        backup_suffix = self.__config.get(sec_name, "backup_suffix")
        print("*****node config info******")
        print("src_path=%s, dst_path=%s, env_path=%s, producer_list=%s, customer_list=%s, "
              "customer_port_list=%s, branch_name=%s, proxy_port=%s, backup_suffix=%s"
              % (src_path, dst_path, env_path, producer_list, customer_list,
                 customer_port_list, branch_name, proxy_port, backup_suffix))


def load_config():
    ConfigParser("hk_master")
