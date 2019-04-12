from threading import Thread
from picamera import PiCamera
import time

class VideoRecorder(Thread):
    '''
        This thread waits for user command to toggle recording. Video is recorded
        from a 'splitter port' which splits the picamera stream onto a second port.
        The video is saved to a .h264 file. Each video is saved to a new file by 
        incrementing the vid count. Vid count is stored in a file, and updated.
    '''
    def __init__(self, inputMonitor, camera):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor
        self.event = inputMonitor["event"]
        self.triangle = 0
        self.prevTriangle = 0
        self.recording = False
        self.camera = camera
        self.vid_count_file = "/home/pi/Desktop/VideoRecordings/vid_count.txt"

        f = open(self.vid_count_file, "r")
        self.vid_count = int(f.readline())
        f.close()        
        
        

    def run(self):
        self.recordVideo()

    def recordVideo(self):
        while not self.event.is_set():
            self.readLock.acquire(blocking=True, timeout=-1)
            self.inputMonitor["pendingReaders"] += 1
            self.readLock.wait()

            self.inputMonitor["pendingReaders"] -= 1
            self.inputMonitor["readers"] += 1

            self.triangle = self.inputMap["triangle"]

            self.inputMonitor["readers"] -= 1
            if self.inputMonitor["pendingWriters"] > 0:
                self.writeLock.notify_all()
            elif self.inputMonitor["pendingReaders"]>0 or self.inputMonitor["readers"]>0:
                self.readLock.notify_all()
            else:
                pass
            self.readLock.release()

            if self.triangle == 1:
                if self.recording == True and self.prevTriangle != 1:
                    self.recording = False
                    self.camera.stop_recording(splitter_port=2)
                elif self.recording == False and self.prevTriangle != 1:
                    self.recording = True
                    self.camera.start_recording('/home/pi/Desktop/VideoRecordings/video' + str(self.vid_count) + '.h264',splitter_port=2)
                    self.vid_count += 1
                    f = open(self.vid_count_file, "w")
                    f.write(str(self.vid_count))
                    f.close()
            
            self.prevTriangle = self.triangle
        exit()
