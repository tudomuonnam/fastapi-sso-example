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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from database import get_db

from fastapi import FastAPI, File, UploadFile, Request,Form
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import shutil

import pytesseract

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


app = FastAPI(
    title='SSO login example API',
    description=description,
    version="1.0.0",
    docs_url="/v1/documentation",
    redoc_url="/v1/redocs",
    lifespan=lifespan
)

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
app.include_router(spotify_sso.router)
app.include_router(github_sso.router)
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
async def upload(request: Request):
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




if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9999,reload=True)
