from authx import AuthX, AuthXConfig
from backend.config import settings

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
config.JWT_ACCESS_COOKIE_NAME = settings.JWT_ACCESS_TOKEN_NAME
config.JWT_REFRESH_COOKIE_NAME = settings.JWT_REFRESH_TOKEN_NAME
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)
