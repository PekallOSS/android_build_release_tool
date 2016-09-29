# -*- coding: utf-8 -*-
import os
import socket
import sys
import time
from ftplib import FTP

import app_name
import constant


class Ftp:
    CONST_HOST = "192.168.20.130"
    CONST_PORT = 21
    CONST_USERNAME = "user"
    CONST_PWD = "12356"
    CONST_BUFFER_SIZE = 8192
    ftp = None

    def __init__(self):
        pass

    # 链接ftp服务器
    def connect(self):
        constant.logger.info("连接ftp服务器......")
        try:
            self.ftp = FTP()
            self.ftp.set_debuglevel(2)
            self.ftp.connect(self.CONST_HOST, self.CONST_PORT)
            self.ftp.login(self.CONST_USERNAME, self.CONST_PWD)
            # Constant.logger.debug(self.ftp.getwelcome())
            self.ftp.set_debuglevel(0)
            return True
        except socket.error, socket.gaierror:
            constant.logger.error("FTP is unavailable,please check the host,username and password!")
            return False

    def close(self):
        self.ftp.close()

    # 上传文件
    def uploadfile(self, from_file, to_file):
        # 以读模式在本地打开文件
        file_handler = open(from_file, 'rb')

        # 上传文件
        try:
            self.ftp.storbinary('STOR %s' % to_file, file_handler, self.CONST_BUFFER_SIZE,
                                self.upload_complete(file_handler.name, to_file))
            file_handler.close()
            f1_size = self.ftp.size(to_file)
            f2_size = os.path.getsize(from_file)
            if f1_size != f2_size:
                constant.logger.info("上传文件大小不一致!")
                constant.logger.info(from_file + " 本地文件大小: " + f2_size)
                constant.logger.info(to_file + " 远程文件大小: " + f1_size)
        except Exception, e:
            constant.logger.error(from_file + "上传失败!\n" + e.message)
            raise e

    # #创建日期目录
    def create_date_path(self, path, date_path):
        cur_path = os.sep + os.path.join(path, constant.config_map['prj_type'])
        self.ftp.cwd(cur_path)
        ftp_f_list = self.ftp.nlst()
        # 创建日期目录
        if date_path not in ftp_f_list:
            self.ftp.mkd(date_path)
            # if (cur_path.find("INTERNET_PRO") > -1):
            # self.ftp.mkd(os.path.join(date_path, 'apk_sign'))

    # 上传文件
    def transfer(self, path):
        date_path = time.strftime('%Y%m%d', time.localtime(time.time()))
        local_path = os.path.join(path, constant.config_map['prj_type'], date_path) + os.sep

        # #创建日期目录
        self.create_date_path(path, date_path)

        os.chdir(sys.path[0])

        files = os.listdir(local_path)

        for f in files:
            # 目录不处理
            if os.path.isdir(os.path.join(local_path, f)):
                continue
            version_dict, current_file = constant.read_version_name_from_file()
            # 多环境
            if constant.QUDAO in version_dict.keys():
                self.uploadfile(local_path + f,
                                os.sep + local_path
                                + app_name.name_dict[constant.config_map['prj_type']][constant.QUDAO])


    #上传文件,查找所在渠道目录
    def main(self):
        constant.logger.info("\n------上传FTP------")
        if self.connect() is False:
            exit(0)

        # 创建ftp环境,多渠道,多渠道集中目录
        self.createFtpPath()

        # 获取目录列表
        path_list = constant.get_path_list()

        for constant.QUDAO, on in constant.ENV_LIST.items():
            # 保存当前环境
            if on == '1':
                # 获取该渠道所在的目录
                path = path_list[path_list.index(os.path.join(constant.PCP_BASE_PATH, constant.QUDAO))]
                self.transfer(path)
        self.close()
        constant.logger.info("上传完成.")

    # 创建ftp目录
    def createFtpPath(self):
        # 进入\storage\pcp目录
        cur_path = os.sep + constant.PCP_BASE_PATH
        self.ftp.cwd(cur_path)

        # 遍历环境渠道列表,获取名称
        env_channel_list = [key for key, value in constant.ENV_LIST.items()]

        # 遍历环境列表
        for q in env_channel_list:
            self.ftp.cwd(cur_path)
            try:
                self.ftp.mkd(q)
            except Exception, e:
                constant.logger.debug(e)
            self.ftp.cwd(cur_path + os.sep + q)
            path = self.ftp.nlst()

            # 创建目录
            if constant.prja not in path:
                self.ftp.mkd(constant.prja)
            if constant.prjb not in path:
                self.ftp.mkd(constant.prjb)
