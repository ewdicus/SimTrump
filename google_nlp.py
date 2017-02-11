import os
import json

from google.cloud import language

CREDENTIALS_FILE = "./google_credentials.json"

class Google():
    """Google API wrapper"""

    def __init__(self):
        self.client = self.create_client()

    def create_client(self):
        # GOOGLE_APPLICATION_CREDENTIALS is a path to the account key. If we
        # don't have that we'll need to write the credentials
        GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if GOOGLE_APPLICATION_CREDENTIALS:
            # Do default
            return language.Client()

        self.write_credentials()
        return language.Client.from_service_account_json(CREDENTIALS_FILE)

    def write_credentials(self):
        # This is a hack, but don't want to store the account key file in github,
        # so instead have it's contents as an env var and write them to a temp file.

        #  GOOGLE_CREDENTIALS is the contents of the key file
        GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")

        with open(CREDENTIALS_FILE, "w") as f:
            f.write(GOOGLE_CREDENTIALS)
            f.write("\n")

    def analyze_text_sentiment(self, text):
        document = self.client.document_from_text(text)

        # Detects the sentiment of the text
        sentiment = document.analyze_sentiment()
        return (sentiment.score, sentiment.magnitude)
