from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# DTO для фотографий
class ExhibitPhotoBase(BaseModel):
    photo_url: str
    is_primary: bool = False

class ExhibitPhotoCreate(ExhibitPhotoBase):
    exhibit_id: int

class ExhibitPhotoRead(ExhibitPhotoBase):
    id: int
    exhibit_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

class ExhibitPhotoUpdate(BaseModel):
    """Схема для обновления фото"""
    photo_url: Optional[str] = None
    is_primary: Optional[bool] = None




#Модели для API (Create/Update/Read)
class ExhibitBase(BaseModel):
    name: str
    dating: str = None
    material: str = None
    technique: str = None
    dimensions: str = None
    description: str = None
    condition: str = None
    exposition_id: int = None

class ExhibitCreate(ExhibitBase):
    pass

class ExhibitUpdate(BaseModel):
    name: Optional[str] = None
    dating: Optional[str] = None
    material: Optional[str] = None
    technique: Optional[str] = None
    dimensions: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[str] = None
    exposition_id: Optional[int] = None
    inventory_number: Optional[str] = None


class ExhibitRead(ExhibitBase):
    id: int
    created_at: datetime
    updated_at: datetime
    photos: List[ExhibitPhotoRead] = []
    
    class Config:
        from_attributes = True

