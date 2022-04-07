# coding:utf-8

import logging

import allure
import jsonpath

from util.tools.dataBase import MYSQL
from util.tools.log import Log
from util.tools.randomData import replace_random
from util.tools.readYamlFile import ini_yaml

Log()


def assert_text(hope_res, real_res, third_data=None, third_datas=None):
    """
    文本判断
    :param third_datas:
    :param third_data:
    :param hope_res: 期望结果
    :param real_res: 实际结果
    :return:
    """
    if isinstance(hope_res["jsonpath"], list):
        for h_res in hope_res["jsonpath"]:
            if jsonpath.jsonpath(real_res, h_res["path"]):
                r_res = jsonpath.jsonpath(real_res, h_res["path"])[0]
                if h_res["asserttype"] == "==":
                    try:
                        if not third_datas:
                            h_res["value"] = replace_random(str(h_res["value"]), res=third_data)
                            with allure.step("json断言判断相等"):
                                allure.attach(name="期望结果", body=str(h_res))
                                allure.attach(name='实际实际结果', body=str(r_res))
                                assert str(r_res) == str(h_res["value"])
                                logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                        elif third_datas:
                            if h_res["relevanceCheck"]:
                                h_res["value"] = replace_random(str(h_res["value"]),
                                                                res=third_datas[h_res["relevanceCheck"]])
                                with allure.step("json断言判断相等"):
                                    allure.attach(name="期望结果", body=str(h_res))
                                    allure.attach(name='实际实际结果', body=str(r_res))
                                    assert str(r_res) == str(h_res["value"])
                                    logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                        raise
                elif h_res["asserttype"] == "!=":
                    try:
                        h_res["value"] = replace_random(str(h_res["value"]), res=third_data)
                        with allure.step("json断言判断不等"):
                            allure.attach(name="json期望结果", body=str(h_res))
                            allure.attach(name='json实际实际结果', body=str(r_res))
                            assert str(r_res) != str(h_res["value"])
                            logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, r_res))
                        raise
                elif h_res["asserttype"] == "in":
                    r_res = str(r_res)
                    try:
                        h_res["value"] = replace_random(str(h_res["value"]), res=third_data)
                        with allure.step("json断言判断包含"):
                            allure.attach(name="期望结果", body=str(h_res))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            assert str(r_res) in str(h_res["value"])
                            logging.info("json断言通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, real_res))
                    except AssertionError:
                        logging.error("json断言未通过, 期望结果'{0}', 实际结果'{1}'".format(h_res, real_res))
                        raise
                else:
                    raise TypeError("asserttype方法错误")
            else:
                raise ValueError("获取json值失败,请检查jsonpath")


def assert_time(hope_res, real_res):
    hope_time = hope_res["time"]
    try:
        with allure.step("判断响应时间"):
            allure.attach(name="期望响应时间", body=str(hope_time))
            allure.attach(name='实际响应时间', body=str(real_res))
            assert real_res <= hope_time
            logging.info("time断言通过, 期望响应时间'{0}', 实际响应时间'{1}'".format(hope_time, real_res))
    except AssertionError:
        logging.error("请求响应时间过长, 期望时间'{0}', 实际时间'{1}'".format(hope_time, real_res))
        raise


def assert_sql(hope_res, real_res):
    """
    一定要把断言的sql写精确写 只能通过sql查询出来的数据第一条进行断言
    :param hope_res:
    :param real_res:
    :return:
    """
    if isinstance(hope_res["sqlassert"], list):

        for h_res in hope_res["sqlassert"]:
            db = MYSQL(h_res["db_name"])
            h_sql = h_res["sql"]
            r_sql = replace_random(h_sql, real_res)
            datas = db.run_sql(r_sql)
            for i in h_res["datas"]:
                if jsonpath.jsonpath(real_res, i["path"]):
                    r_res = jsonpath.jsonpath(real_res, i["path"])[0]
                    i["name"] = replace_random(i["name"], real_res)
                    try:
                        with allure.step("数据库校验"):
                            allure.attach(name="期望结果", body=str(datas))
                            allure.attach(name='实际实际结果', body=str(r_res))
                            allure.attach(name='sql命令', body=str(r_sql))
                            if datas:
                                d = datas[0][i["name"]]
                            else:
                                d = None
                            if isinstance(d, bytes):
                                d = d.decode("utf-8")
                            assert str(r_res) == str(d)
                            logging.info(
                                "sql断言通过, 期望结果'{0}', 实际结果'{1}'".format(datas, r_res))
                            db.close()
                    except AssertionError:
                        db.close()
                        logging.error("sql断言未通过, 期望结果'{0}', 实际结果'{1}'".format(datas, r_res))
                        raise
                else:
                    db.close()
                    raise ValueError("获取json值失败,请检查jsonpath")
    else:
        raise ValueError("请检查sqlassert格式,如不需要断言,此字段应为空.")


def assert_code(hope_res, real_res):
    """

    :param hope_res:
    :param real_res:
    :return:
    """
    hope_code = hope_res["code"]
    try:
        with allure.step("判断状态码"):
            allure.attach(name="期望状态码", body=str(hope_code))
            allure.attach(name='实际状态码', body=str(real_res))
            assert real_res <= hope_code
            logging.info("code断言通过, 期望状态码'{0}', 实际状态码'{1}'".format(hope_code, real_res))
    except AssertionError:
        logging.error("code断言未通过, 期望状态码'{0}', 实际状态码'{1}'".format(hope_code, real_res))
        raise
def asserting(hope_res, real_res,re_code=None, re_time=None, third_data=None, third_datas=None):
    """

    :param re_code:
    :param hope_res: 期望结果
    :param real_res: 实际结果
    :param re_time: 实际响应时间
    :param third_data: 依赖数据
    :param third_datas: 依赖数据组
    :return:
    """
    if hope_res["jsonpath"]:
        assert_text(hope_res, real_res, third_data, third_datas)
    if hope_res["sqlassert"]:
        assert_sql(hope_res, real_res)
    if hope_res["time"]:
        assert_time(hope_res, re_time)
    if hope_res["code"]:
        assert_code(hope_res, re_code)



if __name__ == '__main__':
    j = {'code': 0, 'msg': 'Success.', 'data': {
        'token': 'eyJ1c2VyX2lkIjoxOTYsInVzZXJuYW1lIjoiZmluc2lvdCIsImV4cCI6MTYzMzc2MDg0NCwiZW1haWwiOiIifQ',
        'id': 196, 'username': '123'}}
    # hp = {
    #     "jsonpath": [
    #
    #     ],
    #     "sqlassert": [
    #         {
    #             "datas": [
    #                 {
    #                     "path": "$.data.id",
    #                     "name": "id"
    #                 },
    #                 {
    #                     "path": "$.data.username",
    #                     "name": "username"
    #                 },
    #             ],
    #             "sql": "select * from saas.user where username = '123' ",
    #         },
    #         {
    #             "datas": [
    #                 {
    #                     "path": "$.data.id",
    #                     "name": "id"
    #                 },
    #                 {
    #                     "path": "$.data.username",
    #                     "name": "username"
    #                 },
    #             ],
    #             "sql": "select * from saas.user where username = '44324' ",
    #         }
    #     ],
    #     "time": None
    # }
    hp = ini_yaml("loginData.yml")
    # print(hp)
    asserting(hp["login"][0]["assert"], j, 23)
