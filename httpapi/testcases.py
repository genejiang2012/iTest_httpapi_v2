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

from httpapi.parser import load_yaml_file
from httpapi.core import *
from httpapi.log import *
from httpapi.exceptions import StringEmptyError
from httpapi.log import get_project_metadata
from httpapi.exceptions import StringEmptyError


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
