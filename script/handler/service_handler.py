# !/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   初始化web、services运行环境

from handler import config_handler
from utils import cmd_util, file_util, http_util
import os
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def test(sec_name):
    data = config_handler.get_node_info(sec_name)
    ServiceHandler(data, "financial").reload_nginx()

def switch(sec_name, service_name, action):
    """
    启停服务提供者、消费者
    :param sec_name: 节点名称
    :param service_name: 服务名称
    :param action: 操作: start|stop|restart
    :return: None
    """
    data = config_handler.get_node_info(sec_name)
    sh = ServiceHandler(data, service_name)
    if data.customer_list.count(service_name) > 0:
        __start_web(sh, action)
    else:
        __start_service(sh, action)


def __start_service(sh, action):
    """
    启动dubbo服务
    :param sh: ServiceHandler
    :param action: 服务节点
    :return: None
    """
    if action == "start":
        sh.start()
    elif action == "stop":
        sh.stop()
    elif action == "restart":
        sh.stop()
        time.sleep(3000)
        sh.start()


def __start_web(sh, action):
    """
    启动web项目
    :param sh: ServiceHandler
    :param action: 服务节点
    :return: None
    """
    if action == "start":
        sh.start_web()
    elif action == "stop":
        sh.stop_web()
    elif action == "restart":
        sh.stop_web()
        time.sleep(3000)
        sh.start_web()


