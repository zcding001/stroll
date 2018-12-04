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
