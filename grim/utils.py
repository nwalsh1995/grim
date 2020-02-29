import functools
from typing import Callable, Dict

from webob.request import Request


def bind(f, **ins):
    def wrap(req):
        g = f(req)
        return functools.partial(g, **{k: v(req) for k, v in ins.items()})

    return wrap


def drop_req(f):
    def drop_req_wrapper(req: Request):
        return f

    return drop_req_wrapper


# f(req) returns a function that when called empty returns the actual data
# 0 parameters, f = drop_req, and then returns original function, OK
# 1 parameter, simple bind, take req, pull vars, and then call function, OK
# 2 parameters (split), f(req) passes through all functions to build out the finally formed partial function, which gets returned


# f(req) returns the value of the processed functions
# 0 parmeters, f = drop_req, but calls original function
# 1 parameter, f finishes binds and calls func
# 2 parameters,
