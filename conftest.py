# coding:utf-8
import logging
from util.tools.log import Log
Log()


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


def pytest_terminal_summary(terminalreporter):
    """收集测试结果"""

    PASSED = len(terminalreporter.stats.get('passed', []))
    FAILED = len(terminalreporter.stats.get('failed', []))
    ERROR = len(terminalreporter.stats.get('error', []))
    SKIPPED = len(terminalreporter.stats.get('skipped', []))
    TOTAL = PASSED + FAILED + ERROR + SKIPPED
    logging.info("--"*40)
    logging.info(f"执行总用例数:{TOTAL}")
    logging.info(f"执行通过数:{PASSED}")
    logging.info(f"执行失败数:{FAILED}")
    logging.info(f"执行错误数:{ERROR}")
    logging.info(f"跳过用例数:{SKIPPED}")


