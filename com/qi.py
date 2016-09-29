# -*- coding: utf-8 -*-
# 首先安装　sudo pip install qiniu
import os
import subprocess
import sys

from qiniu import put_file, etag, Auth

import app_name
import constant


class Qiniu:
    czsh_dict = {'bucket_name': 'test',
                 'access_key': '121',
                 'secret_key': '222'}
    # prjA下载地址
    qiniu_prja_download_url = {'INTERNET_DEV': 'http://7viij6.com1.z0.glb.clouddn.com/prja-int-dev.apk',
                               'INTERNET_TEST': 'http://7viij6.com1.z0.glb.clouddn.com/prja-int-test.apk',
                               'INTERNET_PRE': 'http://7viij6.com1.z0.glb.clouddn.com/prja-int-pre.apk',
                               'INTERNET_PRO': 'http://7viij6.com1.z0.glb.clouddn.com/prja-int-pro.apk',
                               'taDEV': 'http://7viij6.com1.z0.glb.clouddn.com/prja-ta-dev.apk',
                               'taTEST': 'http://7viij6.com1.z0.glb.clouddn.com/prja-ta-test.apk',
                               'taPRE': 'http://7viij6.com1.z0.glb.clouddn.com/prja-ta-pre.apk',
                               'taPRO': 'http://7viij6.com1.z0.glb.clouddn.com/prja-ta-pro.apk'}

    # prjB下载地址
    qiniu_prjB_download_url = {'INTERNET_DEV': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-int-dev.apk',
                               'INTERNET_TEST': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-int-test.apk',
                               'INTERNET_PRE': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-int-pre.apk',
                               'INTERNET_PRO': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-int-pro.apk',
                               'taDEV': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-ta-dev.apk',
                               'taTEST': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-ta-test.apk',
                               'taPRE': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-ta-pre.apk',
                               'taPRO': 'http://7viij6.com1.z0.glb.clouddn.com/prjb-ta-pro.apk'}

    # 工程类型映射app下载地址
    url_dict = {constant.prja: qiniu_prja_download_url,
                constant.prjb: qiniu_prjB_download_url}

    # 七牛空间字典
    bucket_dict = {constant.prja: czsh_dict,
                   constant.prjb: czsh_dict}

    # 认证
    auth = None

    # 上传文件
    def upload_apk(self, apk_name, file):
        self.auth = Auth(self.bucket_dict[constant.config_map['prj_type']]['access_key'],
                         self.bucket_dict[constant.config_map['prj_type']]['secret_key'])

        mime_type = "application/vnd.android.package-archive"
        token = self.auth.upload_token(self.bucket_dict[constant.config_map['prj_type']]['bucket_name'], apk_name)
        ret, info = put_file(token, apk_name, file, mime_type=mime_type, check_crc=True)
        if info.status_code == 200 and ret['key'] == apk_name and ret['hash'] == etag(file):
            # 刷新
            self.refresh(file)
            pass
        else:
            constant.logger.error("上传失败! " + str(info.text_body) + '   ' + file)

    # 由于cdn缓存问题,需要手动刷新,利用七牛提供工具:qrsctl
    def refresh(self, file):
        os.chdir(sys.path[0])
        try:
            # 登录
            login_info = {constant.prja: 'sd@dd.com ssds',
                          constant.prjb: 'sd@dd.com ssds'}

            loing_url = './qiniu-devtools/./qrsctl login {}'.format(login_info[constant.config_map['prj_type']])
            (stdoutput, erroutput) = subprocess.Popen(loing_url, stderr=subprocess.STDOUT, shell=True).communicate()

            # 刷新
            cache_url_dict = {constant.prja: ['test', 'http://7viij6.com1.z0.glb.clouddn.com'],
                              constant.prjb: ['test', 'http://7viij6.com1.z0.glb.clouddn.com']}

            url = './qiniu-devtools/./qrsctl cdn/refresh {} {}/{}'.format(
                cache_url_dict[constant.config_map['prj_type']][0],
                cache_url_dict[constant.config_map['prj_type']][1],
                app_name.name_dict[constant.config_map['prj_type']][
                    constant.QUDAO]),

            (stdoutput, erroutput) = subprocess.Popen(url, stderr=subprocess.STDOUT, shell=True).communicate()

            constant.logger.info('七牛:  ' + str(self.url_dict[constant.config_map['prj_type']][constant.QUDAO]))
        except subprocess.CalledProcessError, e:
            constant.logger.error("上传失败!  " + e.cmd + '\n' + e.output)

    # 循环上传文件
    def main(self):
        constant.logger.info('\n------上传七牛------')
        # 变量环境列表
        for constant.QUDAO, on in constant.ENV_LIST.items():
            if on == '1':
                file = constant.get_output_apk()
                if file is not None and os.path.exists(file):
                    # 上传
                    self.upload_apk(app_name.name_dict[constant.config_map['prj_type']][constant.QUDAO], file)
                else:
                    constant.logger.info('{}环境下文件不存在!'.format(constant.QUDAO))
