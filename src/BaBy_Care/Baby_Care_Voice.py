'''
Created on May 06, 2014

@author: nabillo
'''

def voice_ctr_start(host_url) :
	"""Start voice chat listner.
	
	@Imput    host_url : url of the chat client.
	@Return   .
	"""

	log.info('Start Voice Chat')
	
	try :
		
		subprocess.call(["mpc", "clear"])
		subprocess.call(["mpc", "add", host_url])
		subprocess.call(["mpc", "update"])
		subprocess.call(["mpc", "play"])
		
		log.debug('Chat')
		result = 'Success'
	except subprocess.CalledProcessError :
		log.error('Chat error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'

	log.debug('result : %s',result)
	return result
	
def voice_ctr_stop() :
	"""Stop voice chat listner.
	
	@Imput    .
	@Return   .
	"""

	log.info('Stop Voice Chat')
	
	try :
		
		subprocess.call(["mpc", "stop"])
		subprocess.call(["mpc", "clear"])
		subprocess.call(["mpc", "add", app.config['UPLOAD_FOLDER']])
		subprocess.call(["mpc", "update"])

		log.debug('Chat')
		result = 'Success'
	except subprocess.CalledProcessError :
		log.error('Chat error')
		log.warning('Return code : %s',subprocess.CalledProcessError.returncode)
		result = 'Error'

	log.debug('result : %s',result)
	return result
	
