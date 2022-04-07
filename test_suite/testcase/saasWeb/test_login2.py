from test_suite.testcase.saasWeb import *


class Test_firmwareDetail(object):

    @pytest.mark.parametrize('casedata', alldata["firmwareDetail"]["case"],
                             ids=[i["info"] for i in alldata["firmwareDetail"]["case"]])
    def test_firmwareList(self, setup_Login_zhongtai, casedata):
        casedata["headers"]["Authorization"] = setup_Login_zhongtai
        casedata = relevance(alldata, casedata, setup_Login_zhongtai)
        res, restime = apisend(host=casedata["host"], address=casedata["address"],
                               method=casedata["method"], headers=casedata["headers"], data=casedata["data"],
                               rel=casedata["cache"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime)
