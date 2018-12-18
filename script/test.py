#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   入口函数

from handler import service_handler, config_handler, jenkins_config_handler, build_handler, running_env_handler, container_handler
from utils import file_util, cmd_util, http_util
import sys
import os
import logging
import coloredlogs

# pip install coloredlogs
coloredlogs.install(level=logging.DEBUG, fmt='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def test():
    content = "\n"
    content += "export JAVA_HOME=/opt/jdk \n"
    content += "export PATH=$JAVA_HOME/bin:$PATH \n"
    content += "export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar\n"
    path = os.path.abspath("./output/profile")
    file = open(path, "a", encoding="UTF-8")
    file.write(content)
    file.close()
    print(content)


def test_config():
    dict = {}
    dict.setdefault("name", "zc.ding")
    dict.setdefault("age", "90")
    dict.setdefault("workd", "it java")
    configHandler = config_handler.get_node_info("hkjf_master")
    configHandler.add_running_port("hkjf_master", dict)
    configHandler.update_running_port("hkjf_master", dict)


def test_file_create_time_sort():
    result = []
    file_list = file_util.list_files(os.path.abspath("./handler"), child=False)
    for f in file_list:
        t = os.path.getctime(f)
        tup = (f, t)
        result.append(tup)
    if len(result) > 0:
        result.sort(key=lambda o: o[1])
    return result


def test_log_color():
    logging.debug("this is a debugging message")
    logging.info("this is an informational message")
    logging.warning("this is a warning message")
    logging.error("this is an error message")
    logging.critical("this is a critical message")


def test_http_util():
    http_util.send_request("http://www.baidu.com", timeout=3000)


if __name__ == "__main__":
    # test_config()
    # print(os.path.getctime(os.path.abspath("./config/nginx.conf")))
    # print(test_file_create_time_sort())
    # test_log_color()
    # test_http_util()
    configHandler = config_handler.get_node_info("stroll_cxj_master")


