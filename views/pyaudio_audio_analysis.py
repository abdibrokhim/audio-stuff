import os
import librosa
from pyAudioAnalysis import audioTrainTest as aT
import pandas as pd
from dotenv import load_dotenv

from views.utils import get_name_of_file

load_dotenv()

skipped_files = []


class PyAudio:
    def __init__(self):
        self.model = os.environ.get('MODEL')

    def analyse(self, file, folder):
        filename = os.path.join(folder, file)
        result = aT.file_regression(filename, self.model, 'svm')
        duration = librosa.get_duration(filename=filename)
        arousal = result[0][0]
        valence = result[0][1]
        return get_name_of_file(file), arousal, valence, duration

    def get_audio_analysis(self, folder, output_folder):

        if not os.path.exists(output_folder):
            return "Output folder doesn't exist"

        if not os.path.exists(folder):
            return "Input folder doesn't exist"

        columns = ["audio_name", "arousal", "valence", "duration"]
        data = []
        for file in os.listdir(folder):
            if file.split(".")[-1] not in ["wav", "mp3"]:
                continue
            try:
                data.append(self.analyse(file, folder))
            except Exception as ex:
                print(ex)
                skipped_files.append(file)
        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv(os.path.join(output_folder, 'pyaudio.csv'))
        print(skipped_files)
        return "Success"
