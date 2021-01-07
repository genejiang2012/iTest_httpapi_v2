# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 19:29
# @Author  : Gene Jiang
# @File    : test_parser.py.py
# @Description:

import pytest
from httpapi import parser


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


def test_parse_string():
    assert parser.parse_string("abc${add_one($num}def", {"num": 3},
                               {"add_one": lambda x: x + 1}) == "abc4def"


def test_parse_variable_mapping():
    variables = {"varA": "$varB", "varB": "$varC", "varC": "123", "a": 1,
                 "b": 2}
    parsed_variable = parser.parse_variable_mapping(variables)
    print(parsed_variable)
    assert parsed_variable["varA"] == "123"
    assert parsed_variable["varB"] == "123"


