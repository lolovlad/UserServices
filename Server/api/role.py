from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse

from ..models.Role import RoleGet, Role
from ..models.Message import Message

from ..services.RoleServices import RoleServices

from typing import List

router = APIRouter(prefix="/role")


@router.post("/", responses={
    status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": Message},
    status.HTTP_201_CREATED: {"model": Message}
})
async def add_role(role: Role, role_services: RoleServices = Depends()):
    try:
        await role_services.add_role(role)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"content": "create new role"})
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"content": "role create error"})


@router.get("/{id_role}/", response_model=RoleGet, responses={
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_role(id_role: int, role_services: RoleServices = Depends()):
    try:
        return await role_services.get_role(id_role)
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"content": "role not found"})


@router.get("/all/", response_model=List[RoleGet], responses={
    status.HTTP_404_NOT_FOUND: {"model": Message}
})
async def get_all_role(role_services: RoleServices = Depends()):
    try:
        return await role_services.get_all_role()
    except ValueError:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"content": "role not found"})