import os
import cv2

from views.utils import get_name_of_file


def convert(file, folder, output_folder):
    frame_rate = 0.5
    cap = cv2.VideoCapture(os.path.join(folder, file))
    success = True
    count = 0
    sec = 0
    file_folder = os.path.join(output_folder, get_name_of_file(file))
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    while success:
        sec += frame_rate
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)
        success, image = cap.read()
        count += 1
        filename = os.path.join(file_folder, str(count)+'.jpg')
        print(filename)
        if success:
            cv2.imwrite(filename, image)


def get_frames(folder, output_folder):
    if not os.path.exists(output_folder):
        return "Output folder doesn't exist"

    if not os.path.exists(folder):
        return "Input folder doesn't exist"

    for file in os.listdir(folder):
        convert(file, folder, output_folder)
