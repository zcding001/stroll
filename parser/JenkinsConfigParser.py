#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom as minidom
import os
from ConfigParser import ConfigParser

class JenkinsConfigParser:

    def __init__(self):
        self.__base_path = os.path.abspath("../config")
        self.__config_dom = minidom.parse(self.__base_path + "/config.xml")
        self.__dom = minidom.Document()
        self.__add_element()

    def __add_element(self):
        views = self.__config_dom.getElementsByTagName("views")
        producer_list = ["user"]
        customer_list = ["api"]
        list_view = self.__create_list_view(producer_list + customer_list)
        views[0].appendChild(list_view)
        # 保存文件
        file = open(self.__base_path + "/config-new.xml", "w", encoding="UTF-8")
        # dom.writexml(file, indent='', addindent='', newl='\n', encoding='UTF-8')
        self.__config_dom.writexml(file)
        file.close()

    def __create_list_view(self, job_list):
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
        e = self.__dom.createElement(name)
        for attr in attr_names:
            index = attr_names.index(attr)
            e.setAttribute(attr, attr_values[index])
        return e

    def __create_element(self, name, value):
        e = self.__dom.createElement(name)
        value = self.__dom.createTextNode(value)
        e.appendChild(value)
        return e


if __name__ == "__main__":
    JenkinsConfigParser()

