# -*- coding: utf-8 -*-
import os
import subprocess

__author__ = 'yanghai'


# 标签操作类
class Tag:
    child_path = "/home/yanghai/work/projects/pcp/pcp_child"
    parent_path = "/home/yanghai/work/projects/pcp/pcp_parent_android"
    pekallandroidutility_path = '/home/yanghai/work/projects/pcp/pekallandroidutility'

    def __init__(self):
        pass

    # 删除本地tag
    def delete_tag(self):

        path = os.getcwd()
        os.chdir(path + "/tag")

        with open('tags.txt', 'r') as f:
            tag_list = f.readlines()

        os.chdir(self.pekallandroidutility_path)
        for tag in tag_list:
            (stdoutput, erroutput) = subprocess.Popen("git tag -d {0}".format(tag.strip()), stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE, shell=True).communicate()
            if stdoutput == '':
                print(erroutput)
            else:
                print(stdoutput)
            (stdoutput, erroutput) = subprocess.Popen('git push origin --delete tag {}'.format(tag),
                                                      stderr=subprocess.PIPE,
                                                      stdout=subprocess.PIPE,
                                                      shell=True).communicate()
            if stdoutput == '':
                print(erroutput)
            else:
                print(stdoutput)


Tag().delete_tag()
