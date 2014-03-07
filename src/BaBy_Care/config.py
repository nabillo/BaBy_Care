'''
Created on Feb 19, 2014

@author: nabillo
'''

# Private app key
SECRET_KEY= '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

# Set to False on production
DEBUG = True

# Celery broker and backend url
#TODO : normalyse ports
CELERY_BROKER_URL= 'redis://localhost:6379',
CELERY_RESULT_BACKEND= 'redis://localhost:6379'

# Sound normal level
LVL_NORMAL = 100
# Interval lenght of normal sound level normal to active
NORMAL_INTERVAL = 10
# Interval lenght of active sound level active to agitation
ACTIVE_INTERVAL = 20
# Normal agitation frequency per minute
AGI_NORMAL = 10

# Period for acquisition of sound level
REFRESH_RATE = 10

# Persistancy storage location
ZODB_STORAGE = 'file://BaByCare.fs'

# Media upload location
UPLOAD_FOLDER = ''
# Media allowed extention
ALLOWED_EXTENSIONS = set(['mp3', 'mp4'])
# Maximum zise of media file
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# GPIO port number
GPIO_CHANNEL = 23
  
