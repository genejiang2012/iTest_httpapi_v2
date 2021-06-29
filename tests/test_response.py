# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 19:29
# @Author  : Gene Jiang
# @File    : test_parser.py.py
# @Description:

import pytest
from httpapi import parser
from loguru import logger
from httpapi import response

# global variables_mapping

def test_get_uniform_comparator():
    """
    test the get_uniform_comparator function from class named response
    :return:
    """
    assert response.get_uniform_comparator("eq") == "equal"
    assert response.get_uniform_comparator("lt") == "less_than"
    assert response.get_uniform_comparator("le") == "less_or_equals"


def test_uniform_validator():
    validator = {
        "check": "status_code",
        "expect": 201,
        "assert": "equals"
    }
    assert response.uniform_validator(validator)["check"] == "status_code"
    assert response.uniform_validator(validator)["expect"] == 201
    # assert response.uniform_validator(validator)["assert"] == "equals"


def test_response_object():
    import requests
    import json
    params = {"key1": "python", "key2": "java"}
    r = requests.get(url="http://httpbin.org/get", params=params)
    dict_result = json.loads(r.json())

    obj_response = response.ResponseObject(r)
    assert obj_response.__getattr__("json") == r.json()






