# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : api_4_3rd.py
# @Description: these wrapped apis for third party


from .core_api import BaseAPI

class TestLogin(BaseAPI):
    url = 'http://54.212.1.235/!/upm/api/appUserLogin'
    method = "POST"
    headers = {"Content-Type": "application/json",
               "timestamp": "15989471111",
               "randomStr": "sample1234567",
               "token": "c74755f9be60c8829dd1bce984bc039830367ca08659f5a4a08075aa94c546a6a342afa390e364f7a2810569ab9bd9309e4beb129090abc4c8995b69aebf7ce2",
               "appId": "DSP"
               }


class TestSegmentList(BaseAPI):
    url = "http://54.212.1.235:9102/api/v1/dsp/segments?pageIndex=1&pageSize=30"
    method = 'GET'
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'application-Type': 'dsp'
    }

    def set_token(self, token):
        self.headers.update({"X-token": token})
        return self
