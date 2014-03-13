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

CARD        = 'sysdefault:CARD=Microphone'
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
	
	log.info('calculate sound level')
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
	log.info("freq : {:10.4f} energy : {:10.4f}".format(freq,energy))
	
	return energy

def activity_check() :
	"""Evaluate sound and agitation level.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Evaluate sound and agitation level')
	energy = sound_level()
	
	if (energy < db['lvl_normal']) :
		# Quiet state
		log.debug('Quiet state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		refresh_count2 = 0
		
	elif ((energy >= db['lvl_normal']) and (energy < db['lvl_normal'] + db['normal_interval'])) :
		# Normal state
		log.debug('Normal state')
		refresh_count2 = 0
		# If agitation stay higher than normal for a configurable periode 
		if (db['mvt_count'] > db['agi_normal']) and (refresh_count1 > app.config['REFRESH_COUNT']) :
			log.debug('if-refresh_count1 : %s',refresh_count1)
			# We reduce the normal level
			db['lvl_normal'] = db['lvl_normal'] * (app.config['REDUCTION_RATE']/100)
			log.debug('new lvl_normal : %s',db['lvl_normal'])
			refresh_count1 = 0
			
		# If agitation is higher we increment timer counter
		elif (db['mvt_count'] > db['agi_normal']) :
			refresh_count1 = refresh_count1 + 1
			log.debug('elif-refresh_count1 : %s',refresh_count1)
			
		# If agitation return to normal we reset timer counter
		else :
			refresh_count1 = 0
			log.debug('else-refresh_count1 : %s',refresh_count1)
		
	elif ((energy >= db['lvl_normal'] + db['normal_interval']) and (energy < db['lvl_normal'] + db['normal_interval'] + db['active_interval'])) :
		# Active state
		log.debug('Active state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		# If active period is higher than a configurable periode 
		if (refresh_count2 > app.config['REFRESH_COUNT']) :
			log.debug('if-refresh_count2 : %s',refresh_count2)
			#TODO : If agitation is higher we send silent notification
			# if (db['mvt_count'] > db['agi_normal']) :
			# We increase the normal level
			db['lvl_normal'] = db['lvl_normal'] * (1+(app.config['INCREASE_RATE']/100))
			log.debug('new lvl_normal : %s',db['lvl_normal'])
			refresh_count2 = 0
		else :
			refresh_count2 = refresh_count2 + 1
			log.debug('else-refresh_count2 : %s',refresh_count2)
		
	elif (energy >= db['lvl_normal'] + db['normal_interval'] + db['active_interval']) :
		# Criying state
		log.debug('Criying state')
		# We reset timer counter for agitation
		refresh_count1 = 0
		refresh_count2 = 0
		#TODO : Tigger alarm

def agitation_count() :
	"""Retreive number of mvt per minute and store it on db.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Retreive number of mvt per minute')
	global mvt_counter
	log.debug('mvt_counter : %d',mvt_counter)
	db['mvt_count'] = mvt_counter
	mvt_counter = 0

def mvt_counter(channel) :
	"""Incremente mvt conter on each call from GPIO triggering.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Incremente mvt conter')
	global mvt_counter
	mvt_counter = mvt_counter + 1
	log.debug('mvt_counter : %d',mvt_counter)

def agitation_detect() :
	"""Detect agitation from GPIO and call mvt_counter.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Set GPIO')
	GPIO.setmode(GPIO.BCM)
	# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press
	GPIO.setup(app.config['GPIO_CHANNEL'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.add_event_detect(app.config['GPIO_CHANNEL'], GPIO.RISING, callback=mvt_counter, bouncetime=300)  

def terminate() :
	"""Free resources.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Free resources')
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
	
	log.info('Activity controller task')
	refresh_count1 = 0
	refresh_count2 = 0
	
	# Set the signal handler
	signal.signal(signal.SIGTERM, handler)
	signal.signal(signal.SIGALRM, handler)
	
	# set up audio input
	card = CARD
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
	
	log.info('Agitation controller task')
	with app.app_context():
		signal.setitimer(signal.ITIMER_PROF, 60, 60)
		agitation_detect()

def normal_levels(agi_normal) :
	"""Calibrate the normal level to actual sound level.
	
	@Imput    .
	@Return   .
	"""
	
	log.info('Calibration')
	db['agi_normal'] = agi_normal
	db['lvl_normal'] = sound_level()
	log.debug('agi_normal : %s',agi_normal)
	log.debug("lvl_normal : {:10.4f}".format(db['lvl_normal']))

