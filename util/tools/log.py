# coding:utf-8
import logging
import time
import os
from util.tools.mkDir import mk_dir
from config.confManage import dir_manage
from util.tools import root_path


class Log(object):

    def __init__(self):
        """
        日志配置
        """
        now = time.strftime('%Y-%m-%d')
        log_path = root_path + dir_manage(directory='${log_dir}$') + "/"+now + "/"
        mk_dir(log_path)
        logfile_debug = log_path + "{}".format(now) + "debug.log"
        logfile_err = log_path + "{}-".format(now) + 'error.log'
        logfile_info = log_path + "{}".format(now) + "info.log"
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers = []
        fh_inf = logging.FileHandler(logfile_info, mode='a+', encoding='utf-8')
        fh_inf.setLevel(logging.INFO)
        fh_deb = logging.FileHandler(logfile_debug, mode='a+', encoding='utf-8')
        fh_deb.setLevel(logging.DEBUG)
        fh_err = logging.FileHandler(logfile_err, mode='a+',encoding='utf-8')
        fh_err.setLevel(logging.ERROR)
        formatter = logging.Formatter("%(levelname)-8s%(asctime)s  %(name)s:%(filename)s:%(lineno)d %(message)s")
        fh_inf.setFormatter(formatter)
        fh_err.setFormatter(formatter)
        self.logger.addHandler(fh_inf)
        self.logger.addHandler(fh_err)
        self.logger.addHandler(fh_deb)


if __name__ == '__main__':
    Log()
    logging.info("111222")
    logging.error("111222")
    logging.debug("111222")
    logging.warning("111222")
