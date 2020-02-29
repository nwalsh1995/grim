from webob import Response

import operator

from grim.router import Router
from grim.utils import drop_req, bind


def hello(name="World"):
    """Example of a function with keyword argument."""
    return f"Hello {name}"


def hello_world():
    """Example of a function with no parameters."""
    return "Hello World no params"


def hello_one(name1):
    return f"Hello {name1}"


def hello_two(name1, name2):
    return f"Hello {name1} and {name2}"


app = Router()


@app.wsgi_converter.register
def str_converter(self, arg: str):
    """Convert string types to WSGI response objects."""
    return Response(body=arg)


# these return a string, which we have registered.
app.add_route(
    "^/hello/(?P<name1>.+)/(?P<name2>.+)$",
    bind(
        bind(drop_req(hello_two), name1=lambda req: req.urlvars["name1"]),
        name2=lambda req: req.urlvars["name2"],
    ),
)
app.add_route(
    "^/hello/(?P<name1>.+)$",
    bind(drop_req(hello_one), name1=lambda req: req.urlvars["name1"]),
)
app.add_route("^/hello$", drop_req(hello_world))


if __name__ == "__main__":
    from paste import httpserver

    httpserver.serve(app, host="127.0.0.1", port=8080)
