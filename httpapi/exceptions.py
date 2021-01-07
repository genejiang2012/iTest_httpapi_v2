# !/usr/bin/env python3 
# -*- coding: utf-8 -*-
# @Time    : 2020/12/24 11:48
# @Author  : Gene Jiang
# @File    : exceptions.py
# @Description:


class MyBaseFailure(Exception):
    pass


class StringEmptyError(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class FileFormatError(MyBaseFailure):
    pass


class VariableNotFound(NotFoundError):
    pass


class FunctionNotFound(NotFoundError):
    pass

