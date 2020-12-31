import pytest
import os

from typing import Callable
from httpapi.model import MethodEnum, TConfig, TRequest, TStep, ProjectMeta


def test_method_enum():
    method_enum = MethodEnum
    assert method_enum.GET == "GET"
    assert method_enum.POST == "POST"
    assert method_enum.DELETE == "DELETE"


def test_tconfig():
    data = {'name': 'Tom', 'verify': False,
            'base_url': "http://localhost",
            'variables': {'test1': 'test2'},
            'parameters': {'test2': 234},
            'export': [1, 2, 3],
            'path': './tests/',
            'weight': 1
            }
    __config = TConfig(**data)
    __config_2 = TConfig(name='Jerry',
                         verify=True,
                         base_url='www.baidu.com',
                         variables="456",
                         parameters='123',
                         export=[4, 5, 6],
                         path='test1',
                         weight=2
                         )
    assert __config.name == 'Tom'
    assert __config.verify == False
    assert __config.base_url == "http://localhost"
    assert __config.variables['test1'] == 'test2'
    assert __config.parameters['test2'] == 234
    assert __config.export[0] == '1'
    assert __config.path == './tests/'
    assert __config.weight == 1
    assert __config_2.variables == "456"
    assert __config_2.parameters == '123'


def test_trequest():
    data = {'method': 'GET',
            'url': "www.baidu.com",
            'params': {'abc': '123'},
            'headers': {'Content-Type': 'application/json', },
            'json': {
                "loginId": "dsp",
                "password": "data_2020"
            },
            'data': '123',
            'cookies': {},
            'timeout': 120,
            'allow_redirects': True,
            'verify': False,
            'upload': {}
            }

    _request = TRequest(**data)
    assert _request.method == 'GET'
    assert _request.headers["Content-Type"] == 'application/json'
    assert _request.data == '123'
    assert _request.cookies == {}
    assert _request.timeout == 120
    assert _request.allow_redirects == True


def test_tstep():
    data = {
        'name': 'profile_task',
        'request': {
            'method': 'GET',
            'url': "www.baidu.com",
            'params': {'abc': '123'},
            'headers': {'Content-Type': 'application/json', },
            'json': {
                "loginId": "dsp",
                "password": "data_2020"
            },
            'data': '123',
            'cookies': {},
            'timeout': 120,
            'allow_redirects': True,
            'verify': False,
            'upload': {}
        },
        'test_case': 'profile_task',
        'variables': {'params1': 'params1'},
        'extract': {'extract_value': 'extract1'},
        'export': ['123', '456'],
        'validate': [{'message': 'ok'}, {'status': 'E0'}],
        'validate_script': [1, 2, 3]
    }
    _tstep = TStep(**data)
    assert _tstep.name == 'profile_task'
    assert _tstep.request.method == 'GET'
    assert _tstep.request.req_json['loginId'] == "dsp"
    assert _tstep.test_case == 'profile_task'
    assert _tstep.variables['params1'] == 'params1'
    assert _tstep.extract['extract_value'] == 'extract1'
    assert _tstep.export[0] == '123'
    assert _tstep.validators[0]['message'] == 'ok'
    assert _tstep.validate_script[0] == "1"


def test_testcase():
    config_data = {'name': 'Tom', 'verify': False,
                   'base_url': "http://localhost",
                   'variables': {'test1': 'test2'},
                   'parameters': {'test2': 234},
                   'export': [1, 2, 3],
                   'path': './tests/',
                   'weight': 1
                   }
    step_data = {
        'name': 'profile_task',
        'request': {
            'method': 'GET',
            'url': "www.baidu.com",
            'params': {'abc': '123'},
            'headers': {'Content-Type': 'application/json', },
            'json': {
                "loginId": "dsp",
                "password": "data_2020"
            },
            'data': '123',
            'cookies': {},
            'timeout': 120,
            'allow_redirects': True,
            'verify': False,
            'upload': {}
        },
        'test_case': 'profile_task',
        'variables': {'params1': 'params1'},
        'extract': {'extract_value': 'extract1'},
        'export': ['123', '456'],
        'validate': [{'message': 'ok'}, {'status': 'E0'}],
        'validate_script': [1, 2, 3]
    }
    _config = TConfig(**config_data)
    _tstep = TStep(**step_data)
    assert _config.name == 'Tom'
    assert _tstep.validators[0]['message'] == 'ok'


def add(a, b) -> Callable[[int, int], int]:
    def __call__():
        pass
    return a + b


def test_project_meta():
    project_meta_data = {
        'httpapi_py': "core.py",
        "httpapi_path": "c:/",
        "dot_env_path": "test123",
        "functions": {},
        "env": {},
        "RootDir": os.getcwd()
    }
    _project_meta = ProjectMeta(**project_meta_data)
    assert _project_meta.httpapi_py == "core.py"
    assert _project_meta.RootDir == r"F:\git_genejiang\iTest_httpapi_v2"
