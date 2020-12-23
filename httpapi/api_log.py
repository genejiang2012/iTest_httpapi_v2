# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 14:41
# @Author  : Gene Jiang
# @File    : api_log.py.py
# @Description:

import os
import sys
from loguru import logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
normal_log_relative_path = os.sep.join(['logs', 'runtime.log'])
error_log_relative_path = os.sep.join(['logs', 'err.log'])
log_file_path = os.path.join(BASE_DIR, normal_log_relative_path)
err_log_file_path = os.path.join(BASE_DIR, error_log_relative_path)

logger.debug(log_file_path)

logger.add(log_file_path, rotation="500 MB", encoding='utf-8', level='DEBUG')
logger.add(err_log_file_path, rotation="500 MB", encoding='utf-8',
           level='ERROR')
logger.add(sys.stdout, format="{time} {level} {message}", filter="my_module",
           level="INFO")

