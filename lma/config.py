import os

from environs import Env

env = Env()

path = os.getcwd()
env.read_env(".env")

DEBUG = env.bool('DEBUG', False)

SECRET_KEY = env('SECRET_KEY')

DB_NAME = env('DB_NAME')
DB_USER = env('DB_USER')
DB_PASSWORD = env('DB_PASSWORD')
DB_HOST = env('DB_HOST')
DB_PORT = env('DB_PORT')
DB_USER_OWNER = env('DB_USER_OWNER')
DB_PASSWORD_OWNER = env('DB_PASSWORD_OWNER')
