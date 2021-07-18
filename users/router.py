from fastapi import APIRouter, Depends
from typing import List

from .dependencies import get_user_repository, UserRepository
from .models import User, CreateUserParams

router = APIRouter()


@router.get("/", response_model=List[User])
async def list_users(repository: UserRepository = Depends(get_user_repository)):
    users = await repository.list_users()
    return users


@router.post("/", response_model=User, status_code=201)
async def create_user(params: CreateUserParams, repository: UserRepository = Depends(get_user_repository)):
    user = await repository.create_user(params)
    return user
