import pytest

# Task 1
class Http:
    def __init__(self, req_type, req_resource, req_protocol):
        self.req_type = req_type
        self.req_resource = req_resource
        self.req_protocol = req_protocol
    

# task 9 my own error
class BadRequestTypeError(Exception):
    pass

class BadHTTPVersion(Exception):
    pass


methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
versions = ["HTTP1.0", "HTTP1.1", "HTTP2.0"]

# Task 2
def reqstr2Obj(request_string):
    try:
        request_string.split()
    except Exception:
        raise TypeError("Not a string")

    req_info = request_string.split()
    if len(req_info) !=3:
        return None
    req_method = req_info[0]
    req_path = req_info[1]
    req_version = req_info[2]
    if req_method.upper() not in methods:
        raise BadRequestTypeError("Wrong getters")

    if req_version.upper() not in versions:
        raise BadHTTPVersion("Wrong version")
    
    if not req_path.startswith("/"):
        raise ValueError("Bad Path")

    new_req = Http(req_info[0], req_info[1], req_info[2])
    return new_req



def test_1():
    with pytest.raises(TypeError) as exceptionInfo:
        reqstr2Obj(4)
    assert str(exceptionInfo.value) == "Not a string"


def test_2():
    
    http = reqstr2Obj("GET / HTTP1.1")
    assert isinstance(http, Http) == True


def test_3():
    obj = reqstr2Obj("GET / HTTP1.1")
    assert  (obj.req_type, obj.req_resource, obj.req_protocol) == ("GET", "/", "HTTP1.1")


def test_4():
    
    obj = reqstr2Obj("GET / HTTP1.1")
    assert  (obj.req_type, obj.req_resource, obj.req_protocol) == ("GET", "/", "HTTP1.1")


def test_5():
    """If is None for badly formated string"""
    http = reqstr2Obj("GET / HTTP1.1 None False")
    assert  http == None


def test_6():
    
    with pytest.raises(BadRequestTypeError):
        assert  reqstr2Obj("DOWNLOAD /movie.mp4 HTTP1.1")

def test_7():
    with pytest.raises(BadHTTPVersion):
        assert  reqstr2Obj("GET /movie.mp4 HTTP1.2")        



def test_8():
    with pytest.raises(ValueError):
        assert reqstr2Obj("GET User/movie.mp4 HTTP1.1")