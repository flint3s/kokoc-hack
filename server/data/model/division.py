from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship

from data.model.company import Company

class Division(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(default=None, nullable=False)
    company_id: int = Field(foreign_key="company.id")
    company: Optional["Company"] = Relationship(
        back_populates="divisions"
    )
    employees: List["Employee"] = Relationship(back_populates="division", sa_relationship_kwargs={'lazy': 'selectin'})