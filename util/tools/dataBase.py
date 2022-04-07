# coding:utf-8

import warnings

warnings.simplefilter('ignore', DeprecationWarning)
import pymysql
from util.tools.log import Log
import logging
from config.confManage import db_manage
import time

Log()


class MYSQL(object):

    def __init__(self,dbname):
        self.host = db_manage("${host}$",dbname)
        self.user = db_manage("${user}$",dbname)
        self.password = db_manage("${password}$",dbname)
        self.database = db_manage("${database}$",dbname)
        self.charset = db_manage("${charset}$",dbname)
        self.port = int(db_manage("${port}$",dbname))
        try:
            logging.debug("正在连接数据库.")
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
                                        port=self.port, charset=self.charset)
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            logging.debug("数据库连接成功.")
        except Exception as e:
            logging.error("连接数据库失败,{}".format(e))
            raise e

    def run_sql(self, sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        try:
            logging.debug("准备执行SQL语句..")
            logging.debug("sql语句:{}".format(sql))
            t1 = time.time()
            self.cursor.execute(sql)
            rs = self.cursor.fetchall()
            logging.info("执行成功,,sql耗时{0:.5f}秒".format(time.time() - t1))
            return rs
        except Exception as e:
            self.close()
            logging.error("执行SQL失败.{}".format(e))
            raise SystemError("执行SQL失败.{}".format(e))

    def commit(self):
        self.conn.commit()

    def close(self):
        try:
            self.cursor.close()
            logging.debug("断开数据库连接.")
        except Exception:
            logging.debug("断开数据库连接错误,请手动断开.")
            raise


if __name__ == "__main__":
    DB = MYSQL("database")
    datas = DB.run_sql(
        """
select replace((select count(*)
                from (
                         select dr.qr_code,
                                alarm.device_id,
                                alarm.grade,
                                alarm.create_time,
                                alarm.handler_status,
                                alarm.work_order

                         from alarm
                                  inner join (
                             select device.id,
                                    device.qr_code,
                                    device.region_id,
                                    region.enterprise_id,
                                    device.status,
                                    device.category_id
                             from device
                                      inner join region
                                                 on device.region_id = region.id
                                                     and region.enterprise_id = 88
                         ) as dr
                                             on dr.qr_code = alarm.device_id and
                                                alarm.create_time >= '2021-09-17 00:00:00' and
                                                alarm.create_time < '2021-09-18 00:00:00'
                     ) ad), 0, null) as "haha"
        """
    )
    print(datas[0]["haha"].decode("utf-8"))
