# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 17:08
# @Author  : Gene Jiang
# @File    : parser.py.py
# @Description:

import re
import yaml

from typing import Tuple, Dict, Union, Text, List, Callable, Any
from loguru import logger
from httpapi.model import VariablesMapping, FunctionsMapping

dollar_regex_compile = re.compile(r"\$\$")
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")


def load_yaml_file(yaml_file: Text) -> Dict:
    with open(yaml_file, mode='rb') as stream:
        try:
            yaml_content = yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as ex:
            error_msg = f"YAMLError: \n file:{yaml_file}\n error:{ex}"
            logger.error(error_msg)

        return yaml_content


def parse_string(
        raw_string: Text,
        variables_mapping: VariablesMapping,
        functions_mapping: FunctionsMapping
) -> Any:
    try:
        match_start_position = raw_string.index("$", 0)
        parsed_string = raw_string[0:match_start_position]
    except ValueError:
        parsed_string = raw_string
        return parsed_string

    while match_start_position < len(raw_string):
        dollar_match = dollar_regex_compile.match(raw_string,
                                                  match_start_position)

        # search $$
        if dollar_match:
            match_start_position = dollar_match.end()
            parsed_string += "$"
            continue

        # search functions
        func_match = function_regex_compile.match(raw_string, match_start_position)
        if func_match:
            fun_name = func_match.group(1)



def parse_data(
        raw_data: Any,
        variables_mapping: VariablesMapping = None,
        functions_mapping: FunctionsMapping = None
) -> Any:
    if isinstance(raw_data, str):
        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}
        raw_data = raw_data.strip(" \t")
        return parse_string()
