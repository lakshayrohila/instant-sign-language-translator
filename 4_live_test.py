import cv2 as cv
import pickle
import math
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)


MODEL_FNAME = r"./build/model.pickle"
model_file = open(MODEL_FNAME, 'rb')
model_dict = pickle.load(model_file)
model_file.close()
model = model_dict['model']


capture = cv.VideoCapture(0) # 0 means default webcam
fps = capture.get(cv.CAP_PROP_FPS)
if fps == 0:
    print("Failed to open camera. Quitting...")
    quit()
latency_ms = math.floor(1000/fps)


def match_input(input, comparision):
    return (input&0xFF) == ord(comparision.lower())


while True:
    is_capture_successful, frame = capture.read()
    if not is_capture_successful: break

    crr_hands_data = []

    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    min_x = min_y = 1 # for normalizing of landmark points later
    max_x = max_y = 0

    hands_result = hands.process(frame_rgb)
    if hands_result.multi_hand_landmarks:
        for crr_hand_landmarks in hands_result.multi_hand_landmarks:
            for crr_landmark in crr_hand_landmarks.landmark:
                x = crr_landmark.x
                y = crr_landmark.y
                crr_hands_data.extend([x, y])

                if min_x > x: min_x = x
                if min_y > y: min_y = y
                if max_x < x: max_x = x
                if max_y < y: max_y = y

    if len(crr_hands_data) == 42:
        # normalize all the landmarks so that they range from 0 to 1 exactly
        for i in range(len(crr_hands_data)):
            if i%2: # indeces 1,3,5,... for y
                crr_hands_data[i] = (crr_hands_data[i]-min_y)/(max_y-min_y)
            else:
                crr_hands_data[i] = (crr_hands_data[i]-min_x)/(max_x-min_x)

        model_prediction = model.predict([crr_hands_data])[0]
        m_predict_as_char = chr(model_prediction)

        (text_w, text_h), _ = cv.getTextSize(m_predict_as_char, cv.FONT_HERSHEY_COMPLEX, 2, 2)
        cv.rectangle(frame, (45,80), (55+text_w,70-text_h), (0,0,0), -1)
        cv.putText(frame, m_predict_as_char, (50,75),
                   cv.FONT_HERSHEY_COMPLEX, 2, (255,255,255), 2, cv.LINE_AA)

    cv.imshow('Instant Sign Language Translator', frame)

    input = cv.waitKey(1)
    if match_input(input, 'q'): # end with key 'q'
        break

capture.release()
cv.destroyAllWindows()
