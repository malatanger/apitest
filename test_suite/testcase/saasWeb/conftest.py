# coding:utf-8
"""
@author: 井松
@contact: 529548204@qq.com
@file: conftest.py
@time: 2021/12/3 14:25
"""
import pytest

from test_suite.testcase.saasWeb import *



@pytest.fixture(scope="session")
def setup_Login():
    logging.info("前置请求登录")
    paramData = alldata["login"]["case"]
    logging.info("{}".format(paramData[0]["info"]))
    res, restime = apisend(host=paramData[0]["host"], address=paramData[0]["address"], method=paramData[0]["method"],
                           headers=paramData[0]["headers"],
                           data=paramData[0]["data"], caches=paramData[0]["cache"])

    logging.info("前置请求结束")
    return "JWT " + res["data"]["token"]


@pytest.fixture(scope="session")
def setup_Login_zhongtai():
    logging.info("中台前置请求登录")
    paramData = alldata["login"]["case"]
    logging.info("{}".format(paramData[1]["info"]))
    res, restime = apisend(host=paramData[1]["host"], address=paramData[1]["address"], method=paramData[1]["method"],
                           headers=paramData[1]["headers"],
                           data=paramData[1]["data"], caches=paramData[1]["cache"])

    logging.info("前置请求结束")
    return "JWT " + res["data"]["token"]
