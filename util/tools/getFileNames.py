# coding:utf-8
"""
@author: jing
@contact: 529548204@qq.com
@file: getFileNames.py
@time: 2022/4/2 15:54
"""
import os


def getFilePathList(rootpath, filetype):
    filepath = []
    # 获取所有文件下的子文件名称
    for root, dirs, files in os.walk(rootpath):
        # 过滤所有空文件
        if files:
            for file in files:
                path = os.path.join(root, file)
                # 判断只返回 yaml 的文件
                if filetype in path:
                    filepath.append(str(path).replace("\\", "/"))
    return filepath


if __name__ == '__main__':
    datalist = getFilePathList(r"D:\apitest\test_suite\datas\saasWeb", ".yml")
    print(datalist)