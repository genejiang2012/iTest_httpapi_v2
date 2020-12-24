# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 14:41
# @Author  : Gene Jiang
# @File    : log.py.py
# @Description:

import os
import sys
from loguru import logger
from httpapi.exceptions import StringEmptyError


def get_project_metadata():
    project_meta = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))

    if project_meta:
        return project_meta
    else:
        raise StringEmptyError

