import os
import pandas as pd

from google.cloud import language_v1
from google.oauth2 import service_account

from views.utils import get_name_of_file

skipped_files = []


class SentimentAnalysis:

    def __init__(self):
        self.credential_path = os.environ.get('CREDENTIAL_PATH')
        print(self.credential_path)
        self.credentials = service_account.Credentials.from_service_account_file(self.credential_path)

    def analyse(self, file, folder):
        client = language_v1.LanguageServiceClient(credentials=self.credentials)
        with open(os.path.join(folder, file), 'r') as text_file:
            type_ = language_v1.Document.Type.PLAIN_TEXT
            encoding_type = language_v1.EncodingType.UTF8
            document = {'content': text_file.read(), 'type_': type_}
            sentiment = client.analyze_sentiment(
                request={'document': document, 'encoding_type': encoding_type}).document_sentiment
            print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
            return [get_name_of_file(file), sentiment.score, sentiment.magnitude]

    def get_analysis(self, folder, output_folder):

        if not os.path.exists(output_folder):
            return "Output folder doesn't exist"

        if not os.path.exists(folder):
            return "Input folder doesn't exist"

        columns = ['file', 'score', 'magnitude']
        data = []
        for file in os.listdir(folder):
            try:
                data.append(self.analyse(file, folder))
            except Exception as ex:
                print(ex)
                skipped_files.append(file)

        df = pd.DataFrame(data, columns=columns)
        df.to_csv(os.path.join(output_folder, 'google_text.csv'))
        print(skipped_files)
        return "Success"
