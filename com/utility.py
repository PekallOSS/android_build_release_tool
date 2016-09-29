# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import time
from collections import OrderedDict

import constant

__author__ = 'yanghai'


class PrjBranch:
    prja = constant.path_map[constant.prja]
    prjb = constant.path_map[constant.prjb]
    utility = constant.path_map[constant.utility]

    # {项目:{环境:{模块路径:分支}}}
    prj_branch_map = {
        constant.prja:
            {'internet': OrderedDict([(prja, constant.branch_map['prja']),
                                      (utility, constant.branch_map['utility'])]),
             'ta': OrderedDict([(prja, constant.branch_map['prja']),
                                (utility, constant.branch_map['utility'])])
             },
        constant.prjb:
            {'internet': OrderedDict([(prjb, constant.branch_map['prjb']),
                                      (utility, constant.branch_map['utility'])]),
             'ta': OrderedDict([(prjb, constant.branch_map['prjb']),
                                (utility, constant.branch_map['utility'])])
             }
    }

    def __init__(self):
        pass

    def pull_code(self):
        constant.logger.info('\n')
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        for prj_path, branch in items:
            self.pull_model_code(prj_path, branch)

    def tag(self):
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        for prj_path, branch in items:
            self.tag_model(prj_path)

    # 多模块打tag
    def tag_model(self, prj_path):
        # 非生产环境不打tag
        if constant.QUDAO.find('PRO') <= -1:
            return

        # 切换脚本运行目录
        os.chdir(sys.path[0])
        version_dict, current_file = constant.read_version_name_from_file()
        # 获取当前外部版本号
        ver_name = version_dict[constant.QUDAO]
        ver_code = constant.read_global_version_code()

        # tag = 外部版本号_内部版本号_发布日期
        tag = ver_name + "_" + ver_code + "_" + time.strftime('%Y%m%d', time.localtime(time.time()))
        try:
            # 切换到模块目录
            os.chdir(prj_path)
            (stdoutput, erroutput) = subprocess.Popen("git tag {0}".format(tag), stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE, shell=True).communicate()

            (stdoutput, erroutput) = subprocess.Popen('git push origin {}'.format(tag), stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      shell=True).communicate()

            constant.logger.info("模块位置:" + prj_path)

            if erroutput.find('[new tag]') < 0:
                constant.logger.info('推送标签{}出错:{}'.format(tag, erroutput))
            else:
                constant.logger.info('打入标签:{}'.format(tag))
        except Exception, e:
            constant.logger.error('打入标签错误:{}'.format(tag) + e.args[1])

    # 切换分支,拉取代码
    def pull_model_code(self, prj_path, branch):

        # 切换到工程目录
        os.chdir(prj_path)
        constant.logger.info("项目位置:" + prj_path)

        # 切换分支
        # Constant.logger.info("切换分支: {}".format(branch))
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

    # 创建发布分支
    def release_branch(self):
        # 先切换到各个模块的开发分支,并拉取代码
        self.pull_code()

        # 读取模块和分支对应map
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        # 获取分支名称
        branch_name = sys.argv[2]

        for prj_path, branch in items:
            # 切换到工程目录
            os.chdir(prj_path)
            # 创建分支
            (stdoutput, erroutput) = subprocess.Popen('git checkout -b ' + branch_name, stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      shell=True).communicate()
            if erroutput.find('error') >= 0:
                constant.logger.error(
                    "创建本地分支错误: " + prj_path[prj_path.rfind("/") + 1:] + "【" + branch_name + "】,  " + erroutput)
                exit(0)
            else:
                constant.logger.info("已创建本地分支: " + prj_path[prj_path.rfind("/") + 1:] + "【" + branch_name + "】")

            # 推送远程分支
            (stdoutput, erroutput) = subprocess.Popen('git push -u origin {}:{}'.format(branch_name, branch_name),
                                                      stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      shell=True).communicate()
            if erroutput.find('error') >= 0:
                constant.logger.error(
                    "创建远程分支错误: " + prj_path[prj_path.rfind("/") + 1:] + "【" + branch_name + "】,  " + erroutput)
                exit(0)
            else:
                constant.logger.info("已创建远程分支: " + prj_path[prj_path.rfind("/") + 1:] + "【" + branch_name + "】")

    # 删除本地,远程分支
    def delete_branch(self):
        # 先切换到各个模块的开发分支,并拉取代码
        self.pull_code()

        # 读取模块和分支对应map
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        # 获取分支名称
        branch_name = 'release_' + sys.argv[2] + '_branch'

        for prj_path, branch in items:
            # 切换到工程目录
            os.chdir(prj_path)
            constant.logger.info("模块位置:" + prj_path)

            # 查找分支是否存在
            s = self.has_branch(branch_name)

            if s['local_branch'] > 0:
                # 删除本地分支
                (stdoutput, erroutput) = subprocess.Popen('git branch -D ' + branch_name, stderr=subprocess.PIPE,
                                                          stdout=subprocess.PIPE,
                                                          shell=True).communicate()
                if erroutput.find('error') >= 0:
                    constant.logger.error("删除本地分支错误: " + branch_name + ",  " + erroutput)
                else:
                    constant.logger.info("已删除本地分支: " + branch_name)

            if s['remotes_branch'] > 0:
                # 删除远程分支
                (stdoutput, erroutput) = subprocess.Popen('git push origin :{}'.format(branch_name),
                                                          stderr=subprocess.PIPE,
                                                          stdout=subprocess.PIPE,
                                                          shell=True).communicate()
                if erroutput.find('error') >= 0:
                    constant.logger.error("删除远程分支错误: " + branch_name + ",  " + erroutput)
                else:
                    constant.logger.info("已删除远程分支: " + branch_name)

    # 查找本地和远程分支
    def has_branch(self, branch_name):
        s = {'local_branch': 0, 'remotes_branch': 0}
        # 查找分支
        (stdoutput, erroutput) = subprocess.Popen('git branch -a ', stderr=subprocess.PIPE,
                                                  stdout=subprocess.PIPE,
                                                  shell=True).communicate()
        if erroutput.find('error') >= 0:
            constant.logger.error("查找分支错误: " + branch_name + ",  " + erroutput)
            exit(0)
        else:
            if stdoutput.find(branch_name) < 0:
                constant.logger.info("本地分支不存在: " + branch_name)
            else:
                s['local_branch'] = 1
            if stdoutput.find('remotes/origin/' + branch_name) < 0:
                constant.logger.info("远程分支不存在: " + 'remotes/origin/' + branch_name)
            else:
                s['remotes_branch'] = 1
        return s

    # 查找本地和远程分支
    def query_branch(self):

        # 先切换到各个模块的开发分支,并拉取代码
        self.pull_code()

        # 读取模块和分支对应map
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        # 获取分支名称
        branch_name = 'release_' + sys.argv[2] + '_branch'

        info = ''
        branch_info = ''

        for prj_path, branch in items:
            # 切换到工程目录
            os.chdir(prj_path)
            constant.logger.info("模块位置:" + prj_path)

            # 查找分支是否存在
            s = self.has_branch(branch_name)
            if s['local_branch'] > 0:
                branch_info += prj_path[prj_path.rfind("/") + 1:] + '[本地,'
            if s['remotes_branch'] > 0:
                branch_info += '远程],'
        if branch_info != '':
            info = '发现' + branch_name + '分支,\n在' + branch_info + '有同名分支,\n请确认是否全部删除?'
        constant.logger.info(info)
        return info

    # 内容重置
    def reset(self):
        items = self.prj_branch_map[constant.config_map['prj_type']][constant.config_map['environment']].iteritems()
        for prj_path, branch in items:
            # 让工作目录回到上次提交时的状态:恢复项目中的version_name,version_code文件
            os.chdir(prj_path)
            subprocess.Popen('git reset --hard HEAD', stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                             shell=True).communicate()


if __name__ == '__main__':
    s = '创建分支: utility.py -a 分支名称\n' \
        '删除分支: utility.py -d 分支名称\n' \
        '查看分支: utility.py -l 分支名称\n' \
        '拉取分支: utility.py -p\n'
    if sys.argv.__len__() == 3:
        if sys.argv[1] == '-a':
            PrjBranch().release_branch()
        elif sys.argv[1] == '-d':
            PrjBranch().delete_branch()
        elif sys.argv[1] == '-l':
            PrjBranch().query_branch()
        else:
            print s
    elif sys.argv.__len__() == 2:
        if sys.argv[1] == '-p':
            PrjBranch().pull_code()
        else:
            print s
    else:
        print s
