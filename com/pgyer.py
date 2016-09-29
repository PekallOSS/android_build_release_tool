# -*- coding: utf-8 -*-
# 首先安装:sudo easy_install poster
import json
import os
import requests

import constant


class Pqyer:
    # 存储userKey,apiKey,孩子端下载地址,家长端下载地址
    token_dict = {'INTERNET_DEV': ['123456', '654321',
                                   'http://www.pgyer.com/prjAintdev', 'http://www.pgyer.com/prjBintdev'],
                  'INTERNET_TEST': ['123456', '654321',
                                    'http://www.pgyer.com/prjAinttest', 'http://www.pgyer.com/prjBinttest'],
                  'INTERNET_PRE': ['123456', '654321',
                                   'http://www.pgyer.com/prja', 'http://www.pgyer.com/prjb'],
                  'INTERNET_PRO': ['123456', '654321',
                                   'http://www.pgyer.com/prjAintpro', 'http://www.pgyer.com/prjBintpro'],
                  'taDEV': ['123456', '654321',
                            'http://www.pgyer.com/prjAtadev', 'http://www.pgyer.com/prjBtadev'],
                  'taTEST': ['123456', '654321',
                             'http://www.pgyer.com/prjAtatest', 'http://www.pgyer.com/prjBtatest'],
                  'taPRE': ['123456', '654321',
                            'http://www.pgyer.com/prjAtapre', 'http://www.pgyer.com/prjBtapre'],
                  'taPRO': ['123456', '654321',
                            'http://www.pgyer.com/prjAtapro', 'http://www.pgyer.com/prjBtapro']
                  }

    # 项目类型映射token字典
    prj_token = {constant.prja: token_dict,
                 constant.prjb: token_dict}

    # 上传apk
    def upload_apk(self, list, file):
        r = requests.post('http://www.pgyer.com/apiv1/app/upload', files={'file': open(file, 'rb')},
                          data={"uKey": list[0], "_api_key": list[1]})
        if r.status_code == 200:
            try:
                d = json.loads(r.content)
                self.update_app_info(d['data']['appKey'], list, file)
            except Exception, e:
                constant.logger.error("上传完成,但解析返回的信息出错:" + e.message)
                return -1
        else:
            constant.logger.error("上传失败! " + str(r.status_code) + ", " + r.content)
            return -1

    # 修改上传的apk信息
    def update_app_info(self, app_key, list, file):
        values = {'aKey': app_key,
                  'uKey': list[0],
                  '_api_key': list[1],
                  'appName': constant.app_dict[constant.config_map['prj_type']][1],
                  'appUpdateDescription': constant.app_dict[constant.config_map['prj_type']][3],
                  'appDescription': constant.app_dict[constant.config_map['prj_type']][2],
                  'appVersion': constant.read_global_version_code()}

        r = requests.post('http://www.pgyer.com/apiv1/app/update', data=values)
        if r.status_code == 200:
            if constant.config_map['prj_type'] == constant.prja:
                info = list[2]
            elif constant.config_map['prj_type'] == constant.prjb:
                info = list[3]
            else:
                info = ''

            constant.logger.info('蒲公英:  ' + info)
        else:
            constant.logger.error('上传失败！ 发生在修改信息：' + str(r.status_code) + ',' + r.content + '    ' + file)

    def main(self):
        constant.logger.info('\n------上传蒲公英------')
        # 变量环境列表
        for constant.QUDAO, on in constant.ENV_LIST.items():
            if on == '1':
                file = constant.get_output_apk()
                if file is not None and os.path.exists(file):
                    self.upload_apk(self.prj_token[constant.config_map['prj_type']][constant.QUDAO], file)
                else:
                    constant.logger.info('{}环境下文件不存在!'.format(constant.QUDAO))
