from datetime import timedelta
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