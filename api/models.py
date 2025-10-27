import uuid
import re

from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, constr



LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z/-]+$")


class TunedModel(BaseModel):

    class Config: # говорит что pydantic надо конвертировать не dict объекты в json 
        orm_mode = True

# модель которая будет возвращать на клиентскую сторону поля характерные для пользовтаеля 
class ShowUser(TunedModel):
    user_id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool


# модель обратки входящего запроса 
class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr


    @field_validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contrains only letters")

        return value
    

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contrains only lettets")
        
        return value

class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID

class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID

class UpdateUserRequest(BaseModel):
    name = Optional[constr(min_length=1)]
    surname = Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @field_validator("name")
    def validate_name(cls,value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Name should contains only letters")
        return value
    

    @field_validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(status_code=422, detail="Surname should contains only lettetrs")
        return value




