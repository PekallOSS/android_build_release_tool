# -*- coding: utf-8 -*-
import os
import subprocess

__author__ = 'yanghai'


# 获取手机中家长端版本号
def get_version_from_phone():
    subprocess.call('adb shell dumpsys package com.jinyuc.pcp.parent', stderr=subprocess.STDOUT, shell=True)


# 获取指定apk版本号
def get_version(apk_file):
    apk_info_file = './tool/apkInfo.txt'
    subprocess.call('./tool/./aapt d badging {}'.format(apk_file), stdout=open(apk_info_file, 'w'), shell=True)
    s = open(apk_info_file, 'r').readlines()[0]
    ver_code = s.split(' ')[2].split('=')[1].replace("'", '')
    ver_name = s.split(' ')[3].split('=')[1].replace("'", '').replace('\n', '')
    os.remove(apk_info_file)
    # print("versionName={}, versionCode={}".format(versinoName, versionCode))
    return ver_code, ver_name
