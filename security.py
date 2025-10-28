from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Optional

from jose import jwt

import settings


# функция создаёт токен аутентификации
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(  # время, когда токен истечёт
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})  # обязательно указывать в exp
    encoded_jwt = jwt.encode(  # создание токена
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt
