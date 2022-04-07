# coding:utf-8
"""
@author: jing
@contact: 529548204@qq.com
@file: test_login.py
@time: 2022/04/04 11:29
"""
from test_suite.testcase.saasWeb import *
    

class Test_login(object):
    @allure.story("Test_login")
    @pytest.mark.parametrize('casedata', alldata["login"]["case"],
                             ids=[i["info"] for i in alldata["login"]["case"]])
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.run(order=1)
    def test_login(self, casedata):
        res, restime = apisend(host=casedata["host"], address=casedata["address"], method=casedata["method"],
                               headers=casedata["headers"],
                               data=casedata["data"], caches=casedata["cache"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime)
