import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///service_shop.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    CACHE_TYPE = "SimpleCache"
    HOST = "0.0.0.0"
    PORT = "443"
