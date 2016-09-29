# -*- coding: utf-8 -*-
import datetime
import os
import sys
import time

import build
import channel
import constant
import download
import ftp
import pgyer
import qi


# 发布入口
def main():
    starttime = datetime.datetime.now()
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    constant.logger.info("\n开始时间:" + t)
    constant.logger.debug('发布开始,请选择下面的工程')
    constant.config.read('config/const.properties')
    constant.logger.info(constant.path_map[constant.config_map['prj_type']])

    try:
        prj = constant.config.get("PRJ_TYPE", "build_prj")
        if prj == constant.prja:
            constant.logger.info('发布工程A:\n')
            invoke()
        elif prj == constant.prjb:
            constant.logger.info('发布工程B:\n')
            invoke()
        else:
            constant.logger.info('没有选择任何工程!')

    except Exception, e:
        constant.logger.error(e)

    endtime = datetime.datetime.now()
    constant.logger.info(("\n结束时间:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    constant.logger.info("花费 {} 分钟".format(str((endtime - starttime).seconds / 60)))
    time.sleep(5)


def invoke():
    # 创建本地目录
    create_path()
    if constant.MODULE_LIST[0].values()[0] == '1':
        build.Build().main()
    if constant.MODULE_LIST[6].values()[0] == '1':
        channel.Channel().main()
    if constant.MODULE_LIST[1].values()[0] == '1':
        ftp.Ftp().main()
    if constant.MODULE_LIST[2].values()[0] == '1':
        qi.Qiniu().main()
    if constant.MODULE_LIST[3].values()[0] == '1':
        pgyer.Pqyer().main()
    if constant.MODULE_LIST[5].values()[0] == '1':
        download.Download().main()


# 创建目录 [storage/环境/项目/日期/channel]
def create_path():
    # 当前日期
    date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
    os.chdir(sys.path[0])
    env_channel_list = constant.get_path_list()
    for env in env_channel_list:
        path = os.path.join(env, constant.config_map['prj_type'], date_path)
        if not os.path.exists(path):
            os.makedirs(path)
            os.makedirs(os.path.join(path, 'channel'))

main()
