'''
Created on Feb 19, 2014

@author: nabillo
'''

import alsaaudio, audioop
from BaBy_Care import app, celery, log, db
from subprocess import check_call, CalledProcessError

import signal
import RPi.GPIO as GPIO


# constants

CARD        = 'sysdefault:CARD=CameraB409241'
CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 16000
FRAMESIZE   = 1024

global state_err1
global state_err2
global refresh_rate
global activity_status

def sound_level(framesize) :
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
	recorder.setperiodsize(framesize)
	
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
	
	global state_err
	energy = sound_level(FRAMESIZE)
	
	if (energy < db['lvl_normal']) :
		# Quiet state
		log.debug('Quiet state on agitation !!!')
		state_err1 = state_err1 + 1
		# We reduce the normal level if that has has been reproduced many times
		if (state_err1 > app.config['STATE_ERROR']) :
			db['lvl_normal'] = db['lvl_normal'] * ((2 * app.config['REDUCTION_RATE'])/100)
			state_err1 = 0
		
	elif ((energy >= db['lvl_normal']) and (energy < db['lvl_BaBy_Carenormal'] + db['normal_interval'])) :
		# Normal state
		log.debug('Normal state with agitation')
		state_err2 = state_err2 + 1
		# We reduce the normal level if that has has been reproduced many times
		if (state_err2 > app.config['STATE_ERROR']) :
			db['lvl_normal'] = db['lvl_normal'] * (app.config['REDUCTION_RATE']/100)
			state_err2 = 0
			
	elif ((energy >= db['lvl_normal'] + db['normal_interval']) and (energy < db['lvl_normal'] + db['normal_interval'] + db['active_interval'])) :
		# Active state
		log.debug('Active state with agitation')
		#TODO : Trigger alarm
		
	elif (energy >= db['lvl_normal'] + db['normal_interval'] + db['active_interval']) :
		# Crying state
		log.debug('Crying state with agitation !!!')
		#TODO : Trigger alarm

@celery.task
def crying_check() :
	"""Check baby crying and trigger alarm to Android app.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Check baby crying')
	
	energy = sound_level(0.3 * db['cry_normal'])
	
	if (energy >= db['lvl_normal'] + db['normal_interval'] + db['active_interval']) :
		# Crying state
		log.debug('Crying state !!!')
		#TODO : Trigger alarm

def terminate() :
	"""Free resources.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Free resources')

	signal.alarm(0)
	signal.setitimer(signal.ITIMER_PROF, 0)
	GPIO.cleanup()
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
	log.debug('signal : %d , SIGALRM : %d, SIGPROF : %d',signum,signal.SIGALRM,signal.SIGPROF)
	if (signum == signal.SIGTERM) :
		terminate()
	elif (signum == signal.SIGALRM) :
		act_job = activity_check.delay()
		result = act_job.state
		log.debug('activity check result : %s',result)
	elif (signum == signal.SIGPROF) :
		cry_job = crying_check.delay()
		result = cry_job.state
		log.debug('crying check result : %s',result)
	else :
		log.debug('not handled ')

def activity_ctr_start() :
	"""Start Motion for activity control.
	
	@Imput    .
	@Return   .
	"""
	
	global activity_status
	log.info('Start Motion')
		
	activity_status = True
	# launch timer for crying check
	signal.setitimer(signal.ITIMER_PROF, db['cry_normal'], db['cry_normal'])

def activity_ctr_stop() :
	"""Stop Motion and activity control.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Stop Motion')
	
	activity_status = False
	# Stop timer for crying check
	signal.setitimer(signal.ITIMER_PROF, 0)

def activity_event_begin() :
	"""A Baby event has started.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Baby Event started')
	
	if (activity_status == True) :
		# setup alarm to evaluate agitation level
		signal.alarm(db['agi_normal'] )

def activity_event_end() :
	"""A Baby event has ended.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Baby Event ended')
	
	# cancel alarm
	signal.alarm(0)

def normal_levels(agi_normal, cry_normal) :
	"""Calibrate the normal level to actual sound level.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Calibration')
	try :
		db['lvl_normal'] = sound_level()
		db['agi_normal'] = agi_normal
		db['cry_normal'] = cry_normal
		log.debug("lvl_normal : %f, agi_normal %d, cry_normal %d",db['lvl_normal'],db['agi_normal'],db['cry_normal'])
		result = 'Success'
	except:
		log.exception('Calibration error')
		result = 'Error'
	return result 
		
