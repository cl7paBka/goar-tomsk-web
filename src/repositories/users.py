from typing import Optional

from sqlalchemy import insert, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User
from src.schemas.user import UserCreate, UserRead


class UsersRepository:
    async def create_user(self, session: AsyncSession, user_data: dict) -> UserRead:
        stmt = insert(User).values(**user_data).returning(User)
        result = await session.execute(stmt)
        await session.commit()

        created_user = result.scalars().first()
        # Преобразуем SQLAlchemy объект в pydantic-модель и сразу исключаем ленивые отношения
        user_dict = UserRead.model_validate(created_user).model_dump(exclude={'addresses', 'orders'})
        new_user = UserRead(**user_dict)
        return new_user

    #
    # @staticmethod
    # def get_user_by_username(session: Session, username: str) -> Optional[UserSchema]:
    #     statement = select(Users).options(joinedload(Users.prizes)).filter_by(username=username)
    #     result = session.execute(statement).unique()
    #
    #     user = result.scalar_one_or_none()
    #     if not user:
    #         return None
    #
    #     return user.to_read_model()
    #
    # @staticmethod
    # def update_user_balance(session: Session, user_id: int, value: int, task_id: int):
    #     statement = update(Users).where(Users.id == user_id).values(balance=Users.balance + value)
    #     result = session.execute(statement)
    #     logging.debug(result)
    #
    #     update_tasks_stmt = (
    #         update(Users)
    #         .where(Users.id == user_id)
    #         .values(done_tasks=func.array_append(Users.done_tasks, task_id))
    #     )
    #     result = session.execute(update_tasks_stmt)
    #     logging.debug(result)
    #
    #     session.commit()
    #
    #     statement = select(Users).filter_by(id=user_id)
    #     result = session.execute(statement)
    #     logging.debug(result)
    #
    #     user = result.scalar_one_or_none()
    #
    #     if not user:
    #         return None
    #     return user.to_read_model()
    #
    # @staticmethod
    # def update_user_personal_data(session: Session, username: str, new_data: UpdatePersonalDataSchema):
    #     update_values = {}
    #
    #     if new_data.full_name is not None and new_data.full_name != "":
    #         update_values['full_name'] = new_data.full_name
    #
    #     if new_data.group_number is not None and new_data.group_number != "":
    #         update_values['group_number'] = new_data.group_number
    #
    #     statement = update(Users).where(Users.username == username).values(**update_values)
    #     session.execute(statement)
    #     session.commit()
    #
    #     statement = select(Users).filter_by(username=username)
    #     result = session.execute(statement)
    #     user = result.scalar_one_or_none()
    #
    #     if not user:
    #         return None
    #     return user.to_read_model()
