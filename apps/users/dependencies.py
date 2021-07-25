import aiohttp

from typing import Any, Dict, List

from fastapi import Depends

from .models import User, CreateUserParams


class UserRepository:
    def __init__(self, session):
        self._endpoint = "https://jsonplaceholder.typicode.com/users"
        self._session = session

    async def list_users(self) -> List[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]

    async def create_user(self, params: CreateUserParams) -> User:
        raw_user = await self._create_user(params)
        return self._convert_user(raw_user)

    async def _list_users(self):
        resp = await self._session.get(self._endpoint)
        raw_users = await resp.json()
        return raw_users

    async def _create_user(self, params):
        resp = await self._session.post(self._endpoint, json=params.dict())
        raw_user = await resp.json()
        return raw_user

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)


async def get_session() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession() as session:
        yield session


class UserRepositoryFactory:
    async def __call__(self, session: aiohttp.ClientSession = Depends(
        get_session)) -> UserRepository:
        return UserRepository(session=session)


get_user_repository = UserRepositoryFactory()
