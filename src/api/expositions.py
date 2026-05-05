from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select

from database import get_session

from typing import List

from models import Exposition, Exhibit  # Модели БД
from schemas import (
    ExpositionCreate, ExpositionUpdate, ExpositionRead
)
router = APIRouter()

@router.post("/api/v1/expositions/", response_model=ExpositionRead, status_code=status.HTTP_201_CREATED, tags=["Экспозиции"])
def create_exposition(exposition: ExpositionCreate, session: Session = Depends(get_session)):
    """Создание новой экспозиции"""
    db_exposition = Exposition.model_validate(exposition)
    session.add(db_exposition)
    session.commit()
    session.refresh(db_exposition)
    return db_exposition

@router.get("/api/v1/expositions/", response_model=List[ExpositionRead], tags=["Экспозиции"])
def list_expositions(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Получение списка всех экспозиций"""
    expositions = session.exec(select(Exposition).offset(skip).limit(limit)).all()
    return expositions

@router.get("/api/v1/expositions/{exposition_id}", response_model=ExpositionRead, tags=["Экспозиции"])
def get_exposition(
    exposition_id: int, 
    include_exhibits: bool = True,
    session: Session = Depends(get_session)
):
    """
    Получение экспозиции по ID
    
    - **include_exhibits**: Включить список экспонатов в ответ
    """
    exposition = session.get(Exposition, exposition_id)
    if not exposition:
        raise HTTPException(status_code=404, detail="Exposition not found")
    
    if not include_exhibits:
        exposition.exhibits = []
    
    return exposition

@router.patch("/api/v1/expositions/{exposition_id}", response_model=ExpositionRead, tags=["Экспозиции"])
def update_exposition(
    exposition_id: int, 
    exposition_update: ExpositionUpdate, 
    session: Session = Depends(get_session)
):
    """Обновление экспозиции"""
    exposition = session.get(Exposition, exposition_id)
    if not exposition:
        raise HTTPException(status_code=404, detail="Exposition not found")
    
    update_data = exposition_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(exposition, key, value)
    
    session.add(exposition)
    session.commit()
    session.refresh(exposition)
    return exposition

@router.delete("/api/v1/expositions/{exposition_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Экспозиции"])
def delete_exposition(exposition_id: int, session: Session = Depends(get_session)):
    """
    Удаление экспозиции (экспонаты останутся с exposition_id = NULL)
    """
    exposition = session.get(Exposition, exposition_id)
    if not exposition:
        raise HTTPException(status_code=404, detail="Exposition not found")
    
    exhibits_count = session.exec(
        select(Exhibit).where(Exhibit.exposition_id == exposition_id)
    ).count()  
    
    if exhibits_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete exposition with {exhibits_count} exhibits. Move them first."
        )
    
    session.delete(exposition)
    session.commit()
    return None