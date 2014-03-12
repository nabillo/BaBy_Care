'''
Created on Feb 19, 2014

@author: nabillo
'''

from subprocess import Popen, PIPE
	
def steam_ctr_start() :
	"""Start streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Start streamer')

	result = 'Error'
	gst = Popen(["Streamer.sh","Start"])
	gst.poll()
	log.info('return code : %s',gst.returncode)
	if (gst.returncode == 0) :
		log.info('Gstreamer Started')
		result = 'Success'

	return result
	
def steam_ctr_stop() :
	"""Stop streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Stop streamer')
	result = 'Error'
	gst = Popen(["Streamer.sh","Stop"])
	gst.poll()
	log.info('return code : %s',gst.returncode)
	if (gst.returncode == 0) :
		log.info('Gstreamer Stoped')
		result = 'Success'

	return result
def steam_ctr_restart() :
	"""Restart streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Restart Streamer')
	result = 'Error'
	gst = Popen(["Streamer.sh","Restart"])
	gst.poll()
	log.info('return code : %s',gst.returncode)
	if (gst.returncode == 0) :
		log.info('Gstreamer Restarted')
		result = 'Success'

	return result
