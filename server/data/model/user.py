from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from data.model.role import Role


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    login: str = Field(default=None, nullable=False, unique=True)
    password: str = Field(default=None, nullable=False)

    role_id: int = Field(foreign_key="role.id")
    role: Optional["Role"] = Relationship(
        back_populates="users"
    )