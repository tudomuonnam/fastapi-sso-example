## SlowAPI
1. Support individual limits by IP address or user token?
https://github.com/laurentS/slowapi/issues/155

hey, hope its useful for u:
u can define limiter as Limiter(key_func=get_limiter_key, ...)
```
def get_limiter_key(request: Request):
    current_key = request.scope.get("client")[0]
    request_headers = request.scope.get("headers")
    limiter_prefix = request.scope.get("root_path") + request.scope.get("path") + ":"

    for headers in request_headers:
        if headers[0].decode() == "authorization":
            current_key = headers[1].decode()
            break

        if headers[0].decode() in ("user-agent", "x-real-ip"):
            current_key += headers[1].decode()

    # shorter key
    hash_object = hashlib.sha256(current_key.encode())
    current_key = hash_object.hexdigest()

    limiter_key = re.sub(
        r":{1,}",
        ":",
        re.sub(r"/{1,}", ":", limiter_prefix + current_key),
    )
    return limiter_key
```
2. Dynamic rate limit based on user type
https://github.com/laurentS/slowapi/issues/13
```
REQUEST_CTX_KEY = "request_context"
_request_ctx_var: ContextVar[str] = ContextVar(REQUEST_CTX_KEY, default=None)

@app.middleware("http")
async def request_context_middleware(request: Request, call_next):
    try:
        request_ctx = _request_ctx_var.set(request)
        response = await call_next(request)
        _request_ctx_var.reset(request_ctx)
        return response
    except Exception as e:
        raise e
```
## Fastapi-limiter
https://github.com/long2ice/fastapi-limiter

## Payment gateway
https://github.com/django-getpaid/django-getpaid

## Fastapi redirect link after login
https://stackoverflow.com/questions/71657407/how-to-redirect-to-login-in-fastapi