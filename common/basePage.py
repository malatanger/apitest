# coding:utf-8
import json
import logging
import os
import random
import allure
import requests
from requests_toolbelt import MultipartEncoder
from util.tools.log import Log
from util.tools.randomData import replace_random
from config.confManage import host_manage
from util.tools.caches import Cache, valueHandle

Log()


class apiSend(object):

    def __init__(self):
        self.http_type = host_manage(hos="${http_type}$")
        self.rel = Cache()

    @staticmethod
    def iniDatas(data):
        if isinstance(data, dict):
            data = json.dumps(data, ensure_ascii=False)
        if data is None:
            return data
        dataran = replace_random(data)
        return dataran

    def post(self, address, header, caches, timeout=8, data=None, files=None, host="host"):
        """
        post请求
        :param host:
        :param caches: 关联情况
            - cachefrom: 'body' # response : 从结果中获取 body : 从参数中获取
              path: '$.code' # body如果是 "id=2&path=haha" 会转换成字典 然后根据path使用jsonpath取值
              name: 'code'
        :param address:  请求地址
        :param header: 请求头
        :param timeout: 超时时间
        :param data: 请求参数
        :param files: 文件对象 dict
        {
            'file参数名(files)': (r'文件名称.xlsx', open(r'路径\文件名称.xlsx', 'rb') 或者 直接文件路径)
        }
        file: 'D:\apitest\test_suite\files\test.png'
        files={"files": casedata["data"]["file"]}
        :return:
        """

        iniaddress = replace_random(address, param=data["urlparam"])
        url = str(self.http_type) + "://" + host_manage(hos='${{{}}}$'.format(host)) + iniaddress
        data_random = self.iniDatas(data["param"])
        logging.info("请求地址：%s" % "" + url)
        logging.info("请求方法:POST")
        logging.info("请求头: %s" % str(header))
        logging.info("请求参数: %s" % str(data_random))
        with allure.step("POST请求"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(header))
            allure.attach(name="请求参数", body=str(data_random))
        if "multipart/form-data" in str(header.values()):
            # 根据请求头contenttype判断是否为上传文件
            if isinstance(files, dict):
                for fileskey in files:
                    value = files[fileskey]
                    if isinstance(value, int):
                        files[fileskey] = str(value)
                        pass
                    elif '/' in value or "\\" in value:
                        file_parm = fileskey
                        files[file_parm] = (os.path.basename(value), open(value, 'rb'), 'application/octet-stream')
                    else:
                        pass
                multipart = MultipartEncoder(
                    fields=files,
                    boundary='-----------------------------' + str(random.randint(int(1e28), int(1e29 - 1)))
                )
                header['Content-Type'] = multipart.content_type
                response = requests.post(url=url, headers=header, timeout=timeout, data=multipart)
            elif files is None:
                try:
                    data_random = json.loads(data_random)
                except json.decoder.JSONDecodeError:
                    pass
                if not isinstance(data_random,dict):
                    data_random = valueHandle(str(data_random))
                multipart = MultipartEncoder(
                    fields=data_random,
                    boundary='-----------------------------' + str(random.randint(int(1e28), int(1e29 - 1)))
                )
                header['Content-Type'] = multipart.content_type
                response = requests.post(url=url, data=multipart, headers=header,
                                         timeout=timeout)
            else:
                raise TypeError("files参数格式错误")
        elif 'application/json' in str(header.values()):
            if data_random:
                data_random = json.loads(data_random)
            response = requests.post(url=url, json=data_random, headers=header, timeout=timeout)
        else:
            response = requests.post(url=url, data=data_random, headers=header, timeout=timeout)
        try:
            if response.status_code == 200 or response.status_code == 201:
                res = response.json()
            else:
                res = response.text
            logging.info("请求接口结果： %s" % str(res))
            self.rel.locallcache(caches, bodys=data_random, res=res)
            allure.attach(name="请求结果", body=str(res))
            return res, response.elapsed.total_seconds(),response.status_code
        except Exception as e:
            logging.error(e)
            logging.error(response.text)
            raise

    def get(self, address, caches, header, data, timeout=8, host="host"):
        """
        get请求
        :param host:
        :param caches: 关联情况
            - cachefrom: 'body' # response : 从结果中获取 body : 从参数中获取
              path: '$.code' # body如果是 "id=2&path=haha" 会转换成字典 然后根据path使用jsonpath取值
              name: 'code'
        :param address:
        :param header: 请求头
        :param data: 请求参数
        :param timeout: 超时时间
        :return:
        """
        iniaddress = replace_random(address, param=data["urlparam"])
        # if isinstance(data, dict):
        #     if "urlparam" in data.keys():
        #         address = replace_random(address, param=data["urlparam"])
        data_random = self.iniDatas(data["param"])
        url = str(self.http_type) + "://" + host_manage(hos='${{{}}}$'.format(host)) + iniaddress
        logging.info("请求地址：%s" % "" + url)
        logging.info("请求方法:GET")
        logging.info("请求头: %s" % str(header))
        logging.info("请求参数: %s" % str(data_random))
        with allure.step("GET请求接口"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(header))
            allure.attach(name="请求参数", body=str(data_random))
        response = requests.get(url=url, params=data_random, headers=header, timeout=timeout)
        if response.status_code == 301:
            response = requests.get(url=response.headers["location"])
        try:
            if response.status_code == 200 or response.status_code == 201:
                res = response.json()
            else:
                res = response.text
            logging.info("请求接口结果： %s" % str(res))
            self.rel.locallcache(caches, bodys=data_random, res=res)
            allure.attach(name="请求结果", body=str(res))
            return res, response.elapsed.total_seconds(),response.status_code
        except Exception as e:
            logging.error(e)
            logging.error(response.text)
            raise

    def put(self, address, caches, header, timeout=8, data=None, files=None, host="host"):
        """
        put请求
        :param host:
        :param address:
        :param caches: 关联情况
            - cachefrom: 'body' # response : 从结果中获取 body : 从参数中获取
              path: '$.code' # body如果是 "id=2&path=haha" 会转换成字典 然后根据path使用jsonpath取值
              name: 'code'
        :param header: 请求头

        :param timeout: 超时时间
        :param data: 请求参数
        :param files: 文件路径
        :return:
        """
        iniaddress = replace_random(address, param=data["urlparam"])
        url = str(self.http_type) + "://" + host_manage(hos='${{{}}}$'.format(host)) + iniaddress
        logging.info("请求地址：%s" % "" + url)
        logging.info("请求方法:PUT")
        logging.info("请求头: %s" % str(header))
        data_random = self.iniDatas(data["param"])
        logging.info("请求参数: %s" % str(data_random))
        with allure.step("PUT请求接口"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(header))
            allure.attach(name="请求参数", body=str(data_random))
        if 'application/json' in header.values():
            if data_random:
                data_random = json.loads(data_random)
            response = requests.put(url=url, json=data_random, headers=header, timeout=timeout, files=files)
        else:
            response = requests.put(url=url, data=data_random, headers=header, timeout=timeout, files=files)
        try:
            if response.status_code == 200 or response.status_code == 201:
                res = response.json()
            else:
                res = response.text
            logging.info("请求接口结果： %s" % str(res))
            self.rel.locallcache(caches, bodys=data_random, res=res)
            allure.attach(name="请求结果", body=str(res))
            return res, response.elapsed.total_seconds(),response.status_code
        except Exception as e:
            logging.error(e)
            logging.error(response.text)
            raise

    def delete(self, address, caches, header, data, timeout=8, host="host"):
        """
        get请求
        :param host:
        :param caches: 关联情况
            - cachefrom: 'body' # response : 从结果中获取 body : 从参数中获取
              path: '$.code' # body如果是 "id=2&path=haha" 会转换成字典 然后根据path使用jsonpath取值
              name: 'code'
        :param address:
        :param header: 请求头
        :param data: 请求参数
        :param timeout: 超时时间
        :return:
        """
        iniaddress = replace_random(address, param=data["urlparam"])
        data_random = self.iniDatas(data["param"])
        url = str(self.http_type) + "://" + host_manage(hos='${{{}}}$'.format(host)) + iniaddress
        logging.info("请求地址：%s" % "" + url)
        logging.info("请求方法:DELETE")
        logging.info("请求头: %s" % str(header))
        logging.info("请求参数: %s" % str(data_random))
        with allure.step("DELETE请求接口"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(header))
            allure.attach(name="请求参数", body=str(data_random))
        response = requests.delete(url=url, params=data_random, headers=header, timeout=timeout)

        try:
            if response.status_code == 200 or response.status_code == 201:
                res = response.json()
            else:
                res = response.text
            logging.info("请求接口结果： %s" % str(res))
            self.rel.locallcache(caches, bodys=data_random, res=res)
            allure.attach(name="请求结果", body=str(res))
            return res, response.elapsed.total_seconds(),response.status_code
        except Exception as e:
            logging.error(e)
            logging.error(response.text)
            raise

    def patch(self, address, caches, header, timeout=8, data=None, files=None, host="host"):
        iniaddress = replace_random(address, param=data["urlparam"])
        url = str(self.http_type) + "://" + host_manage(hos='${{{}}}$'.format(host)) + iniaddress
        logging.info("请求地址：%s" % "" + url)
        logging.info("请求方法:PATHC")
        logging.info("请求头: %s" % str(header))
        data_random = self.iniDatas(data["param"])
        logging.info("请求参数: %s" % str(data_random))
        with allure.step("PATCH请求接口"):
            allure.attach(name="请求地址", body=url)
            allure.attach(name="请求头", body=str(header))
            allure.attach(name="请求参数", body=str(data_random))
        if 'application/json' in header.values():
            if data_random:
                data_random = json.loads(data_random)
            response = requests.patch(url=url, json=data_random, headers=header, timeout=timeout, files=files)
        else:
            response = requests.patch(url=url, data=data_random, headers=header, timeout=timeout, files=files)
        try:
            if response.status_code == 200 or response.status_code == 201:
                res = response.json()
            else:
                res = response.text
            logging.info("请求接口结果： %s" % str(res))
            allure.attach(name="请求结果", body=str(res))
            self.rel.locallcache(caches, bodys=data_random, res=res)
            return res, response.elapsed.total_seconds(),response.status_code
        except Exception as e:
            logging.error(e)
            logging.error(response.text)
            raise

    def __call__(self, address, method, headers, data, caches, **kwargs):
        try:
            if method == "post" or method == 'POST':
                return self.post(address=address, data=data, header=headers, caches=caches, **kwargs)
            elif method == "get" or method == 'GET':
                return self.get(address=address, data=data, header=headers, caches=caches, **kwargs)
            elif method == "delete" or method == 'DELETE':
                return self.delete(address=address, data=data, header=headers, caches=caches, **kwargs)
            elif method == "put" or method == 'PUT':
                return self.put(address=address, data=data, header=headers, caches=caches, **kwargs)
            elif method == "patch" or method == 'PATCH':
                return self.patch(address=address, data=data, header=headers, caches=caches, **kwargs)
            else:
                raise TypeError(f"请求异常,检查yml文件method")
        except Exception:
            raise


