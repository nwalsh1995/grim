from webob import Request, Response, exc

import grim.errors as errors

import inspect
import functools
import re


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, route_regex: str, func):
        self.routes.append((re.compile(route_regex), func))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for route, func in self.routes:
            match = route.match(req.path_info)
            if match:
                # NOTE: setting urlvars will modify `environ` dict, webob thing
                req.urlvars = {
                    k: v for k, v in match.groupdict().items() if v is not None
                }
                try:
                    non_wsgi_resp = func(req)()
                except exc.HTTPException as e:
                    resp = e
                else:
                    resp = self.wsgi_converter(non_wsgi_resp)
                return resp(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)

    @functools.singledispatchmethod
    def wsgi_converter(arg):
        raise errors.NoMatchingConverter(f"No matching converter for {type(arg)}")
