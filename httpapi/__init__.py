# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/22 17:43
# @Author  : Gene Jiang
# @File    : __init__.py.py
# @Description:

__version__ = "0.1.0"
__description__ = "Http API framework"


# from httpapi.parser import parse_parameters as Parameters
from httpapi.core import HttpAPI
from httpapi.testcases import Config, Step, RunRequest, RunTestCase
from httpapi.testcases import Config, Step

__all__ = [
    "__version__",
    "__description__",
    "HttpAPI",
    "Config",
    "Step",
    "RunRequest",
    "RunTestCase",
    # "Parameters",
]