import os
import moviepy as mp

from views.utils import get_name_of_file


def convert(folder, output_folder):
    if not os.path.exists(output_folder):
        return "Output Folder not exist"

    if not os.path.exists(folder):
        return "Input folder not exist"

    for file in os.listdir(folder):
        if file == '.DS_Store':
            continue
        output_file = os.path.join(output_folder, get_name_of_file(file) + ".wav")
        if not os.path.exists(output_file):
            convert_file(file, folder, output_folder)


def convert_file(file, folder, output_folder):
    with mp.VideoFileClip(os.path.join(folder, file)) as clip:

        clip.audio.write_audiofile(os.path.join(output_folder, file + '.wav'))
