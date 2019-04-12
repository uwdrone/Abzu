AUTOBOOT=0
if [[ ${AUTOBOOT} -eq 1 ]] then
	python3 /home/pi/Abzu/launcherProgram.py
	wait
	sudo shutdown now
fi
