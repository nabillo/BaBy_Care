'''
Created on Feb 19, 2014

@author: nabillo
'''

from subprocess import Popen, PIPE

# Command sentence
gst_pid = 'ps -aef | grep "gst\-launch" | grep -v grep | awk "{print $2}"'

gst_kill = 'killall gst-launch-1.0'
gst_launch = ["gst-launch-1.0", "" ]

#pid = subprocess.check_output(gst_pid, shell=True)
#log.info('pid %s', pid)

gst = subprocess.Popen(gst_launch, stdout=subprocess.PIPE)
	
def steam_ctr_start() :
	"""Start streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Start streamer')
	try :
		log.info('Start Gstreamer')
		
		subprocess.call(gst_launch)
		
		log.info('Gstreamer Started')
		result = 'Success'
	except subprocess.CalledProcessError :
		# Streamer not started
		log.warning('Error starting Gstreamer')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def steam_ctr_stop() :
	"""Stop streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Stop streamer')
	try :
		log.info('Stop Gstreamer')
		
		subprocess.call(gst_kill)
		
		log.info('Gstreamer Stopped')
		result = 'Success'
	except subprocess.CalledProcessError :
		# Streamer not started
		log.warning('Error stopping Gstreamer')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def steam_ctr_restart() :
	"""Restart streamer.
	
	@Imput    .
	@Return   result.
	"""
	
	log.debug('Restart Streamer')
	try :
		log.info('Stop Gstreamer')
		
		subprocess.call(gst_kill)
		
		log.info('Gstreamer Stopped')
		log.info('Start Gstreamer')
		
		subprocess.call(gst_launch)
		
		log.info('Gstreamer Started')
		result = 'Success'
	except subprocess.CalledProcessError :
		# Streamer not started
		log.warning('Error stopping Gstreamer')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
