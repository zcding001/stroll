#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author    :   zc.ding@foxmail.com

from xml.dom.minidom import parse
from config_parser import instance
import xml.dom.minidom as minidom
import os
import shutil


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
        self.__base_path = os.path.abspath("../config/")
        self.__job_path = self.__base_path + "job-template"
        self.__config_dom = minidom.parse(self.__base_path + "config.xml")
        self.__dom = minidom.Document()
        # 添加视图列表
        self.__add_view_list_element()
        # 添加job结构
        self.__create_jobs()

    def __add_view_list_element(self):
        """
        更新jenkins全局的config.xml配置，动态添加view及其job列表
        """
        views = self.__config_dom.getElementsByTagName("views")
        list_view = self.__create_list_view(self.__ini_config.producer_list + self.__ini_config.customer_list)
        views[0].appendChild(list_view)
        # 保存文件
        file = open(self.__base_path + "/config-new.xml", "w", encoding="UTF-8")
        # dom.writexml(file, indent='', addindent='', newl='\n', encoding='UTF-8')
        self.__config_dom.writexml(file)
        file.close()

    def __create_list_view(self, job_list):
        """
        封装list_view信息
        :param job_list: list_veiw下的job列表 
        :return: list_view的xml节点信息
        """
        list_view = self.__dom.createElement("listView")
        list_view.appendChild(self.__create_element_attrs("owner", ["class", "reference"], ["hudson", "../../.."]))
        list_view.appendChild(self.__create_element("name", "hk_master"))
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

    def __create_jobs(self):
        """
        创建job结构信息
        :return: void
        """
        for producer in self.__ini_config.producer_list:
            job_name = self.__ini_config.sec_name + "-finance-" + producer
            shutil.copytree(self.__job_path, self.__base_path + job_name, symlinks=False, ignore=None)

        for customer in self.__ini_config.customer_list:
            job_name = self.__ini_config.sec_name + "-hk-" + customer + "-services"
            shutil.copytree(self.__job_path, self.__base_path + job_name, symlinks=False, ignore=None)


if __name__ == "__main__":
    ini_config = instance("hk_master")
    JenkinsConfigParser(ini_config)
