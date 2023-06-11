from fastapi import APIRouter, Depends, status, Response
from fastapi.responses import JSONResponse
from ..models.User import UserGet, UserPost
from ..models.Message import Message

from ..services.LoginServices import get_current_user

from pydantic.error_wrappers import ValidationError

from ..services.UserServices import UserServices

from typing import List

router = APIRouter(prefix="/user")


@router.get("/list_user/", response_model=List[UserGet], responses={
    status.HTTP_404_NOT_FOUND: {"model": Message},
})
async def get_list_page_users(response: Response,
                              num_page: int = 1,
                              role_user: int = 0,
                              user_service: UserServices = Depends(),
                              user: UserGet = Depends(get_current_user)):
    try:
        count_page = await user_service.get_count_page()
        count_user_in_page = user_service.count_user_in_page

        response.headers["X-Count-Page"] = str(count_page)
        response.headers["X-Count-Item-User"] = str(count_user_in_page)
        users = await user_service.get_list_user_page(num_page, role_user)
        return users
    except:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=Message(content="error").dict())


@router.get("/{id_user}/", response_model=UserGet, responses={status.HTTP_404_NOT_FOUND: {"model": Message}})
async def get_user(id_user: int,
                   user_service: UserServices = Depends(),
                   user: UserGet = Depends(get_current_user)):
    try:
        user = await user_service.get_user(id_user)
        return user
    except ValidationError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=Message(content="User not found").dict())


@router.post("/", responses={status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
                             status.HTTP_201_CREATED: {"model": Message}})
async def create_user(user: UserPost,
                      user_service: UserServices = Depends()):
    try:
        await user_service.add_user(user)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=Message(content="User create").dict())
    except ValidationError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=Message(content="User create error").dict())