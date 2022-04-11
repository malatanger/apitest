# coding:utf-8
import logging
import os

import yaml

from config.confManage import dir_manage
from util.scripts import root_path
from util.tools.getFileNames import getFilePathList
import logging

datapath = root_path + dir_manage("${test_suite}$") + dir_manage("${data_dir}$") + "/" + dir_manage("${test_name}$")


def ini_allyaml():
    # 获取目录下所有yaml文件内容 拼接成一个大字典
    alldata = {}
    datalist = getFilePathList(datapath,".yml")
    for file in datalist:
        try:
            with open(file, 'r', encoding="utf-8") as f:
                file_data = f.read()
                alldata= {**alldata,**yaml.safe_load(file_data)}
        except UnicodeDecodeError:
            with open(file, 'r') as f:
                file_data = f.read()
                alldata= {**alldata,**yaml.safe_load(file_data)}
    logging.info("*"*200)
    return alldata

def ini_yaml(filename, path=datapath):
    # 获取指定yml文件的内容
    try:
        with open(path + "/" + filename, 'r', encoding="utf-8") as f:
            file_data = f.read()
            data = yaml.safe_load(file_data)
        return data
    except UnicodeDecodeError:
        with open(path + "/" + filename, 'r') as f:
            file_data = f.read()
            data = yaml.safe_load(file_data)

        return data

if __name__ == '__main__':
    # print(datapath)
    d = ini_yaml("login_user_info.yml",r"E:\apitest")
    # d = ini_allyaml()
    print(d)
    # # case_level = runConfig_dict[0]["address"].format(**{"home_id": "123"})
    # print(runConfig_dict)

    # print(case_level)
    # print(type(case_level))
