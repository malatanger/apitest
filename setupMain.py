# coding:utf-8
import logging
import os
import time

import pytest

from config.confManage import dir_manage
from util.tools.dingding import DingTalkSendMsg
from util.tools.mkDir import mk_dir
from util.tools import root_path

project_path = os.path.dirname(os.path.abspath(__file__))


# if ':' in project_path:
#     project_path = project_path.replace('\\', '/')
# else:
#     pass


def run():
    date = time.strftime('%Y-%m-%d')
    localtime = time.strftime('%Y%m%d%H%M%S', time.localtime())
    test_case_path = project_path + dir_manage('${test_suite}$') + dir_manage('${case_dir}$') + "/" + dir_manage(
        '${test_name}$')
    # temp地址变量
    temp_path = project_path + dir_manage('${report_xml_dir}$') + "/temp/"
    # html地址变量
    html_path = project_path + dir_manage('${report_html_dir}$')
    # 如果不存在地址路径则创建文件夹
    mk_dir(temp_path)
    mk_dir(html_path)
    # 执行命令行

    args = ['-s', '-q', test_case_path, '--alluredir', temp_path,"--clean-alluredir",'-n','1']
    # args = ['-s', '-q', test_case_path,]

    # args = ['-s', '-q', test_case_path, '--alluredir',
    #              '/var/jenkins_home/workspace/js/report/xml'] # docker中 jenkins工作空间项目根路径

    pytest.main(args)

    # cmd = 'allure generate %s -o %s -c' % (temp_path, html_path)
    # os.system(cmd)
    # 发送报告
    # send_email(localtime + "测试报告", "http://192.168.1.2:9999")
    # 钉钉发送
    # ding = DingTalkSendMsg()
    # ding.send_text("点击链接打开测试报告 http://192.168.1.2:9999",[13688400244])
    # 生成html报告
    os.system(r'allure generate {0} -o {1} --clean'.format(temp_path, html_path))
    # 打开报告服务 并指定端口
    os.system(r'allure serve {0} -p 11999'.format(temp_path))


if __name__ == '__main__':
    # print(project_path)
    # print(root_paht)
    run()
