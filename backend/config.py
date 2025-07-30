from datetime import timedelta
from flask_caching import Cache

cache=Cache()
class Config:
    DEBUG= False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'salt'  
    JWT_SECRET_KEY='secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  # No expiration for local development
    CACHE_TYPE='redis'
    CACHE_REDIS_HOST='localhost'
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_DB=0
    CACHE_REDIS_URL='redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT=300  # 5 minutes
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_EMAIL = 'admin@gmail.com'
    MAIL_PASSWORD = 'admin'
