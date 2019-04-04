from threading import Thread
import time

class VideoRecorder(Thread):
    def __init__(self, inputMonitor):
        Thread.__init__(self)
        self.inputMap = inputMonitor["inputMap"]
        self.readLock = inputMonitor["readLock"]
        self.writeLock = inputMonitor["writeLock"]
        self.inputMonitor = inputMonitor
        self.triangle = None
        self.recording = False

    def run(self):
        self.recordVideo()
    
    def recordVideo(self):
        while True:
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
                #do things
                pass
