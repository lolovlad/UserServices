from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from ..models.User import GetUser, PostUser
from ..models.Message import Message

from ..services.LoginServices import get_current_user

from pydantic.error_wrappers import ValidationError

from ..services.UserServices import UserServices

router = APIRouter(prefix="/user")


@router.get("/{id_user}", response_model=GetUser, responses={status.HTTP_404_NOT_FOUND: {"model": Message}})
async def get_user(id_user: int,
                   user_service: UserServices = Depends(),
                   user: GetUser = Depends(get_current_user)):
    try:
        user = await user_service.get_user(id_user)
        return user
    except ValidationError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=Message(content="User not found").dict())


@router.post("/", responses={status.HTTP_404_NOT_FOUND: {"model": Message},
                             status.HTTP_201_CREATED: {"model": Message}})
async def create_user(user: PostUser,
                      user_service: UserServices = Depends()):
    try:
        await user_service.add_user(user)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=Message(content="User create").dict())
    except ValidationError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=Message(content="User not found").dict())