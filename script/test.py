#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   入口函数

from handler import service_handler, config_handler, jenkins_config_handler, build_handler, running_env_handler, container_handler
from utils import file_util, cmd_util, http_util
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


if __name__ == "__main__":
    content = "\n"
    content += "export JAVA_HOME=/opt/jdk \n"
    content += "export PATH=$JAVA_HOME/bin:$PATH \n"
    content += "export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar\n"
    path = os.path.abspath("./output/profile")
    file = open(path, "a", encoding="UTF-8")
    file.write(content)
    file.close()
    print(content)