class ServiceHandler:
    """
    服务启停脚本
    """
    def __init__(self, data, service_name):
        self.__ini_config = data
        self.__parent_path = os.path.abspath(
            self.__ini_config.container_root_path) + os.path.sep + self.__ini_config.sec_name + os.path.sep
        file_util.make_dirs(self.__parent_path)
        # self.__jre_home = self.__parent_path + "jdk/jre/bin/java"
        self.__service_name = service_name
        self.__jar_name = service_name + "-1.0-SNAPSHOT.jar"
        self.__pid = "service.pid"
        self.__service_log = "service.log"

    def start(self):
        """
        启动指定服务
        :return: None
        """
        # 创建启动节点
        self.__create_node()
        # 清理历史资源
        cmd = "cd " + self.__new_service_path + " && "
        cmd += " echo '' > " + self.__service_log + " &&"
        cmd += " echo '' > " + self.__pid + " &&"
        cmd += " rm -rf logs/*"
        cmd_util.exec_cmd(cmd)
        # 创建启动脚本
        cmd = "cd " + self.__new_service_path + " &&"
        cmd += " nohup /opt/jdk/jre/bin/java -jar"
        # 判断是否开启代理
        if self.__ini_config.agent == "1":
            cmd += " -javaagent:" + self.__new_service_path + "/agent/skywalking-agent.jar"
        # 判断是否开启了debug
        cmd += " -Xms256m -Xmx256m"
        port_list = self.__ini_config.get_service_port_list(self.__service_name, self.__new_service_path)
        if self.__ini_config.debug == "1":
            # debug端口
            cmd += " -Xdebug -Dsun.zip.disableMemoryMapping=true -Xrunjdwp:transport=dt_socket,"
            cmd += "address=" + port_list[2] + ",server=y,suspend=n"
        # 自定义dubbo协议端口号
        cmd += " -Ddubbo.protocol.port=" + port_list[1]
        cmd += " " + self.__jar_name + " >> " + self.__service_log + " 2>&1 &"
        cmd_util.exec_cmd(cmd)
        # 存储pid
        cmd = "cd " + self.__new_service_path + " && echo $! > " + self.__pid
        cmd_util.exec_cmd(cmd)
        # 启动监控，处理服务启动后续操作
        self.__start_monitor()

    def stop(self, path=""):
        """
        kill指定pid的服务
        :return: None
        """
        try:
            if path == "":
                path = self.__new_service_path
            cmd = "cd " + path + " &&"
            cmd += " kill -9 `cat " + self.__pid + "`"
            cmd_util.exec_cmd(cmd)
        except Exception:
            logging.error("stop tomcat fail. Don't care about")

    def __create_node(self):
        """
        创建服务对应的节点
        :return: None
        """
        # 创建存储运行中node的路径
        self.__nodes_path = self.__parent_path + "nodes"
        file_util.make_dirs(self.__nodes_path)
        # 判断当前运行的节点是不是备份节点
        self.__new_node_path = os.path.abspath(self.__nodes_path + "/" + self.__service_name)
        self.__old_node_path = self.__new_node_path + self.__ini_config.backup_suffix
        self.__new_service_path = self.__parent_path + self.__ini_config.get_module_name(self.__service_name)
        self.__old_service_path = self.__new_service_path + self.__ini_config.backup_suffix
        # Do you need to wait
        self.__waiting()
        if os.path.exists(self.__new_node_path) and os.path.isfile(self.__new_node_path):
            self.__old_node_path = self.__new_node_path
            self.__new_node_path += self.__ini_config.backup_suffix
            self.__old_service_path = self.__new_service_path
            self.__new_service_path += self.__ini_config.backup_suffix
        logging.info("******************************************************")
        logging.info("* new_node_path is %s.", self.__new_node_path)
        logging.info("* old_node_path is %s.", self.__old_node_path)
        logging.info("* new_service_path is %s.", self.__new_service_path)
        logging.info("* old_service_path is %s.", self.__old_service_path)
        logging.info("******************************************************")
        file_util.create_file(self.__new_node_path)

    def __waiting(self, times=1):
        """
        判断服务节点和备份节点是否都在运行，如果都在运行，等待一分钟后在校验，如果还在运行中，那么终止本次服务启动
        :param times: 等待次数，一次1分钟
        :return: None
        """
        if os.path.exists(self.__new_node_path) and os.path.isfile(self.__new_node_path) and os.path.exists(self.__old_node_path) and os.path.isfile(self.__old_node_path):
            if times > 1:
                logging.info("%s had been waiting 1 min, please restart once." % self.__service_name)
                raise Exception("%s have to wait 1 min, please restart once." % self.__service_name)
            logging.info("both %s and with _suffix is running, waiting for 1 min." % self.__service_name)
            time.sleep(60)
            times += 1
            self.__waiting(times)

    def __start_monitor(self):
        logging.debug("start dubbo service monitor...")
        flag = 'Dubbo service server started'
        count = 1
        finish = False
        logging.info("total %s times" % self.__ini_config.producer_try_times)
        while count < self.__ini_config.producer_try_times:
            logging.info("try %s times to get dubbo running status." % count)
            time.sleep(3)
            content = file_util.read_file(self.__new_service_path + os.path.sep + self.__service_log)
            if content.count(flag) > 0:
                count = self.__ini_config.producer_try_times
                finish = True
            else:
                # 休息3秒继续执行
                time.sleep(3)
                count += 1
        logging.info("******************************************************")
        logging.info("* Dubbo service status is %s.", finish)
        logging.info("******************************************************")
        if finish:
            # 删除旧的node文件
            file_util.del_path(self.__nodes_path, os.path.basename(self.__old_node_path))
            # 停止旧的服务
            self.stop(self.__old_service_path)
        else:
            # 删除新的node文件
            file_util.del_path(self.__nodes_path, os.path.basename(self.__new_node_path))
            # 停止新的服务
            self.stop(self.__new_service_path)

    def start_web(self):
        """启动web"""
        self.__create_node()
        cmd = "cd " + self.__new_service_path + "/bin/"
        cmd += " && sh startup.sh"
        cmd_util.exec_cmd(cmd)
        self.__start_web_monitor()

    def stop_web(self, path=""):
        # 停止web项目
        try:
            if path == "":
                path = self.__new_service_path
            cmd = "cd " + path + "/bin/"
            cmd += " && sh shutdown.sh"
            cmd_util.exec_cmd(cmd)
        except Exception:
            logging.info("stop tomcat fail. Don't care about")

    def __start_web_monitor(self):
        logging.debug("start web monitor...")
        count = 1
        finish = False
        logging.info("total %s times" % self.__ini_config.customer_try_times)
        while count < self.__ini_config.customer_try_times:
            logging.info("try %s times to get the tomcat running status." % count)
            time.sleep(3)
            port_list = self.__ini_config.get_tomcat_port_list(self.__service_name, self.__new_service_path)
            url = "http://localhost:" + port_list[1] + "/"
            url += self.__ini_config.get_module_name(self.__service_name) + "/index.html"
            code = http_util.send_request(url)
            if code == 200:
                count = self.__ini_config.customer_try_times
                finish = True
            else:
                # 休息3秒继续执行
                time.sleep(3)
                count += 1
        if finish:
            # 删除旧的node文件
            file_util.del_path(self.__nodes_path, os.path.basename(self.__old_node_path))
            # 重新加载nginx
            self.reload_nginx()
            # 停止旧的服务
            self.stop_web(self.__old_node_path)
        else:
            # 删除新的node文件
            file_util.del_path(self.__nodes_path, os.path.basename(self.__new_node_path))
            # 停止新的服务
            self.stop_web(self.__new_node_path)

    def reload_nginx(self):
        nginx_path = os.path.abspath("./config/nginx.conf")
        file = open(nginx_path, "r", encoding="UTF-8")
        tup = self.__get_upstream_and_location()
        content = ""
        if tup[0] == "" or tup[1] == "":
            logging.warning("can't find running tomcat")
            return
        for line in file:
            if line.count("stroll_upstream") > 0:
                content += tup[0]
            elif line.count("stroll_location") > 0:
                content += tup[1]
            else:
                content += line
        file.close()
        dst_path = os.path.abspath("/etc/nginx/nginx.conf")
        dst_file = open(dst_path, "w+", encoding="UTF-8")
        dst_file.write(content)
        dst_file.close()
        cmd_util.exec_cmd("service nginx reload")

    def __get_upstream_and_location(self):
        tup_list = []
        upstream_content = ""
        location_content = ""
        # 遍历消费(web列表)
        for c in self.__ini_config.customer_list:
            # 运行中或是启动的中node节点
            for tup in self.__get_running_nodes():
                # 若果找到最先匹配的节点就停止遍历
                if os.path.basename(tup[0]).count(c) > 0:
                    list.append((c, tup[0]))
                    break
        for t in tup_list:
            upstream_content += self.__get_upstream(t)
            location_content += self.__get_location(t)
        tup = (upstream_content, location_content)
        return tup

    def __get_upstream(self, tup):
        content = "\t\tupstream " + tup[0] + " {\n"
        port_list = self.__ini_config.get_tomcat_port_list(tup[0], tup[1])
        content += "\t\t\tserver localhost:" + port_list[1] + ";\n"
        content += "\t\t}\n"
        return content

    def __get_location(self, tup):
        service_name = self.__ini_config.get_module_name(tup[0])
        content = "\t\t\t\tlocation /" + service_name + " {\n"
        content += "\t\t\t\t\tproxy_pass http://" + tup[0] + ";\n"
        content += "\t\t\t\t\tproxy_cookie_path /" + service_name + " /;\n"
        content += "\t\t\t\t\tproxy_set_header Host $host;\n"
        content += "\t\t\t\t\tproxy_set_header X-Real-IP $remote_addr;\n"
        content += "\t\t\t\t\tproxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n"
        content += "\t\t\t\t\tproxy_redirect     off;\n"
        content += "\t\t\t\t\tproxy_read_timeout  60s;\n"
        content += "\t\t\t\t\tproxy_connect_timeout   60s;\n"
        content += "\t\t\t\t\tproxy_send_timeout   60s;\n"
        content += "\t\t\t\t\tproxy_set_header X-Forwarded-Proto https;\n"
        content += "\t\t\t\t\tproxy_intercept_errors on;\n"
        content += "\t\t\t\t\taccess_log /var/log/nginx/access.log main;\n"
        return content

    def __get_running_nodes(self):
        """
        获得运行中的节点，按节点创建时间升序， 创建时间越大，表示启动越晚，最有可能是正在启动中的节点
        :return: 含有文件路径和时间的元组组成的集合
        """
        result = []
        file_list = file_util.list_files(self.__nodes_path)
        for f in file_list:
            t = os.path.getctime(f)
            tup = (f, t)
            result.append(tup)
        if len(result) > 0:
            result.sort(key=lambda o: o[1])
        return result
