import os
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_file_path():
    for root, _, files in os.walk('.'):
        if '.env' in files:
            return os.path.join(root, '.env')


class Settings(BaseSettings):
    """App settings"""
    # Database
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # Test database
    DB_USER_TEST: str
    DB_PASS_TEST: str
    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str

    # Auth
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_NAME: str
    JWT_REFRESH_TOKEN_NAME: str

    model_config = SettingsConfigDict(env_file=get_env_file_path())

    @property
    def database_url_asyncpg(self):
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    @property
    def test_database_url_asyncpg(self):
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}')


settings = Settings()


if __name__ == '__main__':
    print(settings.test_database_url_asyncpg)
