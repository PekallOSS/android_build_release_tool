# -*- coding: utf-8 -*-
import ConfigParser
import fnmatch
import os
import pickle
import shutil
import subprocess
import sys
import time

import app_name
import constant
import utility


class Build:
    # 版本名称
    version_name_file = "version_name"
    # 版本号
    version_code_file = "version_code"
    # 当前日期
    date_path = time.strftime('%Y%m%d', time.localtime(time.time()))

    def __init__(self):
        pass

    # 更新版本号
    def update_version_code(self):
        # 获取全局版本号
        ver_code = self.get_global_version_code()

        os.chdir(constant.path_map[constant.config_map['prj_type']])
        ver_code_file = os.path.join(constant.path_map[constant.config_map['prj_type']], self.version_code_file)
        # 读取version_code文件
        with open(ver_code_file, 'w')as f:
            f.write(ver_code)
            constant.logger.info("版本号： " + ver_code)

    # 更新version_name
    def update_version_name(self):
        # 版本名称持久化到文件
        self.write_version_name_to_file()

        # 从脚本配置文件中读取版本名称
        version_dict = constant.read_version_name_from_file()[0]

        # 将版本名称写入项目工程版本名称文件
        os.chdir(constant.path_map[constant.config_map['prj_type']])
        ver_name_file = os.path.join(constant.path_map[constant.config_map['prj_type']], self.version_name_file)
        ver_name = version_dict[constant.QUDAO]
        with open(ver_name_file, 'w') as f:
            f.write(ver_name)
            constant.logger.info("版本名称:" + ver_name)

    # 打包编译
    def gradle_prj(self):
        constant.logger.info('\n正在生成APK,请等待......')
        os.chdir(constant.path_map[constant.config_map['prj_type']])

        (stdoutput, erroutput) = subprocess.Popen('gradle clean', stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  shell=True).communicate()
        # 生产环境编译release版本

        child = subprocess.Popen('gradle assemble{} -PconfigurationName={}'.format(constant.QUDAO, constant.QUDAO),
                                 stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE, shell=True)

        (stdoutput, erroutput) = child.communicate()
        if stdoutput.find('BUILD FAILED') != -1:
            constant.logger.info(stdoutput)
            constant.logger.error(erroutput)
            exit(0)
        else:
            # 复制文件
            self.copy_file()

    # 搜索指定的文件
    def find_files(self, path, fnexp):
        for root, dirs, files in os.walk(path):
            for filename in fnmatch.filter(files, fnexp):
                yield os.path.join(root, filename)

    def copy_file(self):
        # 获取4个环境目录
        path_list = constant.get_path_list()
        # 获取该环境所在的目录
        path = path_list[path_list.index(os.path.join(constant.PCP_BASE_PATH, constant.QUDAO))]

        list = []
        # 搜索apk文件
        for filename in self.find_files(constant.path_map[constant.config_map['prj_type']], '*.apk'):
            if filename.find('build/outputs/apk') != -1:
                list.append(filename)

        # 搜索指定文件
        for f in list:
            # 过滤掉未签名的apk
            if f.lower().find('unaligned') != -1:
                continue

            map = constant.config_map

            # 定义apk名称
            apk = os.path.join(sys.path[0], path,
                               constant.config_map['prj_type'],
                               self.date_path,
                               app_name.name_dict[constant.config_map['prj_type']][constant.QUDAO])

            shutil.copyfile(f, apk)
            constant.logger.info(f + " 拷贝到 " + apk)

    # 写入版本名称:
    def write_version_name_to_file(self):
        # 读取版本名称
        version_dict, current_file = constant.read_version_name_from_file()
        # 持久化新版本名称
        self.write_new_version_name(version_dict, current_file)

    # 持久化新版本名称
    def write_new_version_name(self, version_dict, current_file):
        # 获取旧版本名称
        verName = version_dict[constant.QUDAO]

        # 生产环境下的新版本名称
        if constant.QUDAO.find('PRO') != -1:
            version_dict[constant.QUDAO] = constant.config_map['pro_version_name']
        # 非生产环境下的新版本名称
        else:
            # 今天是否编译过(检查日期)
            if verName[1:5] == self.date_path[4:8]:
                # 编译多次吗
                pos = verName.find('RC')
                if pos == -1:
                    # 编译过一次
                    s = version_dict[constant.QUDAO] + '-RC2'
                    version_dict[constant.QUDAO] = s
                else:
                    # 编译过多次
                    n = verName[0:verName.find('RC') + 2]
                    c = int(verName[verName.find('RC') + 2]) + 1
                    version_dict[constant.QUDAO] = n + str(c)
                    pass
            # 今天没编译
            else:
                version_dict[constant.QUDAO] = 'v' + self.date_path[4:8] + '_' + constant.QUDAO

        ver_name = version_dict[constant.QUDAO]

        ver_name = ver_name.replace('intel', 'CL_').replace('ta', 'TA_').replace('DEV', '_D').replace('TEST', '_T') \
            .replace('PRO', '_P').replace('__', '_')

        # 防止版本号长度超过20字节,版本号截取
        version_dict[constant.QUDAO] = ver_name.replace('INTERNET', 'INT').replace('STUDENT', 'S')

        # 写入文件
        with open(current_file, 'wb') as f:
            pickle.dump(version_dict, f)

    # 获取全局版本号,版本号加１
    def get_global_version_code(self):
        pro_file = 'config/version_code.properties'
        os.chdir(sys.path[0])
        config = ConfigParser.ConfigParser()
        config.read(pro_file)
        if constant.config_map['prj_type'] == constant.prja:
            item = 'prjA_code'
        elif constant.config_map['prj_type'] == constant.prjb:
            item = 'prjB_code'
        old_ver_code = config.get("VERCODE", item)
        new_ver_code = int(old_ver_code) + 1
        config.set('VERCODE', item, new_ver_code)
        config.write(open(pro_file, 'w'))
        #self.push_global_version_code(new_ver_code)
        return str(new_ver_code)

    # 推送版本号
    def push_global_version_code(self, ver_code):
        (stdoutput, erroutput) = subprocess.Popen(
            'git commit -m "{}升级版本号:{}" config/version_code.properties'
                .format(constant.config_map['prj_type'], str(ver_code)),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            shell=True).communicate()

        (stdoutput, erroutput) = subprocess.Popen(
            'git push ', stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()
        print stdoutput
        print erroutput

    # 读取分支名称
    def read_branch(self):
        config = ConfigParser.ConfigParser()
        config.read('config/const.properties')
        return config.get("BRANCH", "branch")

    # 切换分支
    def switch_branch(self):
        # 读取分支
        branch = self.read_branch()

        # 切换到工程目录
        os.chdir(constant.path_map[constant.config_map['prj_type']])

        constant.logger.info("切换分支: {}".format(branch))
        (stdoutput, erroutput) = subprocess.Popen('git checkout {}'.format(branch), stderr=subprocess.PIPE,
                                                  stdout=subprocess.PIPE,
                                                  shell=True).communicate()
        if erroutput.find('error') >= 0:
            # subprocess.Popen('git stash', stderr=subprocess.PIPE, stdout=subprocess.PIPE,
            # shell=True).communicate()
            constant.logger.error("切换分支错误: " + erroutput)
            exit(0)

        # 检测是否已切换指定分支
        (stdoutput, erroutput) = subprocess.Popen('git branch', stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  shell=True).communicate()

        i = stdoutput.split('\n').index('* ' + branch)
        constant.logger.info("当前分支: " + stdoutput.split('\n')[i])

        (stdoutput, erroutput) = subprocess.Popen('git pull', stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                                  shell=True).communicate()
        constant.logger.info('拉取最新代码：' + stdoutput)

    def main(self):
        # 拉取各个模块代码
        prj_branch = utility.PrjBranch()
        prj_branch.pull_code()

        # 更新版本号
        self.update_version_code()

        # 遍历环境并编译
        for constant.QUDAO, on in constant.ENV_LIST.items():
            # 如开启,则编译
            if on == '1':
                constant.logger.info('\n编译渠道:' + constant.QUDAO)
                # 跟新版本名称
                self.update_version_name()

                # 编译
                self.gradle_prj()

                # 打标签
                prj_branch.tag()

        # 内容重置
        prj_branch.reset()
