# -*- coding: utf-8 -*-
# 用于检测上传的apk和编译的apk版本是否一致
import os
import subprocess
import sys
import time

import app_name
import constant
import tool.apk_tool

__author__ = 'yanghai'


class Download:
    def __init__(self):
        pass

    dict_login = {
        constant.prja: {'username': 'ui.ff@fo.com', 'password': '1111', 'namespace': 'test'},
        constant.prjb: {'username': 'ui.ff@fo.com', 'password': '1111', 'namespace': 'test'}
    }

    def main(self):
        constant.logger.info('\n------七牛文件版本号比较------')
        os.chdir(sys.path[0])
        # 登录
        # url = './qiniu-devtools/./qrsctl login tan.jing@jinyuc.com clf800050'
        url = './qiniu-devtools/./qrsctl login {} {}'.format(
            self.dict_login[constant.config_map['prj_type']]['username'],
            self.dict_login[constant.config_map['prj_type']]['password'])
        subprocess.call(url, shell=True)

        # 遍历环境并编译
        for constant.QUDAO, on in constant.ENV_LIST.items():
            if on == '1':
                # 获取七牛apk版本信息
                qiniu_code, qiniu_name, apk = self.get_qiniu_apk_version()

                # 获取编译apk版本信息
                build_code, build_name, build_apk = self.get_build_apk_version()

                constant.logger.info('环境:{}\n文件:{}\n编译:[{},{}]\n七牛:[{},{}]'
                                     .format(constant.QUDAO, apk, build_code, build_name, qiniu_code, qiniu_name))

    # 获取七牛apk版本信息
    def get_qiniu_apk_version(self):
        # 获取apk名称
        apk = app_name.name_dict[constant.config_map['prj_type']][constant.QUDAO]
        namespace = self.dict_login[constant.config_map['prj_type']]['namespace']
        url = './qiniu-devtools/./qrsctl get {} {}'.format(namespace, apk)
        subprocess.call(url, shell=True)
        # 获取apk版本信息
        vercode, vername = tool.apk_tool.get_version(apk)
        # 删除apk文件
        os.remove(apk)
        return vercode, vername, apk

    # 获取编译apk版本信息
    def get_build_apk_version(self):
        # 获取所有目录
        path_list = constant.get_path_list()
        # 获取该渠道所在的目录
        path = path_list[path_list.index(os.path.join(constant.PCP_BASE_PATH, constant.QUDAO))]

        # 当前日期
        date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
        apk = os.path.join(sys.path[0], path,
                           constant.config_map['prj_type'],
                           date_path,
                           app_name.name_dict[constant.config_map['prj_type']][constant.QUDAO])

        if os.path.exists(apk):
            # 获取下载apk版本信息
            vercode, vername = tool.apk_tool.get_version(apk)
        else:
            constant.logger.error("编译apk不存在! [{}]".format(apk))
            vercode = ''
            vername = ''
        return vercode, vername, apk
