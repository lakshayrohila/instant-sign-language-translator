import cv2 as cv
import mediapipe as mp
import os
import shutil
import pickle
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)

PICS_DIR = r"./build/pics_dir/" # the directory in which our pictures are located
if not os.path.exists:
    print("Cannot find PICS_DIR:", PICS_DIR)
    quit()
os.chdir(PICS_DIR)

data = [] # contains list of images - an image is a list of coordinates of all hand landmarks in that image
labels = [] # contains the ord() of the label ('a', 'b', ...) corresponding directly to the image on
            # same index in data[]

# for every image in every directory, get all the hand landmarks' (x,y), and store it into data[]
# since we are using RandomForest ai model, (x,y) are stored continously like [x1,y1,x2,y2,x3,y3...] for each image
# data[] is the list of all these lists of images
dirs_done = 1 # for reporting the process progress
total_dirs = len(os.listdir("./"))

for crr_dir in os.listdir("./"): # we are currently chdir'ed into the DATA_DIR
    os.chdir(crr_dir)
    print("\n*** Moved into directory", crr_dir)
    print("*** Directory Index:", dirs_done, "/", total_dirs)

    imgs_done = 1 # for reporting the progress
    total_imgs = len(os.listdir("./"))
    num_imgs_useful = 0

    for crr_img in os.listdir("./"): # i.e. all images in current label
        print("\rProcessing Image:", imgs_done, "/", total_imgs, "@", int(imgs_done/total_imgs*100), "%", end="", flush=True)
        imgs_done += 1

        crr_img_data = []

        img_mat_obj = cv.imread(crr_img)
        img_mat_obj_rgb = cv.cvtColor(img_mat_obj, cv.COLOR_BGR2RGB) # since mediapipe processes rgb only

        min_x = min_y = 1 # for normalizing of landmark points later
        max_x = max_y = 0

        hands_results = hands.process(img_mat_obj_rgb)
        if hands_results.multi_hand_landmarks:
            for crr_hand_landmarks in hands_results.multi_hand_landmarks:
                for crr_landmark in crr_hand_landmarks.landmark:
                    x = crr_landmark.x
                    y = crr_landmark.y
                    crr_img_data.extend([x, y])

                    if min_x > x: min_x = x
                    if min_y > y: min_y = y
                    if max_x < x: max_x = x
                    if max_y < y: max_y = y

        if len(crr_img_data) != 42: continue # this image does not has all landmarks, so leave it
        num_imgs_useful += 1

        # normalize all the landmarks so that they range from 0 to 1 exactly
        for i in range(len(crr_img_data)):
            if i%2: # indeces 1,3,5,... for y
                crr_img_data[i] = (crr_img_data[i]-min_y)/(max_y-min_y)
            else:
                crr_img_data[i] = (crr_img_data[i]-min_x)/(max_x-min_x)

        data.append(crr_img_data)
        labels.append(ord(crr_dir))

    print("\nDirectory", crr_dir, ":", num_imgs_useful, "images useful out of", total_imgs, "@", int(num_imgs_useful/total_imgs*100), "%")

    dirs_done += 1
    os.chdir("../") # since we had earlier switched to crr_dir
os.chdir("../") # since we had earlier switched to PICS_DIR


DATA_FNAME = r"./data.pickle" # the file in which our processed data will be stored
DATA_FNAME_BAK = r"./data_bak.pickle" # create a backup of previous data file if it exists
if os.path.exists(DATA_FNAME): shutil.move(DATA_FNAME, DATA_FNAME_BAK)

data_file = open(DATA_FNAME, 'wb')
pickle.dump({'data': np.asarray(data), 'labels': np.asarray(labels)}, data_file)
data_file.close()

os.chdir("../") # we were currently in build/
