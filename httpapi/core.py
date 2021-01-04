# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : testcases.py
# @Description: core api for calling the requests API

import json
import os
import time
from datetime import datetime
from typing import List, Dict, Text, NoReturn

import requests
from loguru import logger

from httpapi.model import (
    TConfig,
    TStep,
    VariablesMapping,
    StepData,
    TestCaseSummary,
    TestCaseTime,
    TestCaseInOut,
    ProjectMeta,
    TestCase
)
from httpapi.testcases import Config, Step
from httpapi.client import HttpSession
from httpapi.loader import load_project_data


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
        logger.debug(f"the params of the instance is {self.params}")
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
            logger.debug(f"The extract key is {_key}")
            if isinstance(value, requests.Response):
                if _key == 'json':
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value,
                            (requests.structures.CaseInsensitiveDict, dict)):
                value = value[_key]
            logger.debug(f"The extract value is {value}")
        return value

    def validate(self, key, expected_value):
        assert self.extract(key) == expected_value
        return self

    def get_response(self):
        return self.response


class HttpAPI:
    config: Config
    test_steps: List[Step]

    success: bool = False
    __config: TConfig
    __test_steps: List[TStep]
    __project_meta: ProjectMeta = None
    __case_id: Text = ""
    __export: List[Text] = []
    __step_data: List[StepData] = []
    __session: HttpSession = None
    __session_variables: VariablesMapping = {}

    # time
    __start_at: float = 0
    __duration_: float = 0
    # log
    __log_path: Text = ""

    def __init_tests__(self) -> NoReturn:
        self.__config = self.config.perform()
        self.__test_steps = [step.perform() for step in self.test_steps]

    @property
    def raw_testcase(self) -> TestCase:
        if not hasattr(self, "__config"):
            self.__init_tests__()

        return TestCase(config=self.__config, test_steps=self.__test_steps)

    def with_project_meta(self, project_meta: ProjectMeta) -> "HttpAPI":
        self.__project_meta = project_meta
        return self

    def with_session(self, session: HttpSession) -> "HttpAPI":
        self.__session = session
        return self

    def with_case_id(self, case_id: Text) -> "HttpAPI":
        self.__case_id = case_id
        return self

    def with_variables(self, variables: VariablesMapping) -> "HttpAPI":
        self.__session_variables = variables
        return self

    def with_export(self, export: List[Text]) -> "HttpAPI":
        self.__export = export
        return self

    def test_start(self, param: Dict = None) -> "HttpAPI":
        self.__init_tests__()
        self.__project_meta = self.__project_meta or load_project_data(
            self.__config.path)
        self.__case_id = self.__case_id
        self.__log_path = self.__log_path or os.path.join(
            self.__project_meta.RootDir,
            "logs",
            f"{self.__case_id}.run.log")
        log_handler = logger.add(self.__log_path, level="DEBUG")

        # parse config name
        config_variables = self.__config.variables
        if param:
            config_variables.update(param)
        config_variables.update(self.__session_variables)
