'''
Created on Feb 19, 2014

@author: nabillo
'''

def steam_ctr_exe(command):
  # Command sentence
  #gst_pid = 'ps -aef | grep "gst\-launch" | grep -v grep | awk "{print $2}"'

  #gst_kill = 'killall gst-launch-1.0'
  #gst_launch = 'gst-launch-1.0 v4l2src  ! \"video/x-raw,width=640,height=480,framerate=15/1\" ! \
  #            omxh264enc target-bitrate=1000000 control-rate=variable ! \
  #            video/x-h264,profile=high ! h264parse ! queue ! \
  #            flvmux name=mux alsasrc device=hw:1 ! audioresample ! audio/x-raw,rate=48000 ! \
  #            queue ! voaacenc bitrate=32000 ! queue ! mux. mux. ! \
  #            rtmpsink location=\"rtmp://example.com/myapp/mystream live=1\"' 

  #pid = subprocess.check_output(gst_pid, shell=True)
  #log.info('pid %s', pid)
  
  log.info('command %s', command)
  if (command == 'Start') :
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

  elif (command == 'Stop') :
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

  elif (command == 'Restart') :
    log.info('Restart Gstreamer')
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

  else:
    log.info('invalid command')
    result = 'None'

  return result