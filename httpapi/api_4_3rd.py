# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : api_4_3rd.py
# @Description: these wrapped apis for third party

import os

from httpapi.core_api import BaseAPI
from httpapi.parse import _load_yaml_file
from httpapi.core_api import *
from httpapi.api_log import *

yaml_file_path = os.path.dirname(os.path.abspath(__file__))
yaml_file_whole_path = os.sep.join([yaml_file_path, 'config.yml'])

logger.debug(f"{yaml_file_whole_path}")
yaml_content = _load_yaml_file(yaml_file_whole_path)


class StringEmptyError(Exception):
    pass


def concat_url(host, port, path):
    print(host, port, path)
    if port:
        url = f"{host}:{port}/{path}"
    elif host:
        url = f"{host}/{path}"
    else:
        raise StringEmptyError
    return url


class TestLogin(BaseAPI):
    host = yaml_content['config']['host']
    path = '!/upm/api/appUserLogin'
    url = concat_url(host, port=None, path=path)

    logger.debug(f"The login url is {url}")

    method = "POST"
    headers = {"Content-Type": "application/json",
               "timestamp": "15989471111",
               "randomStr": "sample1234567",
               "token": "c74755f9be60c8829dd1bce984bc039830367ca08659f5a4a08075aa94c546a6a342afa390e364f7a2810569ab9bd9309e4beb129090abc4c8995b69aebf7ce2",
               "appId": "DSP"
               }


class TestSegmentList(BaseAPI):
    host = yaml_content['config']['host']
    port = yaml_content['config']['port']
    path = 'api/v1/dsp/segments'
    url = concat_url(host, port=port, path=path)

    logger.debug(f"The login url is {url}")

    method = 'GET'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'application-Type': 'dsp'
    }

    def set_token(self, token):
        self.headers.update({"X-token": token})
        return self
