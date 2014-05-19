'''
Created on Feb 19, 2014

@author: nabillo
'''

# Private app key
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

PORT = 12800

# Set to False on production
DEBUG = True
# logging information
#CRITICAL	50,ERROR	40,WARNING	30,INFO	20,DEBUG	10,NOTSET	0
LOG_LEVEL = 10
LOG_FILE = 'BaBy_Care.log'

# Celery broker and backend url
#TODO : normalyse ports
CELERY_BROKER_URL = 'amqp://',
CELERY_RESULT_BACKEND = 'amqp'

# Sound normal level
LVL_NORMAL = 100
# Interval lenght of normal sound level normal to active
NORMAL_INTERVAL = 10
# Interval lenght of active sound level active to agitation
ACTIVE_INTERVAL = 20
# Normal agitation time in second. This is the max period of agitation before launching an alarm 
AGI_NORMAL = 10
# Normal check period for crying in second
CRY_NORMAL = 30

# Number of inadequate Motion agitation detection and sound activity detection before decrising norma level
STATE_ERROR = 5

# Normal level decrising rate in %
REDUCTION_RATE = 10

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

# Alarm Port
ALARM_PORT = 12900

