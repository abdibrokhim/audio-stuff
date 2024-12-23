import glob
import os
import time
from collections import defaultdict
import pandas as pd
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


class AzureFace:
    def __init__(self, input_folder, output_folder):
        self.KEY = "b39eaba5e98048669e0f67cb18380dca"
        self.ENDPOINT = "https://behzod-hoshimov.cognitiveservices.azure.com/"
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.face_client = FaceClient(self.ENDPOINT, CognitiveServicesCredentials(self.KEY))
        self.check_folder()

    def analyse(self):
        for folder in os.listdir(self.input_folder):
            if folder == '.DS_Store':
                continue
            if os.path.exists(os.path.join(os.path.join(self.output_folder, folder) + ".csv")):
                continue

            keys = ("anger", "contempt", "disgust", "fear", "happiness", "neutral", "sadness", "surprise")
            data = defaultdict(list)
            image_folder = os.path.join(self.input_folder, folder)
            for file in os.listdir(image_folder):
                if file.split(".")[-1] not in ["jpg", "jpeg"]:
                    continue
                image_path = os.path.join(image_folder, file)
                print(image_path)
                image_arr = glob.glob(image_path)
                image = open(image_arr[0], 'r+b')

                faces = self.face_client.face.detect_with_stream(image,
                                                                 detection_model="detection_01",
                                                                 recognition_model="recognition_04",
                                                                 return_face_attributes=["emotion", ])
                data["filename"].append(file)
                if len(faces) > 0:
                    emotions = faces[0].face_attributes.emotion
                    for key in keys:
                        data[key].append(emotions.__getattribute__(key))
                else:
                    for key in keys:
                        data[key].append(0)

                time.sleep(3)
            df = pd.DataFrame(data=data)
            df.to_csv(os.path.join(self.output_folder, folder) + ".csv")
        return "Success"

    def check_folder(self):
        if not os.path.exists(self.input_folder):
            raise "Input folder doesn't exist"

        if not os.path.exists(self.output_folder):
            raise "Output folder doesn't exist"
