import os

from dotenv import load_dotenv


load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')
    FACE_ClOUD_TOKEN = os.getenv('FACE_ClOUD_TOKEN')
    EMAIL_NAME = os.getenv('EMAIL_NAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    FACE_CLOUD_URL = os.getenv('FACE_CLOUD_URL')
    FILEPATH = os.getenv('FILEPATH')
    MAX_FILE_SIZE_MB = os.getenv('MAX_FILE_SIZE_MB')
