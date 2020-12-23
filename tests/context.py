# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 10:09
# @Author  : Gene Jiang
# @File    : context.py.py
# @Description:

import pytest
import requests


@pytest.fixture
def init_session():
    return requests.sessions.Session()


if __name__ == '__main__':
    init_session()

