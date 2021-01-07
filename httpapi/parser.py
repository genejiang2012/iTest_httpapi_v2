# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 17:08
# @Author  : Gene Jiang
# @File    : parser.py.py
# @Description:

import re
import yaml

from typing import Tuple, Dict, Union, Text, List, Callable, Any, Set
from loguru import logger
from httpapi.model import VariablesMapping, FunctionsMapping
import httpapi.exceptions as exceptions

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


def get_mapping_function(function_name: Text,
                         functions_mapping: FunctionsMapping) -> Callable:
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    raise exceptions.FunctionNotFound(f"{function_name} is not found")


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
        func_match = function_regex_compile.match(raw_string,
                                                  match_start_position)
        if func_match:
            fun_name = func_match.group(1)
            func = get_mapping_function(fun_name, functions_mapping)


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


def regex_find_variables(raw_string: Text) -> List[Text]:
    try:
        match_start_position = raw_string.index("$", 0)
    except ValueError:
        return []

    vars_list = []
    while match_start_position < len(raw_string):
        dollar_match = dollar_regex_compile.match(raw_string,
                                                  match_start_position)
        if dollar_match:
            match_start_position = dollar_match.end()
            continue

        var_match = variable_regex_compile.match(raw_string,
                                                 match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            vars_list.append(var_name)
            match_start_position = var_match.end()
            continue

        cur_position = match_start_position
        try:
            match_start_position = raw_string.index("$", cur_position + 1)
        except ValueError:
            break

    return vars_list


def extract_variables(content: Any) -> Set:
    if isinstance(content, (list, set, tuple)):
        variables = set()
        for item in content:
            variables = variables | extract_variables(item)
            return variables

    elif isinstance(content, dict):
        variables = set()
        for key, value in content.items():
            variables = variables | extract_variables(value)
        return variables

    elif isinstance(content, str):
        return set(regex_find_variables(content))

    return set()


def parse_variable_mapping(variables_mapping: VariablesMapping,
                           functions_mapping: FunctionsMapping = None) \
        -> VariablesMapping:
    parsed_variable: VariablesMapping = {}
    while len(parsed_variable) != len(variables_mapping):
        for var_name in variables_mapping:
            if var_name in parsed_variable:
                continue

            var_value = variables_mapping[var_name]
            variables = extract_variables(var_value)

            if var_name in variables:
                raise exceptions.VariableMappingError(var_name)

            not_defined_variables = [v_name for v_name in variables if
                                     var_name not in variables_mapping]

            if not_defined_variables:
                raise exceptions.VariableNotFound(not_defined_variables)
