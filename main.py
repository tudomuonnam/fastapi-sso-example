import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from contextlib import asynccontextmanager
from db_models import Base
from database import engine
from database_crud import users_db_crud as db_crud
from sqlalchemy.orm import Session
from routers import auth, google_sso, spotify_sso, github_sso, facebook_sso, microsoft_sso
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from schemas import User
from authentication import get_current_user

from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db

from fastapi import FastAPI, File, UploadFile, Request,Form


import shutil

import pytesseract

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

parent_directory = Path(__file__).parent
templates_path = parent_directory / "templates"
templates = Jinja2Templates(directory=templates_path)

description = """
Example API to demonstrate SSO login in fastAPI
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

limiter = Limiter(key_func=get_remote_address)

def _429_error_handler(request: Request, exc: RateLimitExceeded) -> Response:
    response = templates.TemplateResponse("/itt/request.html", {"request": request,"js": "exceed_request.js"})
    # response = JSONResponse(
    #     {"error": f"Request exceeded: {exc.detail}"}, status_code=429
    # )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response

app = FastAPI(
    title='SSO login example API',
    description=description,
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs",
    lifespan=lifespan
)

    
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _429_error_handler)

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.router)
app.include_router(google_sso.router)
#app.include_router(spotify_sso.router)
#app.include_router(github_sso.router)
app.include_router(facebook_sso.router)
app.include_router(microsoft_sso.router)






@app.get("/", response_class=HTMLResponse, summary="Home page")
def home_page(request: Request, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """
    Returns all users.
    """
    try:
        if user is not None:
            users_stats = db_crud.get_users_stats(db)
        else:
            users_stats = []
        return templates.TemplateResponse("index.html", {"request": request, "user": user, "users_stats": users_stats})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request,db: Session = Depends(get_db), user: User = Depends(get_current_user)):
   #https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
   client_host = request.client.host
   print(client_host)
   return templates.TemplateResponse("/itt/request.html", {"request": request})

@app.post("/upload/")
async def create_upload_file(request:Request,file: UploadFile = File(...),lang:str=Form()):
    try:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        text = pytesseract.image_to_string(file.filename,lang=lang)
        file.file.close()   
    lines = text.splitlines()
    return templates.TemplateResponse("/itt/response.html", {"request": request, "msg":lines})


@app.get("/slowapi/")
@limiter.limit("2/minute")
async def slow_api(request:Request):
    return templates.TemplateResponse("/itt/request.html", {"request": request})    


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999,reload=True)
