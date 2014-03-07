'''
Created on Mar 06, 2014

@author: nabillo
'''

from flask import Flask, request, json, jsonify
from subprocess import Popen, PIPE
from flaskext.zodb import ZODB

import logging
import Baby_Care_Stream
import Baby_Care_Activity
from Baby_Care_Activity import celery

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object('config')

celery.conf.update(app.config)

db = ZODB(app)

with app.test_request_context() :
    if not db.has_key('lvl_normal') :
        db['lvl_normal'] = app.config['LVL_NORMAL']
    if not db.has_key('normal_interval') :
        db['normal_interval'] = app.config['NORMAL_INTERVAL']
    if not db.has_key('active_interval') :
        db['active_interval'] = app.config['ACTIVE_INTERVAL']
    if not db.has_key('agi_normal') :
        db['agi_normal'] = app.config['AGI_NORMAL']


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

import BaBy_Care.Baby_Care_WS

