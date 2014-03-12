#! /bin/sh

### BEGIN INIT INFO
# Short-Description: Script to manage Streamer for BaBy Care
# Description:       Script to manage Streamer for Baby Care by using the Gstreamer.
### END INIT INFO

gst_command = "gst-launch-1.0 v4l2src  ! \"video/x-raw,width=640,height=480,framerate=15/1\" ! \
				omxh264enc target-bitrate=1000000 control-rate=variable ! \
				video/x-h264,profile=high ! h264parse ! queue ! \
				flvmux name=mux alsasrc device=hw:1 ! audioresample ! audio/x-raw,rate=48000 ! \
				queue ! voaacenc bitrate=32000 ! queue ! mux. mux. ! \
				rtmpsink location=\"rtmp://example.com/myapp/mystream live=1\"" 

case "$1" in
	Start)
		echo -n "Starting Streamer: gst-launch"
		# Run Gstreamer
		$gst_command
		if [ $? -ne 0 ] then
			echo -n "Error starting Streamer: gst-launch"
			exit 1
		fi
		echo -n "."
		;;
	Stop)
		echo -n "Stoping Streamer: gst-launch"
		# kill Gstreamer
		killall gst-launch-1.0
		if [ $? -ne 0 ] then
			echo -n "Error stoping Streamer: gst-launch"
			exit 2
		fi
		echo -n "."
		;;
	Restart)
		echo -n "Restarting Streamer: gst-launch"
		killall -s SIGTERM gst-launch-1.0
		if [ $? -ne 0 ] then
			echo -n "Error stoping Streamer: gst-launch"
			exit 2
		fi
		$gst_command
		if [ $? -ne 0 ] then
			echo -n "Error starting Streamer: gst-launch"
			exit 1
		fi
		echo -n "."
		;;
esac

exit 0
