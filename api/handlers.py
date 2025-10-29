from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .actions.auth import get_current_user_from_token
from .actions.users import _create_new_user
from .actions.users import _delete_user
from .actions.users import _get_user_by_id
from .actions.users import _update_user
from .actions.users import check_user_permissions
from api.models import DeleteUserResponse
from api.models import ShowUser
from api.models import UpdatedUserResponse
from api.models import UpdateUserRequest
from api.models import UserCreate
from db.models import User
from db.session import get_db


logger = getLogger(__name__)
user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error:{err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:

    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(status_code=404, detail="User with id {user_id} not found")
    if not check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id in None:
        raise HTTPException(status_code=404, detail=f"User with{user_id} not found")
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} nor found")
    raise user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user_from_token),
) -> UpdatedUserResponse:

    # Преобразуем Pydantic модель в обычный dict
    update_user_params = body.model_dump(exclude_none=True)
    if update_user_params:
        raise HTTPException(
            status_code=422, detail="At least one parameter for user update info"
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if not check_user_permissions(
        target_user_for_action=user_for_update, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        update_user_id = await _update_user(body=body, session=db, user_id=user_id)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error:{err}")
    return UpdatedUserResponse(updated_user_id=update_user_id)
