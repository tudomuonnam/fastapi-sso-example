from fastapi import Depends, APIRouter, HTTPException, Form, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from authentication import create_access_token, authenticate_user, SESSION_COOKIE_NAME
from database import get_db
from database_crud import users_db_crud as db_crud
from schemas import User, UserSignUp

from authentication import get_current_user
from api.template import templates


router = APIRouter(prefix="/v1")
@router.get("/login",response_class=HTMLResponse)
def login_user(request: Request,user: User = Depends(get_current_user)):
    return templates.TemplateResponse("/auth/request.html",{"request": request, "user": user})

@router.post("/sign_up", response_model=User, summary="Register a user", tags=["Auth"])
def create_user(user_signup: UserSignUp, db: Session = Depends(get_db)):
    """
    Registers a user.
    """
    try:
        user_created = db_crud.add_user(db, user_signup)
        return user_created
    except db_crud.DuplicateError as e:
        raise HTTPException(status_code=403, detail=f"{e}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/login", summary="Login as a user", tags=["Auth"])
def login(response: RedirectResponse, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """
    Logs in a user.
    """
    user = authenticate_user(db=db, username=username, password=password, provider='local')
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid username or password.")
    try:
        access_token = create_access_token(username=user.username, provider='local')
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.set_cookie(SESSION_COOKIE_NAME, access_token)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")


@router.post("/logout", summary="Logout a user", tags=["Auth"])
def logout():
    """
    Logout a user.
    """
    try:
        response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
        response.delete_cookie(SESSION_COOKIE_NAME)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred. Report this message to support: {e}")
