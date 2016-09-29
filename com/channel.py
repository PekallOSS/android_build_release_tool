# -*- coding: utf-8 -*-

import os
import shutil
import sys
import time
import zipfile

import constant

__author__ = 'yanghai'


# 多渠道打包类
class Channel:
    # 多渠道打包需要的环境环境
    src_env = 'INTERNET_PRO'

    channels = ['WANDOUJIA',
                'YINGYONGBAO',
                'YINGYONGHUI',
                'SANLIULINGSHOUJIZHUSHOU',
                'XIAOMISTORE',
                'vmall',
                'meizu',
                'anzhuoapk',
                'amsungapps',
                'lenovo',
                'nearme',
                'gfan',
                'yunos',
                'sogou',
                'mumayi',
                'eoemarket',
                'm10086',
                'nduoa',
                '163',
                'anzhi',
                'chengzhangshouhu',
                'BAIDUSHOUJIZHUSHOU',
                'JIUYIZHUSHOU',
                'ANDROIDMARKET']

    def main(self):
        if constant.QUDAO == None or 'INTERNET_PRO'.find(constant.QUDAO) != -1:
            return
        constant.logger.info('\n------生成多渠道包------')
        if self.has_apk():
            # 遍历渠道列表
            for item in self.channels:
                apk_file = self.copyfile(item)
                self.writeChannel(apk_file, item)
        constant.logger.info('位置: ' + self.get_dst_path())

    # 通道文件写入apk中
    def writeChannel(self, apk_file, item):
        empty_channel_file = os.path.join(sys.path[0], 'channel.txt')
        open(empty_channel_file, 'w').close()
        # 追加的方式打开apk文件
        zipFile = zipfile.ZipFile(apk_file, 'a', zipfile.ZIP_DEFLATED)
        # empty_channel_file写入apk中
        zipFile.write(empty_channel_file, "META-INF/channel_{channel}".format(channel=item))
        zipFile.close()
        os.remove(empty_channel_file)
        pass

    # 将src_env环境目录下的apk文件复制到多渠道目录下,返回当前渠道文件名
    def copyfile(self, channel_name):
        src_path = self.get_src_path()
        dst_path = self.get_dst_path()
        files = os.listdir(src_path)[1]
        if files.find('.apk') != -1:
            dst_file = ''
            # 家长端命名
            if constant.config_map['prj_type'].find(constant.prja) != -1:
                dst_file = dst_path + "prj_a_" + channel_name + ".apk"
            # 孩子端命名
            elif constant.config_map['prj_type'].find(constant.prjb) != -1:
                dst_file = dst_path + "prj_b_" + channel_name + ".apk"
            # 复制
            shutil.copyfile(src_path + files, dst_file)
            return dst_file

    # 将src_env环境目录下的apk文件复制到storage/pcp/channel/child或parent
    def copyfile_new(self):
        # '/home/yanghai/work/projects/build_tool_python/com/storage/pcp/INTERNET_PRO/child/20150820/'
        src_path = self.get_dst_path()
        # dst_path = self.getDstPath()
        dst_path = os.path.join(constant.PCP_BASE_PATH, 'channel', constant.config_map['prj_type'],
                                constant.QUDAO + '.apk')
        files = os.listdir(src_path)[0]
        if files.find('.apk') != -1:
            shutil.copyfile(src_path + files, dst_path)
            return dst_path

    # 是否有发布多渠道的源apk文件
    def has_apk(self):
        src_path = self.get_src_path()
        files = os.listdir(src_path)
        if len(files) == 0:
            constant.logger.info("互联网生产环境下没有发布apk文件,无法打包多渠道!")
            return False
        return True

    # 获取copy的目的地路径
    def get_dst_path(self):
        date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取/storage/pcp下的子目录
        path_list = constant.get_path_list()
        dst_path = path_list[path_list.index(os.path.join(constant.PCP_BASE_PATH, self.src_env))]
        dst_local_path = os.path.join(sys.path[0], dst_path, constant.config_map['prj_type'], date_path,
                                      'channel') + os.sep
        return dst_local_path

    # 获取源apk路径
    def get_src_path(self):
        date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
        # 获取/storage/pcp下的子目录
        path_list = constant.get_path_list()
        src_path = path_list[path_list.index(os.path.join(constant.PCP_BASE_PATH, self.src_env))]
        src_local_path = os.path.join(sys.path[0], src_path, constant.config_map['prj_type'], date_path) + os.sep
        return src_local_path
