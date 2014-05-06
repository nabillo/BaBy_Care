'''
Created on Mar 04, 2014

@author: nabillo
'''

import os
from werkzeug import secure_filename
from BaBy_Care import app, log
import subprocess

def allowed_file(filename) :
	"""For a given file, return whether it's an allowed type or not."""
	
	return '.' in filename and \
				 filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def media_upload(files) :
	"""Save file to SD card."""
	
	log.info('Upload file')
	result = 0
	for file in files:
		# Check if the file is one of the allowed types/extensions
		if file and allowed_file(file.filename):
			# Make the filename safe, remove unsupported chars
			filename = secure_filename(file.filename)
			# Move the file form the temporal folder to the upload
			# folder we setup
			try :
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				log.debug('file saved : %s',filename)
				result = result + 1
			except UploadNotAllowed:
				log.error('file too large : %s',filename)
		else:
			log.warning('file not allowed : %s',filename)
	
	# Reload all song on playlist
	subprocess.call('mpc clear; mpc add %s; mpc update',app.config['UPLOAD_FOLDER'])
	
	log.debug('result : %s',result)
	return result
	
def media_del(files) :
	"""Delete file from SD card and reload playlist."""
	
	log.info('Delete file')
	result = 0
	for file in files:
		try :
			#delete file from directory
			subprocess.call('rm -f %s/%s',app.config['UPLOAD_FOLDER'],file)
			
			log.debug('file deleted : %s',file)
			result = result + 1
		except subprocess.CalledProcessError :
			# file not deleted
			log.error('file not deleted')
			log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
	
	# Reload all song on playlist
	subprocess.call('mpc clear; mpc add %s; mpc update',app.config['UPLOAD_FOLDER'])
	
	log.debug('result : %s',result)
	return result
	
def media_list() :
	"""List song files."""
	
	log.info('List songs')
	try :
		#TODO : list command
		titles = subprocess.check_output(["ls", "-tr"], shell=True)
		
		log.debug('Playlist titles : %s',titles)
		titles = titles.splitlines()
		result = titles
	except subprocess.CalledProcessError :
		# file not deleted
		log.error('list error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	
	log.debug('result : %s',result)
	return result
	
def media_Play() :
	"""Play playlist songs."""
	
	log.info('Play songs')
	try :
		subprocess.call('mpc play ')
	
		log.debug('Play')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.error('Play error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
		
	log.debug('result : %s',result)
	return result
	
def media_Stop() :
	"""Stop playlist songs."""
	
	log.info('Stop songs')
	try :
		subprocess.call('mpc stop ')
	
		log.debug('stop')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.error('stop error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
		
	log.debug('result : %s',result)
	return result
	
def media_VolUp() :
	"""Volume Up."""
	
	log.info('Volume Up')
	try :
		subprocess.call('mpc volume + ')
	
		log.debug('Volume increased')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.error('Volume increase error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
		
	log.debug('result : %s',result)
	return result
	
def media_VolDown() :
	"""Volume down."""
	
	log.info('Volume Down')
	try :
		subprocess.call('mpc volume - ')
	
		log.debug('Volume decreased')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.error('Volume decrease error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
		
	log.debug('result : %s',result)
	return result
	
