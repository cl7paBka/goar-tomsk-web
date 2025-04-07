from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.db import get_async_session

from src.repositories.users import UsersRepository
from src.services.users import UsersService


def users_service(session: AsyncSession = Depends(get_async_session)) -> UsersService:
    users_repository = UsersRepository()
    return UsersService(users_repo=users_repository, session=session)


