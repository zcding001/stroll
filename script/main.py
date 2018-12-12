#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   入口函数

from handler import service_handler, config_handler, jenkins_config_handler, build_handler, running_env_handler, container_handler
from exception.param_exception import ParamException
from exception.fail_exception import FailException
import sys
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def show_usage():
    print("***************************************************************")
    print("**")
    print("** usage: python3 main.py [option] [sec_name] [optional...]")
    print("**")
    print("**\t option: [required]")
    print("**\t \t jenkins: config jenkins")
    print("**\t \t \t sec_name: required")
    print("**\t \t \t action: {add | del} optional, default add")
    print("**\t \t \t eg: python3 main.py jenkins template")
    print("**")
    print("**\t \t docker: run docker container")
    print("**\t \t \t sec_name: required")
    print("**\t \t \t action: {add | del} optional, default add")
    print("**\t \t \t eg: python3 main.py docker template del")
    print("**")
    print("**\t \t env: build running env for war or jar")
    print("**\t \t \t sec_name: required")
    print("**\t \t \t eg: python3 main.py env template")
    print("**")
    print("**\t \t build: build project for creating war or jar resources")
    print("**\t \t \t sec_name: required")
    print("**\t \t \t service_name: empty string allowed, but must be exist.")
    print("**\t \t \t eg: python3 main.py env template user")
    print("**")
    print("**\t \t run: change the customer or producer service status")
    print("**\t \t \t sec_name: required")
    print("**\t \t \t service_name: empty string allowed, but must be exist.")
    print("**\t \t \t action: {start|restart|stop} optional, default start")
    print("**\t \t \t eg: python3 main.py run template user start")
    print("**")
    print("***************************************************************")


class Main:

    def __init__(self):
        self.__size = len(sys.argv)
        if self.__size < 3:
            show_usage()
            raise ParamException("please confirm the number of parameters.")
        self.__option = sys.argv[1]
        self.__sec_name = sys.argv[2]
        logging.info("option is %s" % self.__option)
        logging.info("sec_name is %s" % self.__sec_name)

    def switch(self):
        if self.__option == "jenkins":
            # 配置jenkins
            logging.info("config jenkins...")
            action = "add"
            if self.__size > 3:
                action = sys.argv[3]
            if action == "add":
                jenkins_config_handler.add_view_and_jobs(self.__sec_name)
            elif action == "del":
                jenkins_config_handler.del_view_and_jobs(self.__sec_name)
            else:
                raise Exception("please confirm parameters.")
        elif self.__option == "docker":
            # 构建容器
            logging.info("run container...")
            action = "add"
            if self.__size > 3:
                action = sys.argv[3]
            if action == "add":
                container_handler.run_container(self.__sec_name)
            elif action == "del":
                container_handler.run_container(self.__sec_name)
            else:
                raise Exception("please confirm parameters.")
        elif self.__option == "env":
            # 构建war、jar运行环境
            logging.info("build running env...")
            running_env_handler.build_running_env(self.__sec_name)
        elif self.__option == "build":
            # 构建war、jar
            logging.info("build war jar resources")
            service_name = ""
            if self.__size > 3:
                service_name = sys.argv[3]
            logging.debug("service is [%s]", service_name)
            build_handler.build_project(self.__sec_name, service_name)
        elif self.__option == "run":
            # 启停服务
            logging.info("change service status")
            action = "start"
            if self.__size < 4:
                show_usage()
                raise Exception("please confirm parameters.")
            if self.__size > 4:
                action = sys.argv[4]
            if action != "start" and action != "stop" and action != "restart":
                raise Exception("please confirm parameters.")
            logging.debug("service_name is [%s]" % sys.argv[3])
            logging.info("debug is [%s]", action)
            service_handler.switch(self.__sec_name, sys.argv[3], action)


if __name__ == "__main__":
    try:
        Main().switch()
    except ParamException as paramException:
        print(sys.argv)
        print(paramException)
        time.sleep(3)
        raise paramException
