#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   入口函数

from handler import config_handler as config_handler
import handler.jenkins_config_handler as jenkins_config_handler
import handler.build_handler as build_handler

test_sec_name = "template"


def __test_config_handler():
    config_handler.get_node_info(test_sec_name)


def __test_jenkins_config_handler():
    jenkins_config_handler.add_view_and_jobs(test_sec_name)


def __test_build_handler():
    build_handler.build_project(test_sec_name, "user")


if __name__ == "__main__":
    __test_config_handler()
