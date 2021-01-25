# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 18:58
# @Author  : Gene Jiang
# @File    : testcases.py
# @Description: core api for calling the requests API

import json
import os
import time
import uuid
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
from httpapi.response import ResponseObject
from httpapi.testcases import Config, Step
from httpapi.client import HttpSession
from httpapi.loader import load_project_meta
from httpapi.utils import merge_variables
from httpapi.parser import parse_variable_mapping, parse_data, build_url
from httpapi.exceptions import ValidationFailure, ParamsError


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
    teststeps: List[Step]

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

        print(f"====={self.__config.path}")

        self.__test_steps = []

        for step in self.teststeps:
            print(f"The step is {step.perform()}")
            self.__test_steps.append(step.perform())

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

        self.__project_meta = self.__project_meta or load_project_meta(
            self.__config.path
        )

        self.__case_id = self.__case_id or str(uuid.uuid4())
        self.__log_path = self.__log_path or \
                          os.path.join(self.__project_meta.RootDir,
                                       "logs",
                                       f"{self.__case_id}.run.log")
        log_handler = logger.add(self.__log_path, level="DEBUG")

        # parse config name
        config_variables = self.__config.variables
        if param:
            config_variables.update(param)
        config_variables.update(self.__session_variables)
        self.__config.name = self.__config.name

        logger.info(
            f"Start to run testcase:{self.__config.name}, TecseCase ID:{self.__case_id}"
        )

        print(f"config={self.__config}, steps={self.__test_steps}")

        try:
            return self.run_testcase(
                TestCase(config=self.__config, test_steps=self.__test_steps)
            )
        finally:
            logger.remove(log_handler)
            logger.info(f"generate testcase log: {self.__log_path}")

    def __parse_config(self, config: TConfig) -> NoReturn:
        config.variables.update(self.__session_variables)
        config.variables = config.variables
        config.name = config
        config.base_url = config.base_url

    def run_testcase(self, testcase: TestCase) -> "HttpAPI":
        self.__config = testcase.config
        self.__test_steps = testcase.test_steps

        # prepare
        self.__project_meta = self.__project_meta or load_project_data(
            self.__config.path
        )

        self.__parse_config(self.__config)
        self.__start_at = time.time()
        self.__step_datas: List[StepData] = []
        self.__session = self.__session or HttpSession()
        extracted_variables: VariablesMapping = {}

        # run test step
        for step in self.__test_steps:
            step.variables = merge_variables(step.variables,
                                             extracted_variables)
            step.variables = merge_variables(step.variables,
                                             self.__config.variables)

            step.variables = parse_variable_mapping(
                step.variables, {}
            )

            extract_mapping = self.__run_step(step)
            extracted_variables.update(extract_mapping)

        self.__session_variables.update(extracted_variables)
        self.__duration = time.time() - self.__start_at

        return self

    def __run_step(self, step: TStep) -> Dict:
        logger.info(f"run step begin:{step.name} =========={step.request}==")

        if step.request:
            step_data = self.__run_step_request(step)
        elif step.test_case:
            step_data = self.__run_step_request(step)
        else:
            raise ParamsError(
                f"test step is not a request{step.dict()}"
            )

        self.__step_datas.append(step_data)
        logger.info(f"run the step end:{step.name} =============\n")
        return step_data.export_vars

    def __run_step_request(self, step: TStep) -> StepData:
        step_data = StepData(name=step.name)

        # parse
        # upload functions
        request_dict = step.request.dict()

        print(
            f"===={request_dict}==={step.variables}=={self.__project_meta.functions}===")
        parsed_request_dict = parse_data(
            request_dict, step.variables, self.__project_meta.functions
        )
        parsed_request_dict["headers"].setdefault(
            "HRUN-Request-ID",
            f"HRUN-{self.__case_id}-{str(int(time.time() * 1000))[-6:]}",
        )
        step.variables["requests"] = parsed_request_dict

        # prepare agruments
        method = parsed_request_dict.pop("method")
        url_path = parsed_request_dict.pop("url")
        url = build_url(self.__config.base_url, url_path)
        parsed_request_dict["verify"] = self.__config.verify
        parsed_request_dict["json"] = parsed_request_dict.pop("req_json", {})

        # request
        resp = self.__session.request(method, url, **parsed_request_dict)
        resp_obj = ResponseObject(resp)
        step.variables['response'] = resp_obj

        # extract
        extractors = step.extract
        extract_mapping = resp_obj.extract(extractors)
        step_data.export_vars = extract_mapping

        variables_mapping = step.variables
        variables_mapping.update(extract_mapping)

        # validate
        validators = step.validators
        session_success = False
        try:
            resp_obj.validate(
                validators, variables_mapping, self.__project_meta.functions
            )
            session_success = True
        except ValidationFailure:
            session_success = False
            self.__duration = time.time() - self.__start_at
            raise
        finally:
            self.success = session_success
            step_data.success = session_success

            if hasattr(self.__session, "data"):
                self.__session.data.success = session_success
                self.__session.data.validators = resp_obj.validation_results

                # save step data
                step_data.data = self.__session.data

        return step_data
