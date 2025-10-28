from passlib.context import CryptContext

# создание контекста для хэширования
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:

    # принимаем обычный пароль и его хэшированную версию и сравнивает, соответствует ли обычный пароль хэшу
    @staticmethod
    def verify_password(plan_password, hashed_password) -> bool:
        return pwd_context.verify(plan_password, hashed_password)

    # принимает обычный пароль и возвращает егэ хэишрованную версию
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)
