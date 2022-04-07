# coding:utf-8
import os

root_path = str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))).replace("\\","/")
__all__ = [
    "root_path",
]