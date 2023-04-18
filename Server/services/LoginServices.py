from jose import JWTError, jwt

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer

from ..repositories import UserRepository

from ..models.Message import Token, LoginResponse
from ..models.User import UserLogin, GetUser

from ..settings import setting
from datetime import datetime, timedelta

oauth2_cheme = OAuth2PasswordBearer(tokenUrl='/v1/login/sign-in/')


def get_current_user(token: str = Depends(oauth2_cheme)) -> GetUser:
    return LoginServices.validate_token(token)


class LoginServices:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository: UserRepository = user_repository

    @classmethod
    def validate_token(cls, token: str) -> GetUser:
        exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail="token",
                                  headers={
                                      "AGUContest": 'Bearer'
                                  })
        try:
            payload = jwt.decode(token,
                                 setting.secret_key,
                                 algorithms=[setting.algorithm])
        except JWTError:
            raise exception

        user_data = payload.get("user")

        try:
            user = GetUser.parse_obj(user_data)
        except Exception:
            raise exception
        return user

    @classmethod
    def create_token(cls, user: GetUser) -> Token:
        user_data = user

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=setting.access_token_expire_minutes * 60),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(payload,
                           setting.secret_key,
                           algorithm=setting.algorithm)
        return Token(access_token=token, token_type='bearer')

    async def login_user(self, user_login: UserLogin, request: Request) -> LoginResponse:
        user = await self.__user_repository.get_by_login(user_login.login)
        if user:
            if user.check_password(user_login.password):
                token = self.create_token(GetUser.from_orm(user))
                return LoginResponse(**token.dict(), type_user=user.type_user)