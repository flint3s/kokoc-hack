import datetime

import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from data.database_service import DatabaseService
from data.model.user import User
from data.model.superadmin import SuperAdmin
from data.model.employee import Employee
from data.model.company import Company
from data.model.fund import Fund

from data.model.user_status import UserStatusEnum


class UserService:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_user(self, login: str, plain_password: str, role_id: int):
        hashed_password = bcrypt.hashpw(str.encode(plain_password), bcrypt.gensalt())
        created_user = User(login=login, password=hashed_password, role_id=role_id,
                            date=datetime.datetime.now(), user_status_id=UserStatusEnum.MODERATION.id)

        return await self.database_service.save(created_user)

    async def get_user_by_login(self, login: str):
        async with AsyncSession(self.database_service.engine) as session:
            st = select(User) \
                .where(User.login == login) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result:
                return result[0]

    async def get_user_by_id(self, user_id: int):
        async with AsyncSession(self.database_service.engine) as session:
            st = select(User) \
                .where(User.id == user_id) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result:
                return result[0]

    async def get_user_entity(self, user_id: int):
        """Возвращает сущность, привязанную к пользователю"""

        async with AsyncSession(self.database_service.engine) as session:
            st = select(User) \
                .where(User.id == user_id) \
                .limit(1)
            result = (await session.execute(st)).first()[0]

            if result:
                if result.role_id == 1:
                    st = select(SuperAdmin) \
                        .where(SuperAdmin.user_id == user_id)
                    return (await session.execute(st)).first()[0]

                elif result.role_id == 2:
                    st = select(Employee).options(selectinload(Employee.division)) \
                        .where(Employee.user_id == user_id)
                    return (await session.execute(st)).first()[0]

                elif result.role_id == 3:
                    st = select(Company) \
                        .where(Company.user_id == user_id)
                    return (await session.execute(st)).first()[0]

                elif result.role_id == 4:
                    st = select(Fund) \
                        .where(Fund.user_id == user_id)
                    return (await session.execute(st)).first()[0]

            return None

    async def check_user_password(self, login: str, plain_password: str):
        user = await self.get_user_by_login(login)
        if not user:
            raise HTTPException(401, "Неверный логин или пароль")

        return bcrypt.checkpw(str.encode(plain_password), str.encode(user.password))
