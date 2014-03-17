'''
Created on Mar 06, 2014

@author: nabillo
'''

from flask import Flask
from flask.ext.zodb import ZODB
from celery import Celery
from celery.task.control import revoke
from celery.result import AsyncResult
import logging

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('BaBy_Care.config')

log = logging.getLogger(__name__)
log.setLevel(app.config['LOG_LEVEL'])
# add a file rotation handler of 1Mb of size and 3 backups
fh = logging.handlers.RotatingFileHandler(app.config['LOG_FILE'], maxBytes=1048576, backupCount=3)
fh.setLevel(app.config['LOG_LEVEL'])
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('[%(asctime)s] - %(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
log.addHandler(fh)

celery = Celery('baby_care')
celery.conf.update(app.config)

db = ZODB(app)

@app.before_first_request
def before_first_request():
    if not db.has_key('lvl_normal') :
        db['lvl_normal'] = app.config['LVL_NORMAL']
    if not db.has_key('normal_interval') :
        db['normal_interval'] = app.config['NORMAL_INTERVAL']
    if not db.has_key('active_interval') :
        db['active_interval'] = app.config['ACTIVE_INTERVAL']
    if not db.has_key('agi_normal') :
        db['agi_normal'] = app.config['AGI_NORMAL']

import Baby_Care_WS

