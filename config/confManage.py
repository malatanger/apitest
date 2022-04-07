# coding:utf-8
import re

from config.confRead import Config


def host_manage(hos):
    """
    host关联配置
    :param hos:
    :return:
    """
    try:
        relevance_list = re.findall(r'\${(.*?)}\$', hos)
        for n in relevance_list:
            pattern = re.compile(r'\${' + n + r'}\$')
            host_cf = Config()
            host_relevance = host_cf.read_host()
            hos = re.sub(pattern, host_relevance[n], hos, count=1)
    except TypeError:
        pass
    return hos


def mail_manage(ml):
    """
    email关联配置
    :param ml:
    :return:
    """
    try:
        relevance_list = re.findall(r"\${(.*?)}\$", ml)
        for n in relevance_list:
            pattern = re.compile(r'\${' + n + r'}\$')
            email_cf = Config()
            email_relevance = email_cf.read_email()
            ml = re.sub(pattern, email_relevance[n], ml, count=1)
    except TypeError:
        pass
    return ml


def dir_manage(directory):
    """
    directory关联配置
    :param directory:
    :return:
    """
    try:
        relevance_list = re.findall(r"\${(.*?)}\$", directory)
        for n in relevance_list:
            pattern = re.compile(r'\${' + n + r'}\$')
            dir_cf = Config()
            dir_relevance = dir_cf.read_dir()
            directory = re.sub(pattern, dir_relevance[n], directory, count=1)
    except TypeError:
        pass
    return directory


def db_manage(db,dbname='database'):
    try:
        relevance_list = re.findall(r"\${(.*?)}\$", db)
        for n in relevance_list:
            pattern = re.compile(r'\${' + n + r'}\$')
            dir_cf = Config()
            dir_relevance = dir_cf.read_db(dbname=dbname)
            db = re.sub(pattern, dir_relevance[n], db, count=1)
    except TypeError:
        pass
    return db


def dingding_manage(dingding):
    try:
        relevance_list = re.findall(r"\${(.*?)}\$", dingding)
        for n in relevance_list:
            pattern = re.compile(r'\${' + n + r'}\$')
            dir_cf = Config()
            dir_relevance = dir_cf.read_dingding()
            dingding = re.sub(pattern, dir_relevance[n], dingding, count=1)
    except TypeError:
        pass
    return dingding


if __name__ == '__main__':
    # print(dir_manage("${pro_dir}$"))
    # print(db_manage("${user}$"))
    # print(db_manage("${password}$"))
    # print(db_manage("${database}$"))
    # print(db_manage("${charset}$"))
    # print(int(db_manage("${port}$")))
    print(host_manage("${host}$${host_117}$"))
    # print("${{{haha}}}$".format(**{"haha":"123"}))
    # print(host_manage("${{{haha}}}$".format(**{"haha":"host2"})))
