#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   入口函数

from handler import service_handler, config_handler, jenkins_config_handler, build_handler, running_env_handler
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def show_usage():
    print("***************************************************************")
    print("**")
    print("** usage: python3 main.py [option] [sec_name] [service_name] [action]")
    print("**")
    print("**\t option: [required]")
    print("**\t \t 1: config jenkins")
    print("**\t \t 2: build running env for war or jar")
    print("**\t \t 3: build project for creating war or jar resources")
    print("**\t \t 4: change the customer or producer service status")
    print("**")
    print("**\t sec_name : [required]")
    print("**\t \t config.ini node")
    print("**")
    print("**\t service_name : [required when option is {2, 4}]")
    print("**\t \t in config.ini file, the customer_list or producer_list's children elements")
    print("**")
    print("**\t action : [required when option is {4}]")
    print("**\t \t customer or producer service action. {start|restart|stop}")
    print("***************************************************************")


class Main:

    def __init__(self):
        size = len(sys.argv)
        if size < 3:
            show_usage()
            raise Exception("Please confirm the number of parameters.")
        self.__option = sys.argv[1]
        self.__sec_name = sys.argv[2]
        logging.info("option is %s" % self.__option)
        logging.info("sec_name is %s" % self.__sec_name)

    def switch(self):
        if self.__option == "1":
            # 配置jenkins
            logging.info("config jenkins...")
            jenkins_config_handler.add_view_and_jobs(self.__sec_name)
        elif self.__option == "2":
            # 构建war、jar运行环境
            logging.info("build running env...")
            # running_env_handler.build_running_env(self.__sec_name)
        elif self.__option == "3":
            # 构建war、jar
            if size < 4:
                show_usage()
                raise Exception("Please confirm the number of parameters.")
            logging.info("build war jar resources")
            logging.info("sec_name is %s" % sys.argv[3])
            # build_handler.build_project(self.__sec_name, sys.argv[3])
        elif self.__option == "4":
            # 启停服务
            if size != 5:
                show_usage()
                raise Exception("Please confirm the number of parameters.")
            logging.info("change server status")
            logging.info("sec_name is %s" % sys.argv[3])
            logging.info("action is %s" % sys.argv[4])
            # service_handler.switch(self.__sec_name, sys.argv[3], sys.argv[4])


if __name__ == "__main__":
    size = len(sys.argv)
    if size < 3:
        show_usage()
        raise Exception("Please confirm the number of parameters.")
    Main().switch()
