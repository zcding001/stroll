#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com
# desc      :   动态添加|删除jenkins的view和job

from handler import config_handler
from utils import file_util
import xml.etree.ElementTree as elementTree
import xml.dom.minidom as mini_dom
import os
import shutil
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')


def add_view_and_jobs(sec_name):
    """
    添加jenkins的view和job
    :param sec_name: config.ini中节点名称
    :return: None
    """
    jcp = JenkinsConfigParser(config_handler.get_node_info(sec_name))
    jcp._add_view_list_element()
    jcp._add_jobs()


def del_view_and_jobs(sec_name):
    """
    删除jenkins的view和job
    :param sec_name: config.ini中节点名称
    :return: Nonw
    """
    jcp = JenkinsConfigParser(config_handler.get_node_info(sec_name))
    jcp._del_view_list_element()
    jcp._del_jobs()


class JenkinsConfigParser:
    """
    通过config.ini的节点信息，动态创建jenkins的view和job列表
    """
    def __init__(self, data):
        """
        初始化类
        :param data: config.ini中节点信息
        """
        self.__ini_config = data
        self.__job_template_path = os.path.abspath("./config/job_template")
        # jenkins全局配置文件绝对路径
        self.__config_dom = mini_dom.parse(self.__ini_config.config_xml_path)
        self.__dom = mini_dom.Document()

    def _add_view_list_element(self):
        """
        更新jenkins全局的config.xml配置，动态添加view及其job列表
        """
        views = self.__config_dom.getElementsByTagName("views")
        list_view = self.__create_list_view(self.__ini_config.producer_list + self.__ini_config.customer_list)
        views[0].appendChild(list_view)
        # 保存文件
        file = open(self.__ini_config.config_xml_path, "w", encoding="UTF-8")
        # dom.writexml(file, indent='', addindent='', newl='\n', encoding='UTF-8')
        self.__config_dom.writexml(file)
        file.close()

    def _del_view_list_element(self):
        """
        删除指定sec_name的view视图
        :return: None
        """
        tree = elementTree.parse(self.__ini_config.config_xml_path)
        views = tree.find("views")
        for node in tree.iter("listView"):
            e = node.find('name')
            if e.text == self.__ini_config.sec_name:
                views.remove(node)
        tree.write(self.__ini_config.config_xml_path, encoding="UTF-8")

    def _add_jobs(self):
        """
        创建job结构信息
        :return: None
        """
        for obj in (self.__ini_config.producer_list + self.__ini_config.customer_list):
            job_abs_dst_path = self.__ini_config.job_dst_path + os.path.sep + self.__get_job_name(obj)
            shutil.copytree(self.__job_template_path, job_abs_dst_path, symlinks=False, ignore=None)
            file_util.replace(job_abs_dst_path + os.path.sep + "config.xml",
                              ["stroll_node", "stroll_service"],
                              [self.__ini_config.sec_name, obj])

    def _del_jobs(self):
        """
        删除job列表信息
        :return: None
        """
        for obj in (self.__ini_config.producer_list + self.__ini_config.customer_list):
            job_abs_dst_path = self.__ini_config.job_dst_path + os.path.sep + self.__get_job_name(obj)
            shutil.rmtree(job_abs_dst_path)
            logging.debug("del job config: " + job_abs_dst_path)

    def __create_list_view(self, job_list):
        """
        封装list_view信息
        :param job_list: list_veiw下的job列表 
        :return: list_view的xml节点信息
        """
        list_view = self.__dom.createElement("listView")
        list_view.appendChild(self.__create_element_attrs("owner", ["class", "reference"], ["hudson", "../../.."]))
        list_view.appendChild(self.__create_element("name", self.__ini_config.sec_name))
        list_view.appendChild(self.__create_element("filterExecutors", "false"))
        list_view.appendChild(self.__create_element("filterQueue", "false"))
        list_view.appendChild(self.__create_element_attrs("properties", ["class"], ["hudson.model.View$PropertyList"]))

        # 创建jobNames
        job_names = self.__dom.createElement("jobNames")
        job_names.appendChild(self.__create_element_attrs("comparator", ["class"],
                                                          ["hudson.util.CaseInsensitiveComparator"]))
        for job_name in job_list:
            job_names.appendChild(self.__create_element("string", job_name))
        list_view.appendChild(job_names)

        # 创建jobFilters
        list_view.appendChild(self.__dom.createElement("jobFilters"))

        # 创建columns
        columns = self.__dom.createElement("columns")
        columns.appendChild(self.__dom.createElement("hudson.views.StatusColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.WeatherColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.JobColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.LastSuccessColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.LastFailureColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.LastDurationColumn"))
        columns.appendChild(self.__dom.createElement("hudson.views.BuildButtonColumn"))
        list_view.appendChild(columns)

        # 创建recurse
        list_view.appendChild(self.__create_element("recurse", "false"))
        return list_view

    def __create_element_attrs(self, name, attr_names, attr_values):
        """
        创建含有attribute属性的xml节点 eg:<view class="com.View" target="_blank" />
        :param name: 节点名称
        :param attr_names: 节点属性的name集合
        :param attr_values: 节点属性的value集合
        :return: 节点信息
        """
        e = self.__dom.createElement(name)
        for attr in attr_names:
            index = attr_names.index(attr)
            e.setAttribute(attr, attr_values[index])
        return e

    def __create_element(self, name, value):
        """
        创建节点的节点信息 eg ：<string>hello</string>
        :param name: 节点名称
        :param value: 节点文本信息
        :return: 节点信息
        """
        e = self.__dom.createElement(name)
        value = self.__dom.createTextNode(value)
        e.appendChild(value)
        return e

    def __get_job_name(self, obj):
        """
        获得job文件夹名称，web的job前缀hk-, 服务job前缀finance
        :param obj: producer和customer中元素
        :return: job_name
        """
        job_name = self.__ini_config.sec_name + "-finance-" + obj
        if self.__ini_config.customer_list.count(obj) > 0:
            job_name = self.__ini_config.sec_name + "-hk-" + obj + "-services"
        return job_name


if __name__ == "__main__":
    add_view_and_jobs("template")
    # del_view_and_jobs("template")
