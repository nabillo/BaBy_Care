'''
Created on Feb 19, 2014

@author: nabillo
'''

import alsaaudio, struct
from aubio.task import *

from BaBy_Care import app, celery, log, db

import signal
import RPi.GPIO as GPIO


# constants

CHANNELS    = 1
INFORMAT    = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE        = 44100
FRAMESIZE   = 1024
PITCHALG    = aubio_pitch_yin
PITCHOUT    = aubio_pitchm_freq

global refresh_count1
global refresh_count2

if not db.has_key('lvl_normal') :
	db['lvl_normal'] = app.config['LVL_NORMAL']
if not db.has_key('normal_interval') :
	db['normal_interval'] = app.config['NORMAL_INTERVAL']
if not db.has_key('active_interval') :
	db['active_interval'] = app.config['ACTIVE_INTERVAL']
if not db.has_key('agi_normal') :
	db['agi_normal'] = app.config['AGI_NORMAL']

def sound_level() :
	"""calculate sound level.
	
	@Imput    .
	@Return   energy.
	"""
	
	[length, data]=recorder.read()
	# convert to an array of floats
	floats = struct.unpack('f'*FRAMESIZE,data)
	# copy floats into structure
	for i in range(len(floats)):
		fvec_write_sample(buf, floats[i], 0, i)
	# find pitch of audio frame
	freq = aubio_pitchdetection(detect,buf)
	# find energy of audio frame
	energy = vec_local_energy(buf)
	log.info("{:10.4f} {:10.4f}".format(freq,energy))
	
	return energy

def activity_check() :
	"""Evaluate sound and agitation level.
	
	@Imput    .
	@Return   .
	"""
	
	energy = sound_level()
	
	if (energy < db['lvl_normal']) :
		# Quiet state
		log.info('Quiet state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		refresh_count2 = 0
		
	elif ((energy >= db['lvl_normal']) and (energy < db['lvl_normal'] + db['normal_interval'])) :
		# Normal state
		log.info('Normal state')
		refresh_count2 = 0
		# If agitation stay higher than normal for a configurable periode 
		if (db['mvt_count'] > db['agi_normal']) and (refresh_count1 > app.config['REFRESH_COUNT']) :
			# We reduce the normal level
			db['lvl_normal'] = db['lvl_normal'] * (app.config['REDUCTION_RATE']/100)
			refresh_count1 = 0
			
		# If agitation is higher we increment timer counter
		elif (db['mvt_count'] > db['agi_normal']) :
			refresh_count1 = refresh_count1 + 1
			
		# If agitation return to normal we reset timer counter
		else :
			refresh_count1 = 0
		
	elif ((energy >= db['lvl_normal'] + db['normal_interval']) and (energy < db['lvl_normal'] + db['normal_interval'] + db['active_interval'])) :
		# Active state
		log.info('Active state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		# If active period is higher than a configurable periode 
		if (refresh_count2 > app.config['REFRESH_COUNT']) :
			# TODO : If agitation is higher we send silent notification
			# if (db['mvt_count'] > db['agi_normal']) :
			# We increase the normal level
			db['lvl_normal'] = db['lvl_normal'] * (1+(app.config['INCREASE_RATE']/100))
			refresh_count2 = 0
		else :
			refresh_count2 = refresh_count2 + 1
		
	elif (energy >= db['lvl_normal'] + db['normal_interval'] + db['active_interval']) :
		# Criying state
		log.info('Criying state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		refresh_count2 = 0
		# Tigger alarm

def agitation_count() :
	"""Retreive number of mvt per minute and store it on db.
	
	@Imput    .
	@Return   .
	"""
	
	global mvt_counter
	log.info('agitation count : %d',mvt_counter)
	db['mvt_count'] = mvt_counter
	mvt_counter = 0

def mvt_counter(channel) :
	"""incremente mvt conter on each call from GPIO triggering.
	
	@Imput    .
	@Return   .
	"""
	
	global mvt_counter
	mvt_counter = mvt_counter + 1

def agitation_detect() :
	"""Detect agitation from GPIO and call mvt_counter.
	
	@Imput    .
	@Return   .
	"""
	
	GPIO.setmode(GPIO.BCM)
	# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
	GPIO.setup(app.config['GPIO_CHANNEL'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(app.config['GPIO_CHANNEL'], GPIO.RISING, callback=mvt_counter, bouncetime=300)  

def terminate() :
	"""Free resources.
	
	@Imput    .
	@Return   .
	"""
	
	global recorder
	global detect
	global buf
	
	signal.alarm(0)
	del recorder
	del detect
	del buf
	GPIO.cleanup()
	sys.exit(0)

def handler(signum, frame) :
	"""handle signals.
		SIGTERM to stop controller gracefully
		SIGALRM handle activity controller alarm
		SIGPROF handle agitation 
	
	@Imput    .
	@Return   .
	"""
	
	log.info('signal : %d',signum)
	if (signum == signal.SIGTERM) :
		terminate()
	elif (signum == signal.SIGALRM) :
		activity_check()
	elif (signum == signal.SIGPROF) :
		agitation_count()

@celery.task
def activity_ctr_exe() :
	"""Activity controller task.
	
	@Imput    .
	@Return   .
	"""
	
	global recorder
	global detect
	global buf

	refresh_count1 = 0
	refresh_count2 = 0
	
	# Set the signal handler
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGALRM, handler)

	# set up audio input
	card = 'sysdefault:CARD=Microphone'
	recorder = alsaaudio.PCM(alsaaudio.PCM_CAPTURE,alsaaudio.PCM_NONBLOCK, card)
	recorder.setchannels(CHANNELS)
	recorder.setrate(RATE)
	recorder.setformat(INFORMAT)
	recorder.setperiodsize(FRAMESIZE)
	
	# set up pitch detect
	detect = new_aubio_pitchdetection(FRAMESIZE,FRAMESIZE/2,CHANNELS,RATE,PITCHALG,PITCHOUT)
	buf = new_fvec(FRAMESIZE,CHANNELS)
	
	# setup periodic alarm to evaluate sound level and set agitation level
	signal.alarm(app.config['REFRESH_RATE'])

@celery.task
def agitation_ctr_exe() :
	"""Agitation controller task.
	
	@Imput    .
	@Return   .
	"""
	
	with app.app_context():
		signal.setitimer(signal.ITIMER_PROF, 60, 60)
		agitation_detect()

def normal_levels(agi_normal) :
	"""Calibrate the normal level to actual sound level.
	
	@Imput    .
	@Return   .
	"""
	
	db['agi_normal'] = agi_normal
	db['lvl_normal'] = sound_level()
	log.info("Normal level : {:10.4f}".format(db['lvl_normal']))

