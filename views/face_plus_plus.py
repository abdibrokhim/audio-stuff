import os
import pandas as pd
from PythonSDK.facepp import API, File

api = API()


class FacePlus:
    def __init__(self):
        self.frame = []
        self.person = []
        self.gender = []
        self.age = []
        self.smile = []
        self.anger = []
        self.disgust = []
        self.fear = []
        self.happiness = []
        self.neutral = []
        self.sadness = []
        self.surprise = []
        self.male_score = []
        self.female_score = []
        self.return_attributes = "gender,age,smiling,headpose,facequality,blur,emotion,ethnicity,beauty"

    def analyse(self, res, image):
        if res['faces']:
            for i in range(0, len(res['faces'])):
                face = res['faces'][i]
                if 'attributes' in face.keys():
                    self.frame.append(image)
                    self.person.append('person_' + str(i + 1))
                    attributes = (face['attributes'])
                    self.gender.append(attributes['gender']['value'])
                    self.age.append(attributes['age']['value'])
                    self.smile.append(attributes['smile']['value'])
                    emotion = attributes['emotion']
                    self.anger.append(emotion['anger'])
                    self.disgust.append(emotion['disgust'])
                    self.fear.append(emotion['fear'])
                    self.happiness.append(emotion['happiness'])
                    self.neutral.append(emotion['neutral'])
                    self.sadness.append(emotion['sadness'])
                    self.surprise.append(emotion['surprise'])
                    beauty = attributes['beauty']
                    self.male_score.append(beauty['male_score'])
                    self.female_score.append(beauty['female_score'])

    def repeat(self, image_path, file, output_folder):
        for image in os.listdir(image_path):
            if image == '.DS_Store':
                continue

            res = api.detect(image_file=File(os.path.join(image_path, image)), return_attributes=self.return_attributes)
            self.analyse(res, image)
        values = {'frame': self.frame, 'person': self.person, 'gender': self.gender, 'age': self.age, 'smile': self.smile, 'anger': self.anger,
                  'disgust': self.disgust, 'fear': self.fear, 'happiness': self.happiness, 'neutral': self.neutral,
                  'sadness': self.sadness, 'surprise': self.surprise, 'male_score': self.male_score, 'female_score': self.female_score}
        df = pd.DataFrame(values)
        df.to_csv(os.path.join(output_folder, 'face_' + file + '.csv'))


def get_face_analysis(folder, output_folder):
    if not os.path.exists(folder):
        return "Folder not exist"

    if not os.path.exists(output_folder):
        return "Output folder not exist"

    for image_folder in os.listdir(folder):
        if image_folder == '.DS_Store':
            continue
        face = FacePlus()
        face.repeat(os.path.join(folder, image_folder), image_folder, output_folder)
