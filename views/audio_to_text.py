import os

from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import speech

from views.utils import get_name_of_file


class SpeechToText:
    def __init__(self):
        self.credential_path = os.environ.get('CREDENTIAL_PATH')
        self.bucket_name = os.environ.get('BUCKET_NAME')
        self.gcs_uri = os.environ.get('GCS_URI')
        self.credentials = service_account.Credentials.from_service_account_file(self.credential_path)

    def upload_file_gcs(self, file, folder):
        client = storage.Client(credentials=self.credentials, project='My First Project')
        bucket = client.get_bucket(self.bucket_name)
        blob = bucket.blob(file)
        if not blob.exists():
            blob.upload_from_filename(os.path.join(folder, file))
            print(file)
        else:
            print("File already exists")

    def transcribe_gcs_with_word_time_offsets(self, filename, output_folder):
        client = speech.SpeechClient(credentials=self.credentials)

        audio = speech.RecognitionAudio(uri=self.gcs_uri+filename)
        config = speech.RecognitionConfig(
            encoding="LINEAR16",
            sample_rate_hertz=44100,
            audio_channel_count=2,
            language_code="en-US",
        )

        operation = client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        result = operation.result(timeout=300)
        text = ''
        for result in result.results:
            alternative = result.alternatives[0]
            print("Transcript: {}".format(alternative.transcript))
            text = text + alternative.transcript
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        with open(os.path.join(output_folder, get_name_of_file(filename) + ".txt"),
                  "a") as text_file:
            text_file.write(text)

    def get_text(self, folder, output_folder):
        if not os.path.exists(folder):
            return "Folder not exist"

        if not os.path.exists(output_folder):
            return "Output folder not exist"

        for file in os.listdir(folder):
            self.upload_file_gcs(file, folder)
            self.transcribe_gcs_with_word_time_offsets(file, output_folder)
