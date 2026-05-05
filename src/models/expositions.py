from typing import List
from sqlmodel import SQLModel, Field, Relationship

class Exposition(SQLModel, table=True):
    __tablename__ = "expositions"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    description: str = Field(default=None)
    location: str = Field(default=None, max_length=10)

    exhibits: List["Exhibit"] = Relationship(back_populates="exposition")
