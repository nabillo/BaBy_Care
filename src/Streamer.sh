#! /bin/bash -x

### BEGIN INIT INFO
# Short-Description: Script to manage Streamer for BaBy Care
# Description:       Script to manage Streamer for Baby Care by using the Gstreamer.
### END INIT INFO

gst_command="gst-launch-1.0 -v v4l2src ! 'video/x-raw, width=640, height=480, framerate=15/1' ! queue ! videoconvert ! omxh264enc ! rtph264pay pt=96 ! udpsink host=192.168.137.10 port=9078 &" 

case "$1" in
	Start)
		echo "Starting Streamer: gst-launch"
		# Run Gstreamer
		eval $gst_command
		if [ $? -ne 0 ] 
		then
			echo "Error starting Streamer: gst-launch"
			exit 1
		fi
		echo "."
		;;
	Stop)
		echo "Stoping Streamer: gst-launch"
		# kill Gstreamer
		killall gst-launch-1.0
		if [ $? -ne 0 ] 
		then
			echo "Error stoping Streamer: gst-launch"
			exit 2
		fi
		echo "."
		;;
	Restart)
		echo "Restarting Streamer: gst-launch"
		killall -s SIGTERM gst-launch-1.0
		if [ $? -ne 0 ] 
		then
			echo "Error stoping Streamer: gst-launch"
			exit 2
		fi
		eval $gst_command
		if [ $? -ne 0 ] 
		then
			echo "Error starting Streamer: gst-launch"
			exit 1
		fi
		echo "."
		;;
esac

exit 0
