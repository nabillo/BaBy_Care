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

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
# add a file handler
fh = logging.FileHandler("%s.log" % __name__)
fh.setLevel(logging.DEBUG)
# create a formatter and set the formatter for the handler.
frmt = logging.Formatter('[%(asctime)s] - %(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(frmt)
# add the Handler to the logger
log.addHandler(fh)

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('BaBy_Care.config')

celery = Celery('baby_care')
celery.conf.update(app.config)

db = ZODB(app)

'''with app.test_request_context() :
    if not db.has_key('lvl_normal') :
        db['lvl_normal'] = app.config['LVL_NORMAL']
    if not db.has_key('normal_interval') :
        db['normal_interval'] = app.config['NORMAL_INTERVAL']
    if not db.has_key('active_interval') :
        db['active_interval'] = app.config['ACTIVE_INTERVAL']
    if not db.has_key('agi_normal') :
        db['agi_normal'] = app.config['AGI_NORMAL']
'''
import Baby_Care_WS

