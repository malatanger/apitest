# coding:utf-8
"""
@author: jing
@contact: 529548204@qq.com
@file: iniRequests.py
@time: 2022/4/2 16:48
"""
from common.basePage import apisend
from util.tools.randomData import replace_random
import jsonpath
import allure


def relevance(alldata, relevancedata, headerdata=None):
    """

    :param alldata:  yaml读取的全部数据
    :param relevancedata: 当前请求数据
    :param headerdata: 被关联接口可能需要的请求头
    :return:
    """
    reldatalist = relevancedata["relevance"]
    reldict = {}
    if reldatalist:
        for reldata in reldatalist:

            relcase = alldata[reldata["relCaseName"]]["case"][reldata["relCaseNum"] - 1]
            # 获取被关联请求数据
            # if p["relevance"]:
            #     relevance(alldata,relevancedata=p,headerdata=headerdata)
            with allure.step("执行关联接口"):
                if relcase["relevance"]:
                    # 如果被关联请求数据仍然存在关联情况 递归
                    relcase = relevance(alldata, relevancedata=relcase, headerdata=headerdata)
                if alldata[reldata["relCaseName"]]["token"]:
                    # 处理请求头
                    relcase["headers"][alldata[reldata["relCaseName"]]["token"]] = headerdata
                # 进行关联接口请求
                res, time, code= apisend(address=relcase["address"],
                                    method=relcase["method"], headers=relcase["headers"], data=relcase["data"],
                                    caches=relcase["cache"],host=relcase["host"])

                reldict[reldata["name"]] = jsonpath.jsonpath(res, reldata["value"])[0]
                # 处理结果存入字典中 得到{关联数据的name:关联数据的值}

    data = eval(replace_random(str(relevancedata),param=reldict))
    # 将当前请求根据正则匹配 例: relevancedata 中包含  $relevance(id)$  reldict={id:1} 处理后 $relevance(id)$ 被替换为1
    # 返回关联之完成 处理后的数据
    return data


if __name__ == '__main__':
    d = {'info': '固件详情', 'host': 'host', 'address': '/v1/device/firmware/$url(firmwareId)$/', 'method': 'get',
         'cache': None,
         'relevance': [{'relCaseName': 'firmwareList', 'relCaseNum': 1, 'value': '$.data[0].id', 'name': 'firmwareId'},
                       {'relCaseName': 'firmwareList', 'relCaseNum': 1, 'value': '$.data[0].id', 'name': 'firmwareId2'}],
         'headers': {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': None},
         'data': {'param': None, 'urlparam': {'firmwareId': '$relevance(firmwareId)$'}}, 'assert': {
            'jsonpath': [{'path': '$.msg', 'value': 'Success.', 'asserttype': '==', 'relevanceCheck': None},
                         {'path': '$.code', 'value': 0, 'asserttype': '==', 'relevanceCheck': None}], 'sqlassert': None,
            'time': 2}}
    h = "JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJhZG1pbjIiLCJleHAiOjE2NTE0ODUyOTcsImVtYWlsIjoiYWRtaW5AZXhhbXBsZS5jb20ifQ.ZIUziDJlJXFHPrLB1DH37Y-axF-cRpTNPqfdEk_WQTA"
    # s = relevance(alldata=ini_allyaml(), relevancedata=d, headerdata=h)
    # print(type(s))
    # r = {'address': '/v1/enter/trade/$url(tradeId)$/', 'data': {'file': None, 'param': {'name': '行业名称$RandomString($RandomPosInt(2,6)$)$', 'desc': '备注$RandomString($RandomPosInt(2,8)$)$'}, 'urlparam': {'tradeId': '$relevance(tradeId)$'}}, 'relevance': [{'relCaseName': 'tradeAdd', 'relCaseNum': 1, 'value': '$.id', 'name': 'tradeID'}]}
    # rd = {'tradeID': 119}
    # d2 = replace_random(str(r),param=rd)
    # print(d2)
