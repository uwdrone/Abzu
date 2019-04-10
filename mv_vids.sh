scp pi@192.168.1.102:/home/pi/Desktop/VideoRecordings/video* /home/brady/Videos/AbzuCam/
status=$?
if [[ $status -eq 0 ]]
then
	ssh pi@192.168.1.102 'rm /home/pi/Desktop/VideoRecordings/video*'
fi
#ssh pi@192.168.1.102 'sudo shutdown now'
