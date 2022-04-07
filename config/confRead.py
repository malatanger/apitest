# coding:utf-8
import configparser
import os


class Config(object):

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.conf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

    def read_host(self):
        """
        读取配置文件中host相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['host']

    def read_email(self):
        """
        读取配置文件中host相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['email']

    def read_dir(self):
        """
        读取配置文件中directory相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['directory']

    def read_db(self,dbname):
        """
        读取配置文件中directory相关信息
        :return:
        """
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config[dbname]

    def read_dingding(self):
        self.config.read(self.conf_path, encoding='utf-8')
        return self.config['dingding']


if __name__ == '__main__':
    c = Config()
    print(c.read_db("database"))
