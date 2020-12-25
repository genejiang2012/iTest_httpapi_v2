import os
from enum import Enum
from typing import Any, Dict, Text, Union, Callable, List

from pydantic import BaseModel, Field
from pydantic import HttpUrl

Name = Text
Url = Text
BaseUrl = Union[HttpUrl, Text]
VariablesMapping = Dict[Text, Any]
FunctionsMapping = Dict[Text, Callable]
Headers = Dict[Text, Text]
Cookies = Dict[Text, Text]
Verify = bool
Export = List[Text]
Validators = List[Dict]
Env = Dict[Text, Any]

class MethodEnum(Text, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class TConfig(BaseModel):
    name: Name
    verify: Verify = False
    base_url: BaseUrl = ""
    variables: Union[VariablesMapping, Text] = {}
    parameters: Union[VariablesMapping, Text] = {} 
    export: Export = []
    path: Text = None
    weight: int = 1