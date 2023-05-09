from pydantic import BaseSettings


class Settings(BaseSettings):
    url_base: str = "File/base.db"
    url_base_test: str
    server_host: str
    server_port: int
    front_end_host: str
    front_end_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


setting = Settings(_env_file=".env", _env_file_encoding="utf-8")