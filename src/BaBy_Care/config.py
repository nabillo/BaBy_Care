'''
Created on Feb 19, 2014

@author: nabillo
'''

SECRET_KEY= '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

DEBUG = True

CELERY_BROKER_URL= 'redis://localhost:6379',
CELERY_RESULT_BACKEND= 'redis://localhost:6379'

LVL_NORMAL = 100
NORMAL_INTERVAL = 10
ACTIVE_INTERVAL = 20
AGI_NORMAL = 10

REFRESH_RATE = 10

ZODB_STORAGE = 'file://BaByCare.fs'

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

GPIO_CHANNEL = 23
