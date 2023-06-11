from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    db_host_test: str
    db_port_test: int
    db_name_test: str
    db_user_test: str
    db_pass_test: str

    server_host: str
    server_port: int
    front_end_host: str
    front_end_port: int

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


setting = Settings(_env_file=".env", _env_file_encoding="utf-8")