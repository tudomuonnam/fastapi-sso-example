from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path

limiter = Limiter(key_func=get_remote_address)

parent_directory = Path(__file__).parent
templates_path = parent_directory / "templates"
templates = Jinja2Templates(directory=templates_path)

def _429_error_handler(request: Request, exc: RateLimitExceeded) -> Response:
    response = templates.TemplateResponse("/itt/request.html", {"request": request,"js": "exceed_request.js"})
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response

def get_rate_limit_key(request: Request):
    if request.user is not None:
        return request.user.id
    else:
        return request.ip