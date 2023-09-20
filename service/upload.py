# from fastapi import APIRouter
# from fastapi import FastAPI, Request, Depends, HTTPException, File, UploadFile, Form


# from fastapi.responses import HTMLResponse, JSONResponse, Response
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from pathlib import Path
# from database import get_db

# parent_directory = Path(__file__).parent
# templates_path = parent_directory / "templates"
# templates = Jinja2Templates(directory=templates_path)

# import shutil
# import pytesseract

# #from slowapi import Limiter
# from main import limiter

# router = APIRouter(prefix="/v1")

# #limiter1 = Limiter(limit=1, time_window=1)

# @router.get("/upload/", response_class=HTMLResponse)
# async def upload(request: Request):
#    #https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
#    return templates.TemplateResponse("/itt/request.html", {"request": request})

# @router.post("/upload/")
# async def create_upload_file(request:Request,file: UploadFile = File(...),lang:str=Form()):
#     try:
#         with open(file.filename, 'wb') as f:
#             shutil.copyfileobj(file.file, f)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         text = pytesseract.image_to_string(file.filename,lang=lang)
#         file.file.close()   
#     lines = text.splitlines()
#     return templates.TemplateResponse("/itt/response.html", {"request": request, "msg":lines})


# @router.get("/slowapi/")
# @limiter.limit("5/minute")
# async def slow_api(request:Request):
#     return templates.TemplateResponse("/itt/request.html", {"request": request})