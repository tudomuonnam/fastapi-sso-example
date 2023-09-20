import uvicorn
from fastapi import FastAPI, Request, Depends, HTTPException
from contextlib import asynccontextmanager
from db_models import Base
from database import engine
from database_crud import users_db_crud as db_crud
from sqlalchemy.orm import Session

from routers import auth, google_sso, spotify_sso, github_sso, facebook_sso, microsoft_sso
from service import upload, newupload
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from schemas import User
from authentication import get_current_user

from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db

from api.template import templates

from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from limiter import limiter, _429_error_handler

from fastapi import FastAPI, File, UploadFile,Form

description = """
Example API to demonstrate SSO login in fastAPI
"""

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

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
#app.include_router(upload.router)
app.include_router(newupload.router)


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


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999,reload=True)
