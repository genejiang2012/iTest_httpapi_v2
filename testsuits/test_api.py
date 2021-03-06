# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 9:46
# @Author  : Gene Jiang
# @File    : test_api.py.py
# @Description:

from loguru import logger
from tests.context import init_session
from testsuits.funplus_test import TestLogin, TestSegmentList
from httpapi.testcases import case_start


def test_version():
    from httpapi import __version__
    assert isinstance(__version__, str)


def test_login(init_session):
    logger_handler = case_start(test_login.__name__)
    token = TestLogin() \
        .set_json({
        "loginId": "dsp.funplus",
        "password": "FunPlus_data_2020"}) \
        .run(init_session) \
        .validate('json.status.code', 'E0') \
        .validate('json.status.message', 'ok') \
        .extract('json.data.token')

    logger.remove(logger_handler)

    return token


def test_get_segment_list(init_session):
    logger_handler = case_start(test_get_segment_list.__name__)
    TestSegmentList()\
        .set_token(test_login(init_session))\
        .set_params(pageIndex=1, pageSize=1)\
        .run(init_session)\
        .validate('json.status.code', 'E0')\
        .validate('json.status.message', 'ok')\
        .validate("json.data.total", 6)

    logger.remove(logger_handler)

