# coding:utf-8
"""
@author: 井松
@contact: 529548204@qq.com
@file: caches.py
@time: 2021/11/15 17:13
"""

import os
import shutil

import jsonpath
from util.tools.mkDir import mk_dir
from util.tools import root_path

from config.confManage import dir_manage

"""
response: 执行接口,根据jsonpath 读取返回结果的指定值 存入缓存
body: 执行前 把body转化成json格式 根据jsonpath 读取指定参数值 存入缓存

取
body: get请求 根据name replace参数 post 根据path 更新json数据
"""
cachepath = root_path + dir_manage("${cache_dir}$")


def valueHandle(data: str):
    param_dict = {}
    param_list = data.split("&")
    for param in param_list:
        param_dict[param.split("=")[0]] = param.split("=")[1]
    return param_dict


class Cache(object):
    def __init__(self, path=cachepath):
        self.path = path
        mk_dir(path)
        self.del_list = os.listdir(self.path)

    def set(self, key, value):
        """
        保存缓存值
        :param key:
        :param value:
        :return:
        """
        with open(self.path + "/" + key, 'w', encoding="utf-8") as f:
            f.write(str(value))

    def get(self, key):
        """
        获取指定缓存值
        :param key:
        :return:
        """
        if key in self.del_list:
            with open(self.path + "/" + key, 'r', encoding="utf-8") as f:
                value = f.read()
            return value
        else:
            raise ValueError("{}不存在".format(key))

    def set_many(self, data: dict):
        """
        批量设置缓存
        :param data:
        :return:
        """
        for i in data:
            with open(self.path + "/" + i, 'w', encoding="utf-8") as f:
                f.write(str(data[i]))

    def clear_all_cache(self):
        """
        清楚所有缓存
        :return:
        """
        del_list = os.listdir(self.path)
        for f in del_list:
            file_path = os.path.join(self.path, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    def clear_cache(self, key: str):
        """
        清楚指定缓存
        :param key:
        :return:
        """
        file_path = os.path.join(self.path, key)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    def respons_cache(self, data, respons):
        """
        从请求结果中获取(json结果)
        :param data:
        :param respons:
        :return:
        """
        values = jsonpath.jsonpath(respons, data['path'])
        if not values:
            raise ValueError("path错误")
        self.set(key=data["name"], value=values[0])

    def body_cache(self, data, param):
        """
        从请求体中获取 get请求参数会转化为json格式方便处理
        :param data:
        :param param:
        :return:
        """
        if isinstance(param, dict):
            values = jsonpath.jsonpath(param, data['path'])
            if not values:
                raise ValueError("path错误")
            self.set(key=data["name"], value=values[0])
        else:
            values = jsonpath.jsonpath(valueHandle(param), data['path'])
            if not values:
                raise ValueError("path错误")
            self.set(key=data["name"], value=values[0])

    def locallcache(self, data, bodys=None, res=None):
        """
        本地缓存方法
        :param data:
        :param bodys:
        :param res:
        :return:
        """
        if data is not None:
            for i in data:
                if i["cachefrom"] == 'body':
                    self.body_cache(i, bodys)
                elif i["cachefrom"] == 'response':
                    self.respons_cache(i, res)
                else:
                    raise TypeError("datasfrom错误")
        else:
            pass


if __name__ == '__main__':
    s = {'name': '固件新增', 'token': 'Authorization', 'order': 1, 'case': [
        {'info': '固件新增', 'host': 'host', 'address': '/v1/device/firmware/', 'method': 'post',
         'relevance': [{'cachefrom': 'body', 'path': '$.data.id1', 'name': 'firmwareId'}],
         'headers': {'Content-Type': 'application/json'}, 'data': {
            'param': {'desc': '测试', 'name': '测试固件$RandomString($RandomPosInt(2,8)$)$', 'size': '20',
                      'url': 'V1.0.$RandomPosInt(6,8)$.rbl', 'category': 'F001'}, 'urlparam': None}, 'assert': {
            'jsonpath': [{'path': '$.msg', 'value': 'Success.', 'asserttype': '==', 'relevanceCheck': None},
                         {'path': '$.code', 'value': 0, 'asserttype': '==', 'relevanceCheck': None}], 'sqlassert': None,
            'time': 2}}]}
    ress = {'code': 0, 'msg': 'Success.',
            'data': {'id': 64, 'create_time': '2022-01-12T09:37:32.276085', 'update_time': '2022-01-12T09:37:32.276104',
                     'name': '测试固件dE8', 'size': 20.0, 'category': 'F001', 'desc': '测试', 'url': 'V1.0.6.rbl'}}
    # bo = "code=200&msg=success"
    bo ={"a":1}
    # util.tools.readYamlFile import ini_yaml
    #
    # s1 = ini_yaml("firmware.yml", r"D:\apitest\test_suite\datas\saasWeb\firmware")
    rels = Cache()

    rels.locallcache(s["case"][0]["relevance"], bodys=bo, res=ress)
    # rels.caches.clear_cache("firmwareId")