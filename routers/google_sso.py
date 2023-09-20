from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from fastapi.responses import RedirectResponse, Response
from database_crud import users_db_crud as db_crud
from schemas import UserSignUp
from sqlalchemy.orm import Session
from database import get_db
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
from authentication import create_access_token, SESSION_COOKIE_NAME
from dotenv import load_dotenv
from pathlib import Path
import os
from typing import Union

directory_path = Path(__file__).parent
env_file_path = directory_path.parent / '.env'

load_dotenv()
GOOGLE_CLIENT_ID =  os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET =  os.getenv("GOOGLE_CLIENT_SECRET")

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

google_sso = GoogleSSO(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET, 
    "http://localhost:9999/v1/google/callback",
    allow_insecure_http=True
)

router = APIRouter(prefix="/v1/google")

#previous_link = ''

@router.get("/login", tags=['Google SSO'])
async def google_login(request: Request,response: Response):
    # Store the previous link in the user's session
    previous_link = request.headers.get("referer")#referer
    if previous_link is None:
        previous_link = '/'
    #response.set_cookie(key="previous_link", value=previous_link,max_age=120)
    request.session["previous_link"] = previous_link
    print(previous_link)
    previous_link = request.session.get('previous_link')
    print(previous_link)
    return await google_sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@router.get("/callback", tags=['Google SSO'])
async def google_callback(request: Request, db: Session = Depends(get_db)):
    # Get previous url
    previous_link = request.session.get('previous_link')
    """Process login response from Google and return user info"""
    try:
        user = await google_sso.verify_and_process(request)
        user_stored = db_crud.get_user(db, user.email, provider=user.provider)
        if not user_stored:
            user_to_add = UserSignUp(
                username=user.email,
                fullname=user.display_name
            )
            user_stored = db_crud.add_user(db, user_to_add, provider=user.provider)
        access_token = create_access_token(username=user_stored.username, provider=user.provider)
        response = RedirectResponse(url=previous_link, status_code=status.HTTP_302_FOUND)
        response.set_cookie(SESSION_COOKIE_NAME, access_token)
        return response
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")