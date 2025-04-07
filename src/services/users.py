from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user import UserCreate
from src.repositories.users import UsersRepository


class UsersService:
    """
    Service layer for managing users.

    This class provides methods to handle user-related operations, such as
    creating, retrieving, updating, and deleting users. It acts as a bridge
    between the repository layer and the application layer.
    """

    def __init__(
            self, session: AsyncSession,
            users_repo: UsersRepository
    ) -> None:
        """
        Initialize the UsersService with a user repository.
        """
        self.session = session
        self.users_repo = users_repo

    async def register_user(self, user: UserCreate):
        # Логика проверки зарегистрирован ли юзер
        # Если зарегистрирован -- выдаём, ответ, что юзер уже зарегистрирован и логиним его

        # Если не зарегистрирован
        # 1. Проверяем есть ли такой телефон юзера в БД -- если да, даём ошибку, если нет идём дальше
        # 2. Логика регистрации телефона через сервис (например, смс.ру или от мтс)
        # 3. При успехе - идём в бд и записываем юзера
        # 4. Создаём jwt-токен, записываем его в куки
        # 5. Выдаём 200 и ответ
        created_user = await self.users_repo.create_user(session=self.session, user_data=user)
        return {
            "status": 200,
            "user": created_user
        }
        # pass

    async def login_user(self):
        # Логика проверки зарегистрирован ли юзер
        pass
