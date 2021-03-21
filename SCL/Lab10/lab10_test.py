import pytest

# Task 1
class Http:
    def __init__(self, req_type, req_resource, req_protocol):
        self.req_type = req_type
        self.req_resource = req_resource
        self.req_protocol = req_protocol
    
    def __eq__(self, other):
        """Equal checker =="""
        if( not isinstance(other, Http)):
            return False
        return (self.req_type == other.req_type and self.req_protocol == other.req_protocol
               and self.req_resource == other.req_resource)

    def get_fileds(self):
        """return a tuple of string fileds"""
        return (self.req_type, self.req_resource, self.req_protocol)



# task 9 my own error
class BadRequestTypeError(Exception):
    pass

class BadHTTPVersion(Exception):
    pass


# Task 2
def reqstr2Obj(request_string):
    """Based function """
    http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE',
                    'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
    http_versions = ["HTTP1.0", "HTTP1.1", "HTTP2.0"]
    try:
        request_string.split()
    except Exception:
        raise TypeError("Not a string")

    req_info = request_string.split()
    ## add if length == 3
    if len(req_info) !=3:
        return None
    req_method = req_info[0]
    req_path = req_info[1]
    req_version = req_info[2]
    if req_method.upper() not in http_methods:
        raise BadRequestTypeError("Wrong getters")

    if req_version.upper() not in http_versions:
        raise BadHTTPVersion("Wrong version")
    
    if not req_path.startswith("/"):
        raise ValueError("Bad Path")

    new_req = Http(req_info[0], req_info[1], req_info[2])
    return new_req


# Task 3
def test_1():
    """raise TypeError() """
    with pytest.raises(TypeError) as exceptionInfo:
        reqstr2Obj(4)
    assert str(exceptionInfo.value) == "Not a string"
# task 4 
# changed and not, because it does not make sense to return an exception.
# because they are thrown and they also propagate

# task 5
# in this function return an object of Type HTTp, yes but we don't care about the content
def test_2():
    """return an object of type Http"""
    http = reqstr2Obj("GET / HTTP1.1")
    assert isinstance(http, Http) == True


# Task 6
def test_3():
    """Check if the information are well set"""
    
    http = reqstr2Obj("GET / HTTP1.1")
    assert isinstance(http, Http) and http.get_fileds() == ("GET", "/", "HTTP1.1")
# Task 6 : yes but remenber this is not java so there should not be new ???


# Task 7
def test_4():
    """An object with filed set properly"""
    obj = reqstr2Obj("GET / HTTP1.1")
    assert  (obj.req_type, obj.req_resource, obj.req_protocol) == ("GET", "/", "HTTP1.1")


# Task 8
def test_5():
    """If is None for badly formated string"""
    http = reqstr2Obj("GET / HTTP1.1 None False")
    assert  http == None


# Task 9
def test_6():
    """ check if BadRequest is Raised"""
    with pytest.raises(BadRequestTypeError):
        assert  reqstr2Obj("DOWNLOAD /movie.mp4 HTTP1.1")


# Task 10
def test_7():
    """ check if BadHTTPVersion is Raised"""
    with pytest.raises(BadHTTPVersion):
        assert  reqstr2Obj("GET /movie.mp4 HTTP1.2")        


# Task 11
def test_8():
    """Check if the valueError is raised"""
    with pytest.raises(ValueError):
        assert reqstr2Obj("GET Peter/movie.mp4 HTTP1.1")