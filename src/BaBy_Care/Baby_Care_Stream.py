'''
Created on Feb 19, 2014

@author: nabillo
'''

from subprocess import check_call, CalledProcessError
from BaBy_Care import log
	
def steam_ctr_start() :
	"""Start streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.info('Start streamer')

	try :
		check_call(["./Streamer.sh","Start"])
		result = 'Success'
	except CalledProcessError as e:
		log.exception('gst launch error : %s',e.returncode)
		result = 'Error'

	return result
	
def steam_ctr_stop() :
	"""Stop streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.info('Stop streamer')
	try :
		check_call(["./Streamer.sh","Stop"])
		result = 'Success'
	except CalledProcessError as e:
		log.exception('gst stop error : %s',e.returncode)
		result = 'Error'

	return result
def steam_ctr_restart() :
	"""Restart streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.info('Restart Streamer')
	result = 'Error'
	try :
		check_call(["./Streamer.sh","Restart"])
		result = 'Success'
	except CalledProcessError as e:
		log.exception('gst restart error : %s',e.returncode)
		result = 'Error'
		
	return result
