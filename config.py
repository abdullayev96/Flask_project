# import secrets
#
# class Config:
#
#     print(secrets.token_hex(24))
#     SECRET_KEY = 'be7d521da76feff5d2a0278f259f2659c6bb61067c9c11f4'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False