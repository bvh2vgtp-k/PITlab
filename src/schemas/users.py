from pydantic import BaseModel, EmailStr, Field, field_validator, AfterValidator
from typing import Optional, Annotated
from datetime import datetime


# Валидаторы имен
def validate_firstname(v: str) -> str:
    if not v.isalpha():
        raise ValueError('Firstname must contain only letters')
    return v.capitalize()

def validate_lastname(v: str) -> str:
    if not v.isalpha():
        raise ValueError('Lastname must contain only letters')
    return v.capitalize()

# Типы с валидацией
FirstnameType = Annotated[str, AfterValidator(validate_firstname)]
LastnameType = Annotated[str, AfterValidator(validate_lastname)]

class UserBase(BaseModel):
    """Базовая схема - общие поля"""
    email: EmailStr
    first_name: FirstnameType = Field(min_length=1, max_length=50)
    last_name: LastnameType = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)

class UserCreate(UserBase):
    """Схема для создания пользователя"""
    password: str = Field(min_length=8)

class UserPublic(UserBase):
    """Схема для ответа API (без пароля)"""
    id: int
    email: str
    first_name: str
    last_name: str
    age: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Для работы с SQLModel

class UserUpdate(BaseModel):
    """Схема для обновления данных (все поля опциональны)"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=150)
    password: Optional[str] = Field(None, min_length=8)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not any(char.isdigit() for char in v):
                raise ValueError('Password must contain at least one digit')
            if not any(char.isupper() for char in v):
                raise ValueError('Password must contain at least one uppercase letter')
        return v

class UserLogin(BaseModel):
    """Схема для логина"""
    email: EmailStr
    password: str  # Исправлено с `passwd` на `password` для консистентности