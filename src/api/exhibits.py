from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from database import get_session

from typing import List, Optional
from datetime import datetime

#from models.exhibits import Exhibit, ExhibitCreate, ExhibitRead, ExhibitUpdate
#from models.expositions import Exposition

from models import Exhibit, Exposition

# Импорт Pydantic схем (все остальное)
from schemas import (
    # Схемы для экспонатов
    ExhibitCreate,
    ExhibitUpdate,
    ExhibitRead,
)

router = APIRouter()

@router.post("/api/v1/exhibits/", response_model=ExhibitRead, status_code=status.HTTP_201_CREATED, tags=["Экспонаты"])
def create_exhibit(exhibit: ExhibitCreate, session: Session = Depends(get_session)):
    """
    Создание нового экспоната
    
    - **name**: Название экспоната (обязательно)
    - **dating**: Датировка (например, "XII век")
    - **material**: Материал изготовления
    - **technique**: Техника исполнения
    - **dimensions**: Размеры
    - **description**: Описание
    - **condition**: Сохранность
    - **exposition_id**: ID экспозиции (опционально)
    """
    # Проверяем, существует ли экспозиция (если указана)
    if exhibit.exposition_id:
        exposition = session.get(Exposition, exhibit.exposition_id)
        if not exposition:
            raise HTTPException(
                status_code=404, 
                detail=f"Exposition with id {exhibit.exposition_id} not found"
            )
    
    db_exhibit = Exhibit.model_validate(exhibit)
    session.add(db_exhibit)
    session.commit()
    session.refresh(db_exhibit)
    return db_exhibit

@router.get("/api/v1/exhibits/", response_model=List[ExhibitRead], tags=["Экспонаты"])
def list_exhibits(
    skip: int = 0,
    limit: int = 100,
    exposition_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    """
    Получение списка экспонатов 
    
    - **skip**: Количество пропускаемых записей
    - **limit**: Максимальное количество записей
    - **exposition_id**: Фильтр по ID экспозиции
    """
    query = select(Exhibit)
    
    if exposition_id:
        query = query.where(Exhibit.exposition_id == exposition_id)
    
    
    exhibits = session.exec(query.offset(skip).limit(limit)).all()
    return exhibits

@router.get("/api/v1/exhibits/{exhibit_id}", response_model=ExhibitRead, tags=["Экспонаты"])
def get_exhibit(exhibit_id: int, session: Session = Depends(get_session)):
    """
    Получение экспоната по ID с его фотографиями
    """
    exhibit = session.get(Exhibit, exhibit_id)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return exhibit

@router.patch("/api/v1/exhibits/{exhibit_id}", response_model=ExhibitRead, tags=["Экспонаты"])
def update_exhibit(
    exhibit_id: int, 
    exhibit_update: ExhibitUpdate, 
    session: Session = Depends(get_session)
):
    """
    Частичное обновление экспоната
    """
    exhibit = session.get(Exhibit, exhibit_id)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    
    # Проверяем экспозицию если обновляется
    if exhibit_update.exposition_id:
        exposition = session.get(Exposition, exhibit_update.exposition_id)
        if not exposition:
            raise HTTPException(status_code=404, detail="Exposition not found")
    
    # Проверяем инвентарный номер на уникальность
    if exhibit_update.inventory_number:
        existing = session.exec(
            select(Exhibit).where(
                Exhibit.inventory_number == exhibit_update.inventory_number,
                Exhibit.id != exhibit_id
            )
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Inventory number already exists"
            )
    
    # Обновляем только переданные поля
    update_data = exhibit_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exhibit, key, value)
    
    exhibit.updated_at = datetime.utcnow()
    session.add(exhibit)
    session.commit()
    session.refresh(exhibit)
    return exhibit

@router.delete("/api/v1/exhibits/{exhibit_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Экспонаты"])
def delete_exhibit(exhibit_id: int, session: Session = Depends(get_session)):
    """
    Удаление экспоната (фотографии удалятся каскадно)
    """
    exhibit = session.get(Exhibit, exhibit_id)
    if not exhibit:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    session.delete(exhibit)
    session.commit()
    return None