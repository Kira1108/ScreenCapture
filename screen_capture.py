import tkinter
from PIL import ImageGrab
from datetime import datetime
import os
import uuid
import time
import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import shutil
from config import config

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

IMAGE_FOLDER_PATH = config['image_filepath']

if not os.path.exists(IMAGE_FOLDER_PATH):
    os.makedirs(IMAGE_FOLDER_PATH)

def shot():
    """Take a screen shot and return a PIL IMAGE object"""
    win = tkinter.Tk()
    img = ImageGrab.grab()
    img = img.convert("RGB")
    return img

def save(img, path):
    """Save Image to Path"""
    img.save(path)

def getName():
    """Get a filename uniquely identified by device and current time"""
    ctime = datetime.now().strftime('%Y%m%d%HH%MM%SS')
    device = hex(uuid.getnode())
    return f"{device}_{ctime}.jpg"

def getPath(root = IMAGE_FOLDER_PATH, name = None):
    "Get a Path based on a root folder and a filename"
    root = root if root else IMAGE_FOLDER_PATH
    name = name if name else getName()
    return os.path.join(root,name)

def takeScreenShot(folder = None, filename = None):
    "Take a scrrent shot and save to folder/filename"
    imgPath =getPath(folder, filename)
    save(shot(), imgPath)

def infiniteSc(seconds = 10):
    "Take screen shots every `seconds` seconds"
    while True:
        logger.info(f"Screen Shot at {datetime.now()}")
        takeScreenShot()
        time.sleep(seconds)

def removeFiles(path = IMAGE_FOLDER_PATH):
    "Remove all contents in path folder"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def scheduleSc(screen_capture_seconds = 2, rotate_seconds = 10):
    "Add a job scheduler."
    scheduler = BlockingScheduler()
    scheduler.add_job(takeScreenShot, 'interval', seconds=screen_capture_seconds, id='Screenshot')
    scheduler.add_job(removeFiles,'interval', seconds = rotate_seconds, id = 'CleanupFiles')
    scheduler.start()

if __name__ == "__main__":
    scheduleSc(rotate_seconds = 10)

