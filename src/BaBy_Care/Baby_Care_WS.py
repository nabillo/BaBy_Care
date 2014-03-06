'''
Created on Feb 19, 2014

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

with app.test_request_context():
  if not db.has_key('lvl_normal'):
		db['lvl_normal'] = app.config['LVL_NORMAL']
	if not db.has_key('normal_interval'):
		db['normal_interval'] = app.config['NORMAL_INTERVAL']
	if not db.has_key('active_interval'):
		db['active_interval'] = app.config['ACTIVE_INTERVAL']
	if not db.has_key('agi_normal'):
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

from Baby_Care_Stream import steam_ctr_exe

@app.route('/stream_ctr.json', methods=['POST'])
def stream_ctr():
	"""Control streamer.
	
	@Imput    command : [Start,Stop,Restart].
	@Return   result.
	"""
	
	log.debug('stream_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	log.info(data['command'])
	if (command == 'Start') :
		result = steam_ctr_start()
	elif (command == 'Stop') :
		result = steam_ctr_stop()
	elif (command == 'Restart') :
		result = steam_ctr_restart()
	else:
		log.info('invalid command')
		result = 'None'
	
	log.debug('stream_ctr END')
	return jsonify(result=result)

@app.route('/activity_ctr.json', methods=['POST'])
def activity_ctr():
	"""Control activity.
	
	@Imput    command : [Start,Stop,Calibrate].
	          agi_normal (decimal).
	@Return   result.
	"""
	
	log.debug('activity_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	if (data['command'] == 'Start') :
		# Start the agitation controller
		agi_job = agitation_ctr_exe.delay()
		result = agi_job.AsyncResult(agi_job.id).state
		if (result == states.SUCCESS):
			# Start the activity controller
			act_job = activity_ctr_exe.delay()
			result = act_job.AsyncResult(act_job.id).state
	elif (data['command'] == 'Stop') :
		# Stop the activity controller
		revoke(act_job.id, terminate=True, signal='SIGTERM')
		# Stop the agitation controller
		revoke(agi_job.id, terminate=True, signal='SIGTERM')
	elif (data['command'] == 'Calibrate') :
		# Calibrate the normale sound level
		result = normal_levels(data['agi_normal'])
		#TODO : adjust intervals
	else:
		log.info('invalid command')
		result = 'None'
	
	log.debug('activity_ctr END')
	return jsonify(result=result)
	
@app.route('/media_ctr.json', methods=['POST'])
def media_ctr():
	"""Control media center.
	
	@Imput    command : [Upload,Delete,List,Play,Stop,VolUp,VolDown].
	          num (decimal).
	@Return   result.
	"""
	
	log.debug('media_ctr BEGIN')
	
	# Get the JSON data sent from the form
	data = request.get_json(force=True)
	
	if (data['command'] == 'Upload') :
		result = media_upload()
	elif (data['command'] == 'Delete') :
		result = media_del(data['num'])
	elif (data['command'] == 'List') :
		result = media_list()
	else:
		log.info('invalid command')
		result = 'None'
		
	log.debug('media_ctr END')
	return jsonify(result=result)
	
if __name__ == '__main__':
	app.run(
			host="0.0.0.0",
			port=int(app.config['PORT'])
	)
	
