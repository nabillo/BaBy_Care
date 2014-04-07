'''
Created on Feb 19, 2014

@author: nabillo
'''

import alsaaudio, audioop
import signal
from BaBy_Care import app, celery, log, db
from subprocess import check_call, CalledProcessError


# constants

CARD        = 'sysdefault:CARD=CameraB409241'
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 16000
FRAMESIZE   = 1024

global state_err1
global state_err2

def sound_level() :
	"""calculate sound level.
	
	@Imput    .
	@Return   energy.
	"""
	
	log.info('calculate sound level')
# 	# set up audio input
	card = CARD
	recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NORMAL, card)
	recorder.setchannels(CHANNELS)
	recorder.setrate(RATE)
	recorder.setformat(INFORMAT)
	recorder.setperiodsize(FRAMESIZE)
	
	[length, data]=recorder.read()
	log.debug('length : %f',length)
	volume = audioop.max(data, 2)
	log.debug("volume : %f",volume)
	volume = audioop.rms(data, 2)
	log.debug("volume : %f",volume)
	return volume

@celery.task
def activity_check() :
	"""Evaluate sound and agitation level.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Evaluate sound and agitation level')
	
	global state_err1
	global state_err2
	energy = sound_level()
	
	if (energy < db['lvl_normal']) :
		# Quiet state
		log.debug('Quiet state on agitation !!!')
		state_err1 = state_err1 + 1
		# We reduce the normal level if that has has been reproduced many times
		if (state_err1 > app.config['STATE_ERROR']) :
			db['lvl_normal'] = db['lvl_normal'] * ((2 * app.config['REDUCTION_RATE'])/100)
			state_err1 = 0
		
	elif ((energy >= db['lvl_normal']) and (energy < db['lvl_normal'] + db['normal_interval'])) :
		# Normal state
		log.debug('Normal state with agitation')
		state_err2 = state_err2 + 1
		# We reduce the normal level if that has has been reproduced many times
		if (state_err2 > app.config['STATE_ERROR']) :
			db['lvl_normal'] = db['lvl_normal'] * app.config['REDUCTION_RATE']/100
			state_err2 = 0
			
	elif ((energy >= db['lvl_normal'] + db['normal_interval']) and (energy < db['lvl_normal'] + db['normal_interval'] + db['active_interval'])) :
		# Active state
		log.debug('Active state with agitation')
		#TODO : Tigger alarm
		
	elif (energy >= db['lvl_normal'] + db['normal_interval'] + db['active_interval']) :
		# Criying state
		log.debug('Criying state with agitation !!!')
		#TODO : Tigger alarm

def terminate() :
	"""Free resources.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Free resources')

	signal.alarm(0)
	#GPIO.cleanup()
	exit(0)

def handler(signum, frame) :
	"""Signals handler.
		SIGTERM to stop controller gracefully
		SIGALRM handle activity controller alarm
		SIGPROF handle agitation 
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Signals handler')
	log.debug('signal : %d',signum)
	if (signum == signal.SIGTERM) :
		terminate()
	elif (signum == signal.SIGALRM) :
		activity_check()
		act_job = activity_check.delay()
		result = act_job.AsyncResult(act_job.id).state
		log.debug('activity check result : %s',result)

def activity_ctr_start() :
	"""Start Motion for activity control.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Start Motion')
	
	if (signal.getsignal(signal.SIGALRM) == None) :
		# Set the signal handler
		signal.signal(signal.SIGALRM, handler)
	
	# Send resume command to Motion
	try :
		check_call(["motion-control","detection","resume",0])
		result = 'Success'
	except CalledProcessError as e:
		log.exception('Motion resume error : %s',e.returncode)
		result = 'Error'
	
	return result
	
def activity_ctr_stop():
	"""Stop Motion and activity control.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Stop Motion')
	
	# Send resume command to Motion
	try :
		check_call(["motion-control","detection","pause",0])
		result = 'Success'
	except CalledProcessError as e:
		log.exception('Motion resume error : %s',e.returncode)
		result = 'Error'
		
	# Stop timer for crying check
	signal.setitimer(signal.ITIMER_PROF, 0)

def activity_event_begin() :
	"""A Baby event has started.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Baby Event started')
	
	# setup alarm to evaluate agitation level
	signal.alarm(app.config['AGI_NORMAL'])

def activity_event_end() :
	"""A Baby event has ended.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Baby Event ended')
	
	# cancel alarm
	signal.alarm(0)

def normal_levels(agi_normal) :
	"""Calibrate the normal level to actual sound level.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Calibration')
	try :
		db['lvl_normal'] = sound_level()
		log.debug("lvl_normal : %f",db['lvl_normal'])
		result = 'Success'
	except:
		log.exception('Calibration error')
		result = 'Error'
	return result 
		
