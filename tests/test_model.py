import pytest

from httpapi.model import MethodEnum, TConfig


def test_method_enum():
    method_enum = MethodEnum
    assert method_enum.GET == "GET"
    assert method_enum.POST == "POST"
    assert method_enum.DELETE == "DELETE"