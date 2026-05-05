from pydantic import BaseModel, ConfigDict
from typing import Optional, List, TYPE_CHECKING

# Используем TYPE_CHECKING для избежания циклических импортов
if TYPE_CHECKING:
    from schemas.exhibit import ExhibitRead

# ========== Базовые схемы ==========
class ExpositionBase(BaseModel):
    """Базовая схема экспозиции"""
    name: str
    description: Optional[str] = None
    location: Optional[str] = None

# ========== Схемы для создания ==========
class ExpositionCreate(ExpositionBase):
    """Схема для создания экспозиции"""
    #pass

# ========== Схемы для чтения ==========
class ExpositionRead(ExpositionBase):
    """Схема для чтения экспозиции (ответ API)"""
    id: int
    exhibits: List["ExhibitRead"] = []
    
    model_config = ConfigDict(from_attributes=True)

# ========== Схемы для обновления ==========
class ExpositionUpdate(BaseModel):
    """Схема для обновления экспозиции (все поля опциональны)"""
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None