from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from db_models import User
from database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db_models import IpLog
from datetime import datetime
from schemas import AccessLog
from database_crud import ip_db_crud

def get_current_count(db: Session, ip: str):
    use_service = db.query(IpLog).filter(IpLog.ip == ip)
    time = datetime.now()
    if not use_service:
        #IP chưa sử dụng dịch vụ
        # add ip and add count to 1
        ip_to_add = AccessLog(
            ip=ip,
            count = 1,
            last_access=time,
            first_access=time
        ) 
        ip_stored = ip_db_crud.add_iplog(ip_to_add)
        return 1
    else:
        # Ip da co trong database
        #check if ip da su dung dv hom nay chua
        if(use_service.count_daily >1):
            return use_service.count_daily
        else: return 1