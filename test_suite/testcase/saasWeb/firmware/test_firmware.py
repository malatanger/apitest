# coding:utf-8
"""
@author: jing
@contact: 529548204@qq.com
@file: test_firmware.py
@time: 2022/04/04 11:29
"""
from test_suite.testcase.saasWeb import *
    

class Test_firmware(object):
    @allure.story("Test_firmware")
    @pytest.mark.parametrize('casedata', alldata["firmwareList"]["case"],
                             ids=[i["info"] for i in alldata["firmwareList"]["case"]])
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.run(order=1)
    def test_firmwareList(self, casedata, setup_Login):
        casedata["headers"]["Authorization"] = setup_Login
        casedata = relevance(alldata, casedata, setup_Login)
        res, restime = apisend(host=casedata["host"], address=casedata["address"], method=casedata["method"],
                               headers=casedata["headers"],
                               data=casedata["data"], caches=casedata["cache"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime)

    @allure.story("Test_firmware")
    @pytest.mark.parametrize('casedata', alldata["firmwareDetail"]["case"],
                             ids=[i["info"] for i in alldata["firmwareDetail"]["case"]])
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.run(order=2)
    def test_firmwareDetail(self, casedata, setup_Login):
        casedata["headers"]["Authorization"] = setup_Login
        casedata = relevance(alldata, casedata, setup_Login)
        res, restime = apisend(host=casedata["host"], address=casedata["address"], method=casedata["method"],
                               headers=casedata["headers"],
                               data=casedata["data"], caches=casedata["cache"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime)
