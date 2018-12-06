# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   编译jar、war

import subprocess
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def exec_cmd(cmd):
    """
    run执行系统命令
    :param cmd: 系统命令
    :return: 命令执行结果
    """
    logging.debug("execute command is " + cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug(result.stdout.decode('utf8'))
    return result.returncode


def get_result_exec_cmd(cmd):
    """
    run执行系统命令
    :param cmd: 系统命令
    :return: 命令执行结果
    """
    logging.debug("execute command is " + cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug(result.returncode)
    return result.stdout.decode('utf8')


def get_usable_port(port=1000):
    """
    判断port是否被占用，并返回可用的端口
    :param port: 端口
    :return: 未占用的端口
    """
    cmd = "netstat -nupl | grep " + str(port)
    while not get_result_exec_cmd(cmd):
        port = port + 10
        cmd = "netstat -nupl | grep " + port
    return int(port)
