# coding:utf-8

import os


def mk_dir(path):
    # 去除首位空格
    path = path.strip()
    path = path.rstrip("\\")
    path = path.rstrip("/")

    # 判断路径是否存在
    is_exists = os.path.exists(path)

    if not is_exists:
        try:
            os.makedirs(path)
        except Exception as e:
            raise (f"{path}目录创建失败：%s" % e)