import os
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Mysql40045544@localhost/bingo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)