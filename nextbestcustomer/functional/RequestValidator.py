from types import MappingProxyType
import azure.functions as func
import json

class RequestValidator:

    def __init__(self, request : func.HttpRequest):
        self.req = request
    
    def validate(self, request_attr: str):
        return _getValidator(request_attr, self.req)

def _getValidator(request_attr: str, request: func.HttpRequest):
    if request_attr == "query":
        return _queryValidater(request)
    elif request_attr == "body":
        return _bodyValidator(request)

        

def _queryValidater(req: func.HttpRequest):
    req_parameters = req.params
    valid_parmeters = ['lat', 'long', 'mail']

    if not(_keysAreIdentical(valid_parmeters, req_parameters)):
        raise InvalidQueryParameter()

def _bodyValidator(req: func.HttpRequest):
    try:
        req_body = req.get_body()
        json.loads(req_body)
    except json.JSONDecodeError as e:
        raise InvalidRequestBody()
    
def _keysAreIdentical(valid: list, requests: MappingProxyType) -> bool:
    valid_key_set = set(valid)
    request_key_set = set(requests.keys())
    return valid_key_set == request_key_set and len(valid_key_set) == len(request_key_set)


    

class InvalidQueryParameter(Exception):
    def __init__(self):
        super().__init__("Invalid query-parameters: Except: 'lat', 'long', 'mail'")

class InvalidRequestBody(Exception):
    def __init__(self):
        super().__init__(f"Invalid Body: Except json-object")



