import cv2 as cv
import math
import os
import shutil
import numpy as np
import time


PICS_DIR = r"./build/pics_dir/" # the directory in which our pictures will be located
PICS_DIR_BAK = r"./build/pics_dir_bak/" # create a backup of previous DATA_DIR if it exists
if os.path.exists(PICS_DIR):
    if os.path.exists(PICS_DIR_BAK):
        shutil.rmtree(PICS_DIR_BAK)
    shutil.move(PICS_DIR, PICS_DIR_BAK)
os.makedirs(PICS_DIR)
os.chdir(PICS_DIR)


def match_input(input, comparision):
    return (input&0xFF) == ord(comparision.lower())

press_key_win_name = "Press key to continue"
press_key_win = np.zeros((200,400,3), dtype=np.uint8) # window showing "press key to continue"
cv.putText(press_key_win, "Press Q key to reshoot the previous letter", (0,75), cv.FONT_HERSHEY_PLAIN, 1, (255,255,255))
cv.putText(press_key_win, "Press any other key to continue", (0,125), cv.FONT_HERSHEY_PLAIN, 1, (255,255,255))

crr_char = 'Q'
while crr_char <= 'Q':
    # to allow the user to prepare, wait for him to press any key before continuing
    cv.imshow(press_key_win_name, press_key_win)
    input_key = cv.waitKey(0)
    cv.destroyWindow(press_key_win_name)
    if match_input(input_key, 'Q') and crr_char != 'A': # the user wants to reshoot the previous key
        crr_char = chr(ord(crr_char) - 1) # C-style: crr_char--
        shutil.rmtree("./" + crr_char + "/")

    # setup the directory to put the files for current char in
    crr_dir_name = "./" + crr_char + "/"
    os.makedirs(crr_dir_name)
    os.chdir(crr_dir_name)

    # now start capturing the pics
    vid_capture = cv.VideoCapture(0) # get webcam
    vid_capture_fps = vid_capture.get(cv.CAP_PROP_FPS)
    vid_capture_latency_ms = math.floor(1000/vid_capture_fps) # give this delay to time.sleep

    for crr_pic_num in range(400, 500):
        is_capture_successful, frame = vid_capture.read()
        if not is_capture_successful: # video capture failed, but should not - throw error and exit
            print("Video capture failed!!")
            vid_capture.release()
            cv.destroyAllWindows()
            quit()

        # show the picture to the user
        cv.imshow("Capturing letter " + crr_char, frame)
        cv.waitKey(1) # to refresh the cv.imshow window

        # also save to picture
        crr_pic_name = "./" + str(crr_pic_num) + ".jpg"
        cv.imwrite(crr_pic_name, frame)

        time.sleep(vid_capture_latency_ms/1000)
    cv.destroyWindow("Capturing letter " + crr_char)
    vid_capture.release()

    # finally go back to upper directory since we earlier chdir'ed to one inside it
    os.chdir("../")

    # also increment the crr_char
    crr_char = chr(ord(crr_char) + 1) # C-style: crr_char++

cv.destroyAllWindows()

# go back to one dir up since we earlier chdir'ed to one inside it
os.chdir("../")
