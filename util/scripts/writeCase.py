# coding:utf-8
import os

from config.confManage import dir_manage
from util.tools.readYamlFile import ini_yaml
from util.tools import root_path
from util.tools.getFileNames import getFilePathList
import time


def write_case():
    testname = dir_manage('${test_name}$')
    casepath = root_path + dir_manage('${test_suite}$') + dir_manage('${case_dir}$') + "/" + testname
    datapath = root_path + dir_manage('${test_suite}$') + dir_manage('${data_dir}$') + "/" + testname
    filepathlist = getFilePathList(datapath, ".yml")
    for filepath in filepathlist:

        file = str(filepath.split(datapath)[-1])  # 处理出文件名及路径
        filename = str(filepath.split("/")[-1].split(".")[0])  # 测试用例名称
        filedata = ini_yaml(file)  # 测试数据
        midp = file.split(filename + ".yml")[0]  # 分层路径获取
        case = casepath + midp + "test_" + filename + ".py"  # 用例路径
        if not os.path.exists(casepath + midp):
            os.makedirs(casepath + midp)
        if not os.path.exists(case):

            t1 = time.strftime("%Y/%m/%d %H:%M")
            with open(case, 'w', encoding='utf-8') as f:
                f.write(f"""# coding:utf-8
\"\"\"
@author: jing
@contact: 529548204@qq.com
@file: test_{filename}.py
@time: {t1}
\"\"\"
from test_suite.testcase.{testname} import *


class Test_{filename}(object):""")
                for item in filedata:
                    order = filedata[item]["order"]

                    f.write(f"""
    @allure.story("Test_{filename}")
    @pytest.mark.parametrize('casedata', alldata["{item}"]["case"],
                             ids=[i["info"] for i in alldata["{item}"]["case"]])
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.run(order={order})""")

                    if filedata[item]["token"]:
                        # 判断是否需要token 默认类型是 Authorization
                        f.write(f"""
    def test_{item}(self, casedata, setup_Login):
        casedata["headers"]["{filedata[item]["token"]}"] = setup_Login
        casedata = relevance(alldata, casedata, setup_Login)""")
                    else:
                        f.write(f"""
    def test_{item}(self, casedata):""")
                    if not filedata[item]["file"]:
                        # 判断是否存上传文件
                        f.write("""
        res,restime, code = apisend(host=casedata["host"], address=casedata["address"], method=casedata["method"],
                               headers=casedata["headers"],
                               data=casedata["data"], caches=casedata["cache"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime, re_code=code)\n""")
                    else:
                        f.write(f"""
        res,restime, code  = apisend(host=casedata["host"], address=casedata["address"], method=casedata["method"],
                               headers=casedata["headers"],
                               data=casedata["data"], caches=casedata["cache"], 
                               files=casedata["data"]["file"])
        asserting(hope_res=casedata["assert"], real_res=res, re_time=restime, re_code=code)\n""")


# def write_case(f):
#     for i in f:
#


if __name__ == '__main__':
    # ym_path = r'thirdUrl.yml'
    # pagenames = "third_pages_1.py"

    # write_case(ym_path,pagenames)

    # ym_path = r'urlData.yml'
    # pagenames = "saasWeb_pages_1.py"
    write_case()

    # l = getFilePathList(r"D:\apitest\test_suite\datas\saasWeb", ".yml")
    # l2 = getFilePathList(r"D:\apitest\test_suite\datas\saasWeb", ".yml")
    # # print(str(l[0]).split("\\")[-1])
    # print(l)
