# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 17:08
# @Author  : Gene Jiang
# @File    : parse.py.py
# @Description:

import yaml

from typing import Tuple, Dict, Union, Text, List, Callable
from loguru import logger


def load_yaml_file(yaml_file: Text) -> Dict:
    with open(yaml_file, mode='rb') as stream:
        try:
            yaml_content = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as ex:
            error_msg = f"YAMLError: \n file:{yaml_file}\n error:{ex}"
            logger.error(error_msg)

        return yaml_content


# res = load_yaml_file("./config.yml")
# print(res)
