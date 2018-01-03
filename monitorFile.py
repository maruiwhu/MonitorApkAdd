from watchdog.observers import Observer
from watchdog.events import *
import time
import subprocess
import os

lastModifyFile=""
DIRECTORY_NAME = "Z:/马瑞"
APP_START_CMD = "adb shell am start -n cn.nubia.neostore/cn.nubia.neostore.ui.start.AppStartActivity"

class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_moved(self, event):
        if event.is_directory:
            print("directory moved from {0} to {1}".format(event.src_path,event.dest_path))
        else:
            print("file moved from {0} to {1}".format(event.src_path,event.dest_path))

    def on_created(self, event):
        if event.is_directory:
            print("directory created:{0}".format(event.src_path))
        else:
            print("file created:{0}".format(event.src_path))

    def on_deleted(self, event):
        if event.is_directory:
            print("directory deleted:{0}".format(event.src_path))
        else:
            print("file deleted:{0}".format(event.src_path))

    def on_modified(self, event):
        if event.is_directory:
            print("directory modified:{0}".format(event.src_path))
        else:
            print("file modified:{0}".format(event.src_path))
            file_name = "{0}".format(event.src_path)
            if (file_name.endswith(".apk")):
                global lastModifyFile
                if lastModifyFile != file_name:
                    lastModifyFile = file_name
                    os.system("adb install -r -d \"{0}\"".format(event.src_path))
                    os.system(APP_START_CMD)
                    

if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    observer.schedule(event_handler,DIRECTORY_NAME,True)
    observer.start()
    print('Ctrl-C exit!')
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
