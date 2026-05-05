from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select


from typing import List

from database import get_session
from models import User  # Импорт модели БД
from schemas import UserCreate, UserLogin, UserPublic, UserUpdate  # Импорт схем

router = APIRouter()

@router.post("/api/v1/register", response_model=UserPublic, 
            tags=["Пользователи"],
            summary="Регистрация пользователя")
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    # Проверяем, не существует ли пользователь с таким email
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Хэшируем пароль и создаем пользователя
    hashed_password = User.hash_passwd(user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        age=user_data.age
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.post("/api/v1/login",
             tags=["Пользователи"],
             summary="Вход")
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.email == login_data.email)
    ).first()

    if not user or not user.verify_passwd(login_data.passwd):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}

@router.get("/api/v1/users", response_model=List[UserPublic], tags=["Пользователи"], summary="Получить список всех пользователей")
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Возвращает список всех пользователей"""
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    
    return [UserPublic.model_validate(user) for user in users]

@router.get("/api/v1/users/{user_id}", response_model=UserPublic, tags=["Пользователи"], summary="Получить конкретного пользователя")
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/api/v1/users/{user_id}", response_model=UserPublic, tags=["Пользователи"], summary="Изменить данные пользователя")
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем только переданные поля
    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        # Если обновляют пароль - хэшируем его
        update_data["hashed_password"] = User.hash_password(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    user.update_time()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.delete("/api/v1/users/{user_id}", status_code=204, tags=["Пользователи"], summary="Удалить пользователя")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Удаляет ползьователя"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usser not exist")
    session.delete(user)
    session.commit()
    return None
