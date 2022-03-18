import os
class Config:
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'you_will_never_guess'
    SQLALCHEMY_DATABASE_URI= os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')