from handler import config_handler
from utils import cmd_util, file_util
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def run_container(sec_name):
    """
    启动容器
    :param sec_name: 容器名称 
    :return: None
    """
    data = config_handler.get_node_info(sec_name)
    cmd = "docker run -d"
    cmd += " -p " + data.proxy_tomcat_port + ":8080"
    cmd += " -p " + data.proxy_zk_port + ":2181"
    cmd += " -p " + data.proxy_ssh_port + ":22"
    cmd += " -it -P"
    cmd += " -v " + data.local_share_path + ":/data/www"
    cmd += " --name='" + data.sec_name + "' stroll:v1 /sbin/my_init"
    cmd_util.exec_cmd(cmd)


def del_container(sec_name):
    """
    删除容器
    :param sec_name: 容器名称
    :return: None
    """
    cmd_util.exec_cmd("docker stop " + sec_name + " && docker rm " + sec_name)
