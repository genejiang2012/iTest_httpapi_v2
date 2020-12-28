import pytest

from httpapi.model import MethodEnum, TConfig, TRequest


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
