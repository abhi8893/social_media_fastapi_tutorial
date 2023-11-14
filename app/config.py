from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  database_hostname: str
  database_port: str
  database_password: str
  database_name: str
  database_username: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int
  db_ssl_require: bool

  class Config:
    env_file = '.env'


settings = Settings()


if __name__ == '__main__':
  print(settings)