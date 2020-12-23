# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : api_4_3rd.py
# @Description: core api for calling the requests API

import json
import requests
import loguru


session = requests.sessions.Session()


class BaseAPI:
    method = 'GET'
    url = ''
    params = {}
    headers = {}
    data = {}
    cookies = {}
    json = {}

    def __init__(self):
        self.response = None

    def set_params(self, **params):
        self.params = params
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_json(self, json_data):
        self.data = json.dumps(json_data)
        return self

    def set_cookies(self, **cookies):
        self.cookies = cookies
        return self

    def run(self, session=None):
        self.response = session.request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            headers=self.headers,
            cookies=self.cookies,
            json=self.json
        )

        return self

    def extract(self, field):
        value = self.response

        for _key in field.split("."):
            if isinstance(value, requests.Response):
                if _key == 'json':
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value,
                            (requests.structures.CaseInsensitiveDict, dict)):
                value = value[_key]

            print("The key1 is {}, the value1 is {}, the type(value)1 is {}! \
                    ".format(_key, value, type(value)))
        return value

    def validate(self, key, expected_value):
        assert self.extract(key) == expected_value
        return self

    def get_response(self):
        return self.response
