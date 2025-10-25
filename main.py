from fastapi import FastAPI
import uvicorn
from fastapi.routing import APIRouter
from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession 
from sqlalchemy.orm import sessionmaker, declarative_base
import settings
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator


# создаём асинхронный движок для взаимодейтсвия с бд
engine = create_async_engine(settings.DATABASE_URL, future=True,echo=True)

# создаём объект асинхронной сессии
async_session = sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)


# блок с моделями бд

# вовзращем специальный объект, чтобы от него можно было потом наследоват от них модели
Base = declarative_base()


class User(Base):
    __tablename__ = "users" # название бд в постгре

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    email = Column(String, nullable=True, unique=True)
    is_active = Column(Boolean(), default=True)# удалён/не удалён


# Бизнес логика

class UserDAL:
    "Data Access Layer for operation user info"

    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_user(self, name:str, surname:str, email:str) -> User:
        new_user = User(name=name, surname=surname, email=email)

        self.db_session.add(new_user)
        await self.db_session.flush() # асинхронная отравка данных в постгре 
        return new_user


# Блок API models


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



# Блок с роутерами API

app = FastAPI(title="zhigalev_university")

user_router = APIRouter()


async def _create_new_user(body: UserCreate):
    async with async_session() as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                )
            
            return ShowUser(
                user_id=user.user_id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active

            )

@user_router.post("/", response_model=ShowUser)
async def create_user(body:UserCreate) -> ShowUser:
    return await _create_new_user(body)


main_api_router = APIRouter()



main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


