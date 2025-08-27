import os
from datetime import timedelta
from flask_caching import Cache

cache = Cache()

class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///quiz.db")

    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = 'salt'
    JWT_SECRET_KEY = 'secret'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # Redis (local)
    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST = 'localhost'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300

    # Mailhog (local dev)
    # For Gmail example (use App Passwords, not your actual Gmail password!)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv("MAIL_EMAIL", "your-email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-app-password")

    MAIL_DEFAULT_SENDER = os.getenv("MAIL_EMAIL", "your-email@gmail.com")



class ProductionConfig(Config):
    # Neon Postgres (use env var from Render for safety)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_smDJ0MoLpI8Y@ep-long-wave-a194lj9w-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "salt")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-production-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Redis on Render
    CACHE_TYPE = 'simple'  # fallback in case cache is used
    CACHE_DEFAULT_TIMEOUT = 300

    # SMTP for real emails (example: Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_EMAIL", "your-email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-app-password")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_EMAIL", "your-email@gmail.com")

