# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : testcases.py
# @Description: these wrapped apis for third party

import os
import time

from typing import Text, Any, Union, Callable

from httpapi.model import TConfig, TRequest, TestCase, TStep

from httpapi.core import BaseAPI
from httpapi.parse import load_yaml_file
from httpapi.core import *
from httpapi.log import *
from httpapi.exceptions import StringEmptyError
from httpapi.log import get_project_metadata
from httpapi.exceptions import StringEmptyError

yaml_file_path = os.path.dirname(os.path.abspath(__file__))
yaml_file_whole_path = os.sep.join([yaml_file_path, 'config.yml'])

logger.debug(f"{yaml_file_whole_path}")
yaml_content = load_yaml_file(yaml_file_whole_path)


def concat_url(host, port, path):
    print(host, port, path)
    if port:
        url = f"{host}:{port}/{path}"
    elif host:
        url = f"{host}{path}"
    else:
        raise StringEmptyError
    return url


class TestLogin(BaseAPI):
    host = yaml_content['config']['host']
    path = yaml_content['path']['login']
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
    path = yaml_content['path']['segment_list']
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


def case_start(name):
    log_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    project_root_dir = get_project_metadata()
    if name:
        log_path = os.path.join(project_root_dir, "logs",
                                f"{name}_{log_time}.run.log")
        log_handler = logger.add(log_path, level="DEBUG")
        return log_handler
    else:
        raise StringEmptyError


class Config:
    def __init__(self, name: Text):
        self.__name = name
        self.__variables = {}
        self.__base_url = ""
        self.__verify = False
        self.__export = []
        self.__weight = 1

    @property
    def name(self) -> Text:
        return self.__name

    @property
    def weight(self) -> int:
        return self.__weight

    def variables(self, **variables) -> "Config":
        self.__variables.update(variables)
        return self

    def base_url(self, base_url: Text) -> "Config":
        self.__base_url = base_url
        return self

    def verify(self, verify: bool) -> "Config":
        self.__verify = verify
        return self

    def export(self, *export_var_name: Text) -> "Config":
        self.__export.extend(export_var_name)
        return self

    def locust_weight(self, weight: Text) -> "Config":
        self.__weight = weight
        return self

    def perform(self) -> TConfig:
        return TConfig(
            name=self.__name,
            base_url=self.__base_url,
            verify=self.__verify,
            variables=self.__variables,
            export=list(self.__export),
            path=self.__path,
            weight=self.__weight,
        )


class Step:
    def __init__(self, step_context):
        self.__step_context = step_context.perform()

    @property
    def request(self) -> TRequest:
        return self.__step_context.request

    @property
    def testcase(self) -> TestCase:
        return self.__step_context.testcase

    def perform(self) -> TStep:
        return self.__step_context
