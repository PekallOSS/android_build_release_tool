# -*- coding: utf-8 -*-
import constant

__author__ = 'yanghai'

# prjA名称
dict_parent_name = {'INTERNET_DEV': 'prja-int-dev.apk',
                    'INTERNET_TEST': 'prja-int-test.apk',
                    'INTERNET_PRE': 'prja-int-pre.apk',
                    'INTERNET_PRO': 'prja-int-pro.apk',
                    'ta_DEV': 'prja-ta-dev.apk',
                    'ta_TEST': 'prja-ta-test.apk',
                    'ta_PRE': 'prja-ta-pre.apk',
                    'ta_PRO': 'prja-ta-pro.apk'}
# prjB名称
dict_child_name = {'INTERNET_DEV': 'prjb-int-dev.apk',
                   'INTERNET_TEST': 'prjb-int-test.apk',
                   'INTERNET_PRE': 'prjb-int-pre.apk',
                   'INTERNET_PRO': 'prjb-int-pro.apk',
                   'ta_DEV': 'prjb-ta-dev.apk',
                   'ta_TEST': 'prjb-ta-test.apk',
                   'ta_PRE': 'prjb-ta-pre.apk',
                   'ta_PRO': 'prjb-ta-pro.apk'}


# 工程类型映射app名称
name_dict = {constant.prja: dict_parent_name,
             constant.prjb: dict_child_name}