apisend = apiSend()
if __name__ == '__main__':
    h = {
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjE2OTRmYjlmLTUzNjYtNGZjZS1hODg4LTBlY2UxOThmZThhZSJ9.5_mD4abE-5iHsSr6RB9R8qaIRV7zidUFkpytyyd2cjSiQcrdJvAE_6GjU9Q_Xsr0JmTkSCTiefpFySguyk2E8Q",
        "Content-Type": "multipart/form-data"

    }
    d = {
        "param": "updateSupport=0",
        "urlparam": None
    }
    p ={'address': '/v1/enter/trade/', 'assert': {'jsonpath': None, 'sqlassert': None, 'time': 2, 'code': 201}, 'data': {'param': {'name': '行业名称$RandomString($RandomPosInt(2,6)$)$', 'desc': '备注$RandomString($RandomPosInt(2,8)$)$'}, 'urlparam': None}, 'headers': {'Content-Type': 'application/json', 'Authorization': 'GREEN eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyMiwiZXhwIjoxNjUxODMzNjY4LCJ1c2VybmFtZSI6ImRsMDAxIn0.Dbk1ddEXdmW1tRzxZLvFgJwsh0hek6HJjzCabStdnz0'}, 'host': 'host_HB', 'info': '新建行业', 'method': 'POST', 'cache': None, 'relevance': None}
    ress = apisend(address=p['address'], data=p['data'], method=p['method'], headers=p['headers'],
                   caches=p['cache'],host=p['host'],)
    print(ress)
