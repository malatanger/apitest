# coding:utf-8
"""
@author: 井松
@contact: 529548204@qq.com
@file: recording.py
@time: 2022/1/6 15:41
"""
import os
import yaml
from mitmproxy.http import HTTPFlow
from mitmproxy import ctx
from config.confManage import dir_manage, host_manage
from util.tools import root_path
import logging
from util.tools.log import Log
from util.tools.mkDir import mk_dir

Log()
Host = host_manage("${host_HB}$")


class Counter:
    def __init__(self, host):
        self.re = {}
        self.num = 0
        self.path = root_path
        self.host = host

    def response(self, flow: HTTPFlow):
        mk_dir(self.path + dir_manage("${test_suite}$") + dir_manage("${recording_dir}$"))
        case = dict()
        case["data"] = data = {}
        if flow.request.host == self.host.split(":")[0]:
            headers = flow.request.headers
            # 获取header
            url_param_list = flow.request.path.split("?")
            # 将url根据?截断
            case["method"] = flow.request.method
            # 获取请求方法
            if case["method"] == "GET" or case["method"] == "DELETE":
                if "Content-Type" in headers.keys():
                    case["headers"]["Content-Type"] = headers["Content-Type"]
                else:
                    if len(url_param_list) > 1:
                        data["param"] = url_param_list[1]
            elif case["method"] == "POST" or case["method"] == "PUT":
                if "application/json" in headers["Content-Type"]:
                    data["param"] = flow.request.json()

            if "ETag" not in flow.response.headers.keys():
                # 判断无用请求
                self.re = {}
                # self.num = self.num + 1
                # url根据?截断
                name = url_param_list[0].replace("/", "_")[1:] + flow.request.method
                self.re[name] = detail = {}

                detail["name"] = name # 请求名称
                detail["token"] = "Authorization" # 请求鉴权 默认Authorization 可以根据需要修改
                # detail["order"] = self.num
                detail["case"] = [case]
                detail["file"] = False

                # case 数据
                case["info"] = name
                case["host"] = "host"  # 可参数化
                case["address"] = url_param_list[0] # path
                case["relevance"] = None
                case["cache"] = None
                case["headers"] = {}
                case["headers"] = dict(headers)
                case["assert"] = asserting = {}
                # 断言数据
                asserting["jsonpath"] = None
                asserting["sqlassert"] = None
                asserting["time"] = 2
                asserting["code"] = 200
                # asserting["jsonpath"] = [{
                #     "path": "$.code",
                #     "value": 0,
                #     "asserttype": "=="
                # }]
                # case内参数数据
                data["file"] = None
                data["param"] = None
                data["urlparam"] = None

                path = self.path + dir_manage("${test_suite}$") + dir_manage("${recording_dir}$") + "/" + case[
                    "address"]
                # 根据path创建yaml
                if "form-data" not in str(flow.request.content):
                    self.yaml_cases(path, path + detail[
                        "name"] + ".yml", self.re)

                    print(self.re)
                    #控制台打印

    @staticmethod
    def yaml_cases(casepath, filename, data):
        """
        根据数据创建yaml文件
        :param casepath:
        :param filename:
        :param data:
        :return:
        """
        if not os.path.exists(casepath):
            os.makedirs(casepath)

        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)
            # f.write()
            # yaml.dump(data, f, Dumper=yaml.RoundTripDumper, allow_unicode=True)
    # def response(self, flow: HTTPFlow):
    #     if flow.request.host == "dashboard.finsiot.com":
    #         print(flow.response.json())


addons = [
    Counter(Host)
]

if __name__ == '__main__':
    # os.system("mitmdump -p 4444")
    os.system("mitmdump -p 4444 -s ./recording.py -q")
    # os.system("mitmweb -p 4444 -s ./recording.py -q")
    # os.system("")
