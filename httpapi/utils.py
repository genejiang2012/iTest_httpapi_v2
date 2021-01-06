# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2021/1/6 18:52
# @Author  : Gene Jiang
# @File    : utils.py
# @Description:

import copy
from httpapi.model import VariablesMapping


def merge_variables(variables: VariablesMapping,
                    variables_to_be_overridden: VariablesMapping)\
        -> VariablesMapping:

    step_new_variables = {}
    for key, value in variables.items():
        if f"${key}"  == value or "${" + key + "}" == value:
            continue

        step_new_variables[key] = value

    merge_variables = copy.copy(variables_to_be_overridden)
    merge_variables.update(step_new_variables)
    return merge_variables
