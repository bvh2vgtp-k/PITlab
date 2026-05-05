from schemas.users import (
    UserBase, UserCreate, UserPublic, 
    UserUpdate, UserLogin
)

from schemas.exhibits import (ExhibitBase, ExhibitCreate, ExhibitRead, 
    ExhibitUpdate, ExhibitPhotoBase, ExhibitPhotoCreate, 
    ExhibitPhotoRead, ExhibitPhotoUpdate)

from schemas.expositions import (
    ExpositionBase,
    ExpositionCreate,
    ExpositionUpdate,
    ExpositionRead,
)

ExhibitRead.model_rebuild()
ExpositionRead.model_rebuild()

__all__ = [
    'UserBase', 'UserCreate', 'UserPublic',
    'UserUpdate', 'UserLogin',

    # Exhibit schemas
    'ExhibitBase', 'ExhibitCreate', 'ExhibitUpdate', 'ExhibitRead',
    
    # ExhibitPhoto schemas
    'ExhibitPhotoBase', 'ExhibitPhotoCreate', 'ExhibitPhotoRead', 'ExhibitPhotoUpdate',

    'ExpositionBase', 'ExpositionCreate', 'ExpositionUpdate', 'ExpositionRead',
]
