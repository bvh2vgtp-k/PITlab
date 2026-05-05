from sqlmodel import SQLModel, Field
from datetime import datetime

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

#Это используется для таблицы
class User(SQLModel, table=True):
    """Класс для таблицы"""
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    email: str = Field(unique=True, index=True) 
    first_name: str = Field(nullable=False, min_length=1, max_length=30)
    last_name: str = Field(nullable=False, min_length=1, max_length=30)
    age: int = Field(default=None, ge=0, le=150)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def verify_passwd(self, plain_passwd: str) -> bool:
        """Валидация пароля"""
        return pwd_context.verify(plain_passwd, self.hashed_password)

    @classmethod
    def hash_passwd(cls, plain_passwd: str) -> str:
        """Хэширование пароля"""
        return pwd_context.hash(plain_passwd)

    def update_time(self):
        """Обновление времени"""
        self.updated_at = datetime.utcnow()

