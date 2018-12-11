# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   编译jar、war

import subprocess
import logging
import platform

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def exec_cmd(cmd):
    """
    run执行系统命令
    :param cmd: 系统命令
    :return: 命令执行结果
    """
    logging.info("execute command is [%s]" % cmd)
    if 'Window' in platform.system():
        return 0
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug(result.stdout.decode('utf8'))
    return result.returncode


def get_result_exec_cmd(cmd):
    logging.info("execute command is [%s]" % cmd)
    """
    run执行系统命令
    :param cmd: 系统命令
    :return: 命令执行结果
    """
    if 'Window' in platform.system():
        return ""
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    logging.debug(result.returncode)
    return result.stdout.decode('utf8')


def get_usable_port(port=1000):
    """
    判断port是否被占用，并返回可用的端口
    :param port: 端口
    :return: 未占用的端口
    """
    if 'Window' in platform.system():
        return port
    cmd = "netstat -ano | grep " + str(port)
    while get_result_exec_cmd(cmd):
        logging.warning("the port is already in use [%s]" % str(port))
        port = port + 10
        cmd = "netstat -ano | grep " + port
    return int(port)

