from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Используем TYPE_CHECKING для избежания циклических импортов
if TYPE_CHECKING:
    from models.exposition import Exposition


class ExhibitPhoto(SQLModel, table=True):
    __tablename__ = "exhibit_photos"

    id: int | None = Field(default=None, primary_key=True)
    exhibit_id: int = Field(foreign_key="exhibits.id", description="ID экспоната")
    photo_url: str = Field(max_length=500, description="URL или путь к фото")
    is_primary: bool = Field(default=False, description="Основное фото")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Связь с экспонатом
    exhibit: "Exhibit" = Relationship(back_populates="photos")


class Exhibit(SQLModel, table=True):
    __tablename__ = "exhibits"

    id: int | None = Field(default=None, primary_key=True)
    
    # Основные характеристики
    name: str = Field(max_length=255, nullable=False, description="Название экспоната")
    dating: str = Field(default=None, max_length=100, description="Датировка (например, 'XII век', '1500-1520 гг.')")
    material: str = Field(default=None, max_length=200, description="Материал изготовления")
    technique: str = Field(default=None, max_length=200, description="Техника исполнения")
    dimensions: str = Field(default=None, max_length=100, description="Размеры (например, '45x30x20 см')")
    description: str = Field(default=None, description="Описание экспоната")
    condition: str = Field(default=None, max_length=200, description="Сохранность (например, 'Хорошая', 'Требуется реставрация')")

    exposition_id: Optional[int] = Field(default=None, foreign_key="expositions.id", description="ID экспозиции")

    created_at: datetime = Field(default_factory=datetime.utcnow, description="Дата добавления в базу")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Дата последнего обновления")

    #связи
    exposition: Optional["Exposition"] = Relationship(back_populates="exhibits")
    photos: List[ExhibitPhoto] = Relationship(back_populates="exhibit", sa_relationship_kwargs={"cascade": "all, delete-orphan"})



