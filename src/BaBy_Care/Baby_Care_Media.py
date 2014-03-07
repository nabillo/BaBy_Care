'''
Created on Mar 04, 2014

@author: nabillo
'''

import os
from werkzeug import secure_filename

def allowed_file(filename) :
	"""For a given file, return whether it's an allowed type or not."""
	
	return '.' in filename and \
				 filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def media_upload() :
	"""Save file to SD card."""
	
	log.debug('upload file')
	uploaded_files = request.files.getlist("file[]")
	result = 0
	for file in uploaded_files:
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
				log.debug('file too large : %s',filename)
		else:
			log.debug('file not allowed : %s',filename)
	return result
	
def media_del(num) :
	"""Delete file from playlist and SD card."""
	
	log.debug('delete file')
	try :
		subprocess.call('mpc del %s',num)
		
		log.info('file deleted')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('file not deleted')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def media_list() :
	"""Delete file from playlist and SD card."""
	
	log.debug('list songs')
	try :
		titles = subprocess.check_output('mpc playlist -f " [%position%) %title%]"')
		
		log.info('Playlist titles : %s',titles)
		titles = titles.splitlines()
		result = titles
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('file not deleted')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def media_Play() :
	"""Play playlist songs."""
	
	log.debug('Play songs')
	try :
		subprocess.call('mpc play ')
	
		log.info('Play')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('Play error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def media_Stop() :
	"""Stop playlist songs."""
	
	log.debug('Stop songs')
	try :
		subprocess.call('mpc stop ')
	
		log.info('stop')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('stop error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def media_VolUp() :
	"""Volume Up."""
	
	log.debug('Volume Up')
	try :
		subprocess.call('mpc volume + ')
	
		log.info('Volume increased')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('Volume increase error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
def media_VolDown() :
	"""Volume down."""
	
	log.debug('Volume Down')
	try :
		subprocess.call('mpc volume - ')
	
		log.info('Volume decreased')
		result = 'Success'
	except subprocess.CalledProcessError :
		# file not deleted
		log.warning('Volume decrease error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'
	return result
	
