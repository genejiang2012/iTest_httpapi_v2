# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/31 14:16
# @Author  : Gene Jiang
# @File    : loader.py.py
# @Description:

import csv
import json
import os
import sys

from typing import Tuple, Dict, Union, Text, List, Callable

import yaml
from loguru import logger
from pydantic import ValidationError

from httpapi.model import TestCase, ProjectMeta, TestSuite
from httpapi import exceptions

project_meta: Union[ProjectMeta, None] = None


def locate_project_root_directory(test_path: Text) -> Tuple[Text, Text]:
    def prepare_path(path):
        if not os.path.exists(path):
            err_msg = f'path not existed:{path}'
            logger.error(err_msg)
            raise exceptions.FileNotFound(err_msg)

        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), path)

        return path

    test_path = prepare_path(test_path)

    httpapi_path = locate_httpapi_py(test_path)

    if httpapi_path:
        project_root_directory = os.path.dirname(httpapi_path)
    else:
        project_root_directory = os.getcwd()

    return httpapi_path, project_root_directory


def locate_file(start_path: Text, file_name: Text) -> Text:
    if os.path.isfile(start_path):
        start_dir_path = os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_dir_path = start_path
    else:
        raise exceptions.FileNotFound(f"invalid path:{start_path}")

    file_path = os.path.join(start_dir_path, file_name)
    if os.path.isfile(file_path):
        return os.path.abspath(file_path)

    parent_dir = os.path.dirname(start_dir_path)
    if parent_dir == start_dir_path:
        raise exceptions.FileNotFound(f"{file_name} not found in {start_path}")

    return locate_file(parent_dir, file_name)


def locate_httpapi_py(start_path: Text) -> Text:
    try:
        httpapi_path = locate_file(start_path, "httpaip.py")
    except exceptions.FileNotFound:
        httpapi_path = None

    return httpapi_path


def load_dot_env_file(dot_env_path: Text) -> Dict:
    if not os.path.isfile(dot_env_path):
        return {}

    logger.info(f"loading environment variables from {dot_env_path}")
    env_variable_mapping = {}

    with open(dot_env_path, mode='rb') as fp:
        for line in fp:
            if b"=" in line:
                variable, value = line.split(b"=", 1)
            elif b":" in line:
                variable, value = line.split(b":", 1)
            else:
                raise exceptions.FileFormatError(".env format error")

            env_variable_mapping[
                variable.strip().decode("utf-8", )] = value.strip().decode(
                "utf-8")

    return env_variable_mapping


def load_project_meta(test_path: Text, reload: bool = False) -> ProjectMeta:
    global project_meta

    if project_meta and (not reload):
        return project_meta

    project_meta = ProjectMeta()

    if not test_path:
        return project_meta

    httpapi_path, project_root_directory = locate_project_root_directory(
        test_path)

    sys.path.insert(0, project_root_directory)

    # env file
    dot_env_path = os.path.join(project_root_directory, ".env")
    dot_env = load_dot_env_file(dot_env_path)
    if dot_env:
        project_meta.env = dot_env
        project_meta.dot_env_path = dot_env_path

    project_meta.RootDir = project_root_directory
    project_meta.functions = {}
    project_meta.httpapi_path = httpapi_path

    return project_meta
