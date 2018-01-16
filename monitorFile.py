# -*- coding: utf-8 -*-
from watchdog.observers import Observer
from watchdog.events import *

import os
import re
import sys
import zipfile
import datetime
from subprocess import Popen, PIPE
from os.path import dirname, realpath, join
import time
import subprocess

lastModifyFile=""
APP_START_CMD = "adb shell am start -n  {0}/{1}"

# tools path
AAPT_PATH = join(os.environ["ANDROID_HOME"],'build-tools','25.0.2', 'aapt.exe')
# package name
CMD_PACKAGE_INFO = AAPT_PATH + ' dump badging "%s" | findstr package:'
PACKAGE_INFO_REGEX = re.compile(r"package: name='(.*)' versionCode='(.*)' versionName='(.*)'", re.I)

# launchable-activity name 
CMD_APP_INFO = AAPT_PATH + ' dump badging "%s" | findstr launchable-activity'
LAUNCHABLE_ACTIVITY_REGEX = re.compile("launchable-activity: name='(.*)'  label=", re.I)


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
                    apk_infos=extract_apk_info(file_name)
                    cmd_start = APP_START_CMD.format(apk_infos['package_name'],apk_infos['launchable-activity'])
                    print(cmd_start)
                    os.system(cmd_start)
                    

def extract_apk_info(file_path):
    print (AAPT_PATH)
    apk_infos={}
    try:
        info = Popen(CMD_PACKAGE_INFO % file_path, stdout=PIPE,stdin=PIPE, shell=True).communicate()[0]
        m = PACKAGE_INFO_REGEX.match(info.decode('utf-8').replace('\n', ''))
        if m:
            apk_infos['package_name'] = m.group(1)
            apk_infos['version_code'] = int(m.group(2) or 0)
    except Exception as e:
        print('get package info failed %s',e)
    # get launchable-activity name
    try:
         info = Popen(CMD_APP_INFO % file_path, stdin=PIPE,stdout=PIPE, shell=True).communicate()[0]
         print(info)
         infos=info.decode('utf-8').split('\\r\\n')
         m = LAUNCHABLE_ACTIVITY_REGEX.match(infos[0])
         if m:
             apk_infos['launchable-activity'] = m.group(1)
    except Exception as e :
        print('get launchable-activity failed %s ',e)
    return apk_infos
    
                    
if __name__ == "__main__":
    observer = Observer()
    event_handler = FileEventHandler()
    if not len(sys.argv):
        print('USAGE: python monofy FILE PATH ')
    else:
        DIRECTORY_NAME = sys.argv[-1]
        observer.schedule(event_handler,DIRECTORY_NAME,True)
        observer.start()
        print('Ctrl-C exit!')
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
