# -*- coding: utf-8 -*-
import logging
import logging.config
import os
import pickle
import shutil
import sys
import time

import ConfigParser

prja = 'prja'
prjb = 'prjb'
utility = 'utility'

# apk存放基本目录
PCP_BASE_PATH = os.path.join('storage', 'pcp')

# 工程位置
path_map = {prja: '/home/yanghai/work/openSource/project/prja',
            prjb: '/home/yanghai/work/openSource/project/prjb',
            utility: '/home/yanghai/work/openSource/project/utility'}

# 暂存当前环境
QUDAO = None

# 　切换脚本运行目录
os.chdir(sys.path[0])
config = ConfigParser.ConfigParser()
config.read('config/const.properties')

# 功能模块
MODULE_LIST = [{'Build': config.get("MODULE_LIST", "build")},
               {'Ftp': config.get("MODULE_LIST", "ftp")},
               {'Qiniu': config.get("MODULE_LIST", "qiniu")},
               {'Pqyer': config.get("MODULE_LIST", "pqyer")},
               {'Yunwei': config.get("MODULE_LIST", "yunwei")},
               {'Download': config.get("MODULE_LIST", "download")},
               {'Channel': config.get("MODULE_LIST", "channel")},
               {'Fir': config.get("MODULE_LIST", "fir")}]

# 打包参数配置
config_map = {'prj_type': config.get("PRJ_TYPE", "build_prj"),  # 工程类型
              'build': config.get("MODULE_LIST", "build"),  # 编译
              'channel': config.get("MODULE_LIST", "channel"),  # 多渠道
              'ftp': config.get("MODULE_LIST", "ftp"),  # ftp
              'qiniu': config.get("MODULE_LIST", "qiniu"),  # 七牛
              'pqyer': config.get("MODULE_LIST", "pqyer"),  # 蒲公英
              'fir': config.get("MODULE_LIST", "fir"),  # fir
              'yunwei': config.get("MODULE_LIST", "yunwei"),  # 运维
              'download': config.get("MODULE_LIST", "download"),  # 下载检测
              'environment': config.get("ENV_LIST", "environment"),  # 环境
              'dev': config.get("ENV_LIST", "dev"),  # 开发环境
              'test': config.get("ENV_LIST", "test"),  # 测试环境
              'pre': config.get("ENV_LIST", "pre"),  # 预生产环境
              'pro': config.get("ENV_LIST", "pro"),  # 生产环境
              'pro_version_name': config.get("PRO_NAME", "pro_version_name"),  # 生产环境版本号
              'updateinfo': config.get("UPDATE", "updateinfo"),  # 升级信息
              'updatetype': config.get("UPDATE", "updatetype"),  # 升级类型
              'update_channel': config.get("UPDATE", "update_channel"),  # 升级渠道
              }
# 模块与分支映射
branch_map = {'prja': config.get("BRANCH_MAP", "prja"),  # prjA工程的分支
              'prjb': config.get("BRANCH_MAP", "prjb"),  # prjB工程的分支
              'utility': config.get("BRANCH_MAP", "utility"),  # utility工程的分支
              }

# 邮件主题
MAIL_SUBJECT = '邮件'


# 获取环境列表(1表示打包该环境,0表示不打包该环境)
def get_env():
    env_list = []
    env = config.get("ENV_LIST", "environment")

    dev_val = config.get("ENV_LIST", "dev")
    test_val = config.get("ENV_LIST", "test")
    pre_val = config.get("ENV_LIST", "pre")
    pro_val = config.get("ENV_LIST", "pro")

    if env == 'internet':
        env_list = {'INTERNET_DEV': dev_val,
                    'INTERNET_TEST': test_val,
                    'INTERNET_PRE': pre_val,
                    'INTERNET_PRO': pro_val}
    elif env == 'ta':
        env_list = {'taDEV': dev_val,
                    'taTEST': test_val,
                    'taPRE': pre_val,
                    'taPRO': pro_val}

    return env_list


# 环境列表
ENV_LIST = get_env()


# 根据不同的环境获取应用不同的中文名称
def get_child_app_name():
    env = config.get("ENV_LIST", "environment")
    if env == 'internet':
        return '自定义工程1'
    else:
        return '自定义工程2'


# {工程类型: [英文名称,中文名称,描述,更新说明,包名]}
app_dict = {
    prja: ['prja-', '测试版-A', '测试版-A', config.get("UPDATE", "updateinfo", ''), 'abc.example.com.prja'],
    prjb: ['prjb-', '测试版-B', '测试版-B', config.get("UPDATE", "updateinfo", ''), 'abc.example.com.prjb'],
}


# 环境列表
def get_path_list():
    sum_list = [os.path.join(PCP_BASE_PATH, x) for x in ENV_LIST]
    return sum_list


logging.config.fileConfig('config/log.conf')
logger = logging.getLogger('main')


# 备份日志文件
def copy_log_file():
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    log_path = os.path.join(sys.path[0], 'log')
    old_log = os.path.join(log_path, 'deploy.log')
    new_log = os.path.join(log_path, t + '.log')
    try:
        shutil.copy(old_log, new_log)
    except Exception, e:
        logger.error(e)


# 配置日志
copy_log_file()


# 获取apk路径
def get_output_apk():
    try:
        date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取所有目录
        path_list = get_path_list()
        # 获取该渠道所在的目录
        path = path_list[path_list.index(os.path.join(PCP_BASE_PATH, QUDAO))]
        local_path = os.path.join(sys.path[0], path, config_map['prj_type'], date_path) + os.sep
        files = os.listdir(local_path)
        for f in files:
            if f.find('.apk') != -1:
                return local_path + f
    except Exception, e:
        logger.error(e)
        raise e


# 读取全局版本号
def read_global_version_code():
    pro_file = 'config/version_code.properties'
    config_parser = ConfigParser.ConfigParser()
    config_parser.read(pro_file)
    os.chdir(sys.path[0])
    item = None
    if config_map['prj_type'] == prja:
        item = 'prja_code'
    elif config_map['prj_type'] == prjb:
        item = 'prjb_code'
    return config_parser.get("VERCODE", item)


# 读取版本名称信息
def read_version_name_from_file():
    current_file = None
    os.chdir(sys.path[0])
    if config_map['prj_type'] == prja:
        current_file = 'config/version_name_prja'
    elif config_map['prj_type'] == prjb:
        current_file = 'config/version_name_prjb'

    if not os.path.exists(current_file):
        # 文件不存在,创建
        logger.error(current_file + " 文件不存在!")
        exit(0)

    # 打开文件
    with open(current_file, 'rb') as f:
        version_dict = pickle.load(f)
    return version_dict, current_file
