from fastapi import Request, APIRouter, UploadFile, File, Form
from fastapi.responses import HTMLResponse

from limiter import limiter  # limiter from slowapi setting
from api.template import templates #templates directory setting

import shutil
import pytesseract

router = APIRouter(prefix="/v1")

@router.get("/slowapi/")
@limiter.limit("2/minute")
async def slow_api(request:Request):
    #return ({"msg": "success"})
    print(templates)
    return templates.TemplateResponse("/itt/request.html", {"request": request})

@router.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   #https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
   url = request.url.path
   return templates.TemplateResponse("/itt/request.html", {"request": request, "url": url})

@router.post("/upload/")
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