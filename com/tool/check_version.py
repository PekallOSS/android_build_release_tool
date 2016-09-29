# -*- coding: utf-8 -*-
import os
import sys

import apk_tool

__author__ = 'yanghai'


# 获取apk版本号
class ApkInfo:
    def __init__(self):
        pass

    # 查询参数指定apk版本号
    def query_apk(self):
        base_path = os.getcwd()
        os.chdir("/home/yanghai/work/projects/build_tool_python/com")
        vercode, vername = apk_tool.get_version(os.path.join(base_path, sys.argv[1]))
        print('内部版本号={},外部版本号={}'.format(vercode, vername))

    # 查询目录下的所有apk版本号
    def query_duo_apk(self):
        apk_path = os.getcwd()
        os.chdir("/home/yanghai/work/projects/build_tool_python/com")
        for apk in os.listdir(apk_path):
            vercode, vername = apk_tool.get_version(os.path.join(apk_path, apk))
            print('{} 内部版本号={},外部版本号={}'.format('', vercode, vername))

if __name__ == '__main__':
    if sys.argv.__len__() == 1:
        ApkInfo().query_duo_apk()
    elif sys.argv.__len__() == 2:
        ApkInfo().query_apk()
    else:
        print '参数个数错误'
