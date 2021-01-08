# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/23 17:08
# @Author  : Gene Jiang
# @File    : parser.py.py
# @Description:

import re
import ast
import yaml
import builtins

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


def parse_string_value(str_value: Text) -> Any:
    try:
        return ast.literal_eval(str_value)
    except ValueError:
        return str_value
    except SyntaxError:
        return str_value


def parse_function_params(params: Text) -> Dict:
    """

    :param params:
    :return:
    """
    function_meta = {"args": [], "kwargs": {}}

    params_str = params.strip()
    if params_str == "":
        return function_meta

    args_list = params_str.split(",")
    for arg in args_list:
        arg = arg.strip()
        if "=" in arg:
            key, value = arg.split("=")
            function_meta["kwargs"][key.strip()] = parse_string_value(
                value.strip())
        else:
            function_meta["args"].append(parse_string_value(arg))

    return function_meta


def get_mapping_function(function_name: Text,
                         functions_mapping: FunctionsMapping) -> Callable:
    if function_name in functions_mapping:
        return functions_mapping[function_name]

    try:
        # check if Python builtin functions
        return getattr(builtins, function_name)
    except AttributeError:
        pass

    raise exceptions.FunctionNotFound(f"{function_name} is not found")


def get_mapping_variable(variable_name: Text,
                         variables_mapping: VariablesMapping) -> Any:
    try:
        return variables_mapping[variable_name]
    except KeyError:
        raise exceptions.VariableNotFound(
            f"{variable_name} not found in {variables_mapping}"
        )


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
            func_name = func_match.group(1)
            func = get_mapping_function(func_name, functions_mapping)

            func_params_str = func_match.group(2)
            function_meta = parse_function_params(func_params_str)
            args = function_meta["args"]
            kwargs = function_meta["kwargs"]
            parased_args = parse_data(args, variables_mapping,
                                      functions_mapping)
            parased_kwargs = parse_data(kwargs, variables_mapping,
                                        functions_mapping)

            try:
                func_eval_value = func(*parased_args, **parased_kwargs)
            except Exception as ex:
                logger.error(
                    f"call function error:\n"
                    f"func_name:{func_name}\n"
                    f"args: {parased_args}\n"
                    f"kwargs: {parased_kwargs}\n"
                    f"{type(ex).__name__}: {ex}"
                )
                raise
            func_raw_str = "${" + func_name + f"({func_params_str})" + "}"
            if func_raw_str == raw_string:
                return func_eval_value

            parsed_string += str(func_eval_value)
            match_start_position = func_match.end()
            continue

        # search the variable like ${var}
        var_match = variable_regex_compile.match(raw_string,
                                                 match_start_position)
        if var_match:
            var_name = var_match.group(1) or var_match.group(2)
            var_value = get_mapping_variable(var_name, variables_mapping)

            if f"${var_name}" == raw_string or "${" + var_name + "}" == raw_string:
                # raw_string is a variable, $var or ${var}, return its value directly
                return var_value

            # raw_string contains one or many variables, e.g. "abc${var}def"
            parsed_string += str(var_value)
            match_start_position = var_match.end()
            continue

        curr_position = match_start_position
        try:
            # find next $ location
            match_start_position = raw_string.index("$", curr_position + 1)
            remain_string = raw_string[curr_position:match_start_position]
        except ValueError:
            remain_string = raw_string[curr_position:]
            # break while loop
            match_start_position = len(raw_string)

        parsed_string += remain_string

    return parsed_string


def parse_data(
        raw_data: Any,
        variables_mapping: VariablesMapping = None,
        functions_mapping: FunctionsMapping = None
) -> Any:
    if isinstance(raw_data, str):
        variables_mapping = variables_mapping or {}
        functions_mapping = functions_mapping or {}
        raw_data = raw_data.strip(" \t")
        return parse_string(raw_data, variables_mapping, functions_mapping)
    elif isinstance(raw_data, (list, set, tuple)):
        return [parse_data(item, variables_mapping, functions_mapping) for item
                in raw_data]
    elif isinstance(raw_data, dict):
        parsed_data = {}
        for key, value in raw_data.items():
            parsed_key = parsed_data(key, variables_mapping, functions_mapping)
            parsed_value = parsed_data(value, variables_mapping,
                                       functions_mapping)
            parsed_data[parsed_key] = parsed_value

        return parsed_data
    else:
        return raw_data


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
            print(f"var_value = {var_value}; variables={variables}")

            if var_name in variables:
                raise exceptions.VariableNotFound(var_name)

            not_defined_variables = [v_name for v_name in variables if
                                     var_name not in variables_mapping]

            if not_defined_variables:
                raise exceptions.VariableNotFound(not_defined_variables)

            try:
                parsed_value = parse_data(
                    var_name, parsed_variable, functions_mapping
                )
            except exceptions.VariableNotFound:
                continue

            parsed_variable[var_name] = parsed_value

    return parsed_variable
