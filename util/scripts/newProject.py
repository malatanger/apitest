# coding:utf-8
"""
@author: 井松
@contact: 529548204@qq.com
@file: newProject.py
@time: 2021/12/22 15:52
"""
import os

from config.confManage import dir_manage
from util.tools.mkDir import mk_dir
from util.tools import root_path

testname = dir_manage('${test_name}$')
pro_path = root_path + dir_manage('${test_suite}$')
casepath = pro_path + dir_manage('${case_dir}$') + "/" + testname

datapath = pro_path + dir_manage('${data_dir}$') + "/" + testname


def newProject():
    mk_dir(casepath)
    mk_dir(datapath)
    if casepath + "/" + r"{}".format("__init__.py") not in os.listdir(casepath):
        with open(casepath + "/" + r"{}".format("__init__.py"), 'w', encoding='utf-8') as f:
            f.write("""# coding:utf-8

import logging

import allure
import pytest

from common.checkResult import asserting
from util.tools.log import Log
from util.tools.readYamlFile import ini_allyaml
from common.basePage import apisend
from util.tools.iniRequests import relevance
alldata = ini_allyaml()

Log()
__all__ = [
    'pytest',
    'asserting',
    'Log',
    'ini_allyaml',
    'alldata',
    'allure',
    'apisend',
    'alldata',
    'relevance',
]""")
    if casepath + "/" + r"{}".format("conftest.py") not in os.listdir(casepath):
        with open(casepath + "/" + r"{}".format("conftest.py"), 'w', encoding='utf-8') as f:
            f.write(f"""# coding:utf-8
from test_suite.testcase.{testname} import *""")


if __name__ == '__main__':
    newProject()
