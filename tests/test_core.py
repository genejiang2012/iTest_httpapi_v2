# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 9:46
# @Author  : Gene Jiang
# @File    : test_core.py.py
# @Description:

from api.api_4_3rd import *
from .context import init_session


def test_version():
    from api import __version__
    assert isinstance(__version__, str)


def test_login(init_session):
    token = TestLogin().\
        set_json({
        "loginId": "dsp.funplus",
        "password": "FunPlus_data_2020"})\
        .run(init_session)\
        .validate('json.status.code', 'E0')\
        .validate('json.status.message', 'ok')\
        .extract('json.data.token')

    return token


def test_get_segment_list(init_session):
    TestSegmentList()\
        .set_token(test_login(init_session))\
        .run(init_session)\
        .validate('json.status.code', 'E0')\
        .validate('json.status.message', 'ok')\
        .validate("json.data.total", 6)\
        .validate("json.data.list", [])

