# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 19:29
# @Author  : Gene Jiang
# @File    : test_parser.py.py
# @Description:

import pytest
from httpapi import parser
import logger


def test_parse_string_value():
    assert parser.parse_string_value("123") == 123
    assert parser.parse_string_value("12.2") == 12.2
    assert parser.parse_string_value("abc") == "abc"
    assert parser.parse_string_value("$var") == "$var"


def test_extract_variables():
    assert parser.extract_variables("$var") == {"var"}
    assert parser.extract_variables("$var123") == {"var123"}
    assert parser.extract_variables("$var_name") == {"var_name"}
    assert parser.extract_variables("var") == set()
    assert parser.extract_variables("a$var") == {"var"}
    assert parser.extract_variables("$v ar") == {"v"}
    assert parser.extract_variables(" ") == set()
    assert parser.extract_variables("$abc*") == {"abc"}
    assert parser.extract_variables("${func()}") == set()
    assert parser.extract_variables("${func(1,2)}") == set()
    assert parser.extract_variables("${gen_md5($TOKEN, $data, $random)}") == {
        "TOKEN", "data", "random"}
    assert parser.extract_variables("Z:2>1*0*1+1$$1") == set()


def test_parse_data():
    variables_mapping = {
        "var_1": "abc",
        "var_2": "def",
        "var_3": 123,
        "var_4": {"a": 1},
        "var_5": True,
        "var_6": None
    }

    assert parser.parse_data("$var_1", variables_mapping) == "abc"
    assert parser.parse_data("${var_1}", variables_mapping) == "abc"
    assert parser.parse_data("var_1", variables_mapping) == "var_1"
    assert parser.parse_data("$var_1#XYZ", variables_mapping) == "abc#XYZ"
    assert parser.parse_data("${var_1}#XYZ", variables_mapping) == "abc#XYZ"
    assert parser.parse_data("/$var_1/$var_2/var3",
                             variables_mapping) == "/abc/def/var3"
    assert parser.parse_data("$var_3", variables_mapping) == 123
    assert parser.parse_data("$var_4", variables_mapping) == {"a": 1}
    assert parser.parse_data("$var_5", variables_mapping) == True
    assert parser.parse_data("abc$var_5", variables_mapping) == 'abcTrue'
    assert parser.parse_data("abc$var_4", variables_mapping) == "abc{'a': 1}"
    assert parser.parse_data("$var_6", variables_mapping) == None
    assert parser.parse_data("/api/$var_1", variables_mapping) == "/api/abc"
    assert parser.parse_data(["$var_1", "$var_2"], variables_mapping) == ["abc",
                                                                          "def"]
    assert parser.parse_data({"$var_1": "$var_2"}, variables_mapping) == {"abc":
                                                                              "def"}
    assert parser.parse_data("ABC$var_1", variables_mapping) == "ABCabc"
    assert parser.parse_data("ABC${var_1}", variables_mapping) == "ABCabc"
    assert parser.parse_data("ABC${var_1}/123${var_1}/456",
                             variables_mapping) == "ABCabc/123abc/456"
    assert parser.parse_data("func1(${var_1}, ${var_3})",
                             variables_mapping) == "func1(abc, 123)"


def test_parse_string():
    assert parser.parse_string("abc${add_one($num}def", {"num": 3},
                               {"add_one": lambda x: x + 1}) == "abc4def"


def test_parse_variable_mapping():
    variables = {"varA": "$varB", "varB": "$varC", "varC": "123", "a": 1,
                 "b": 2}
    parsed_variable = parser.parse_variable_mapping(variables)
    logger.info(f"The parsed value is {parsed_variable}")
    assert parsed_variable["varA"] == "123"
    assert parsed_variable["varB"] == "123"
