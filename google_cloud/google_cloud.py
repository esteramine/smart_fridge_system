import os
from dotenv import load_dotenv
from google.cloud import storage

BUCKET_NAME = "chillmate"

load_dotenv()
credentials_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY_PATH')
client = storage.Client.from_service_account_json(credentials_path)
bucket = client.bucket(BUCKET_NAME)

def upload_blob_from_stream(image_bytes, destination_blob_name):
    try:
        blob = bucket.blob(destination_blob_name)

        # Rewind the stream to the beginning. 
        image_bytes.seek(0)

        blob.upload_from_file(image_bytes)
        print(f"Google Cloud Upload successful: {destination_blob_name}.")
        # Return the public URL
        return blob.public_url
    except Exception as e:
        print(f"Google Cloud Upload Failed: {destination_blob_name}. Error: {e}")
        return ""

if __name__ == "__main__":
    # test the connection of google cloud
    blobs = client.list_blobs("chillmate")
    for blob in blobs:
        print(blob.name)