
from google.cloud import storage
from dotenv import load_dotenv
import os
load_dotenv()

def list_files_and_generate_urls(bucket_name, folder_prefix):
    """List all files in a specified GCS bucket folder and generate their URLs in 'gs://' format."""
    # Initialize the Google Cloud Storage client
# service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
client = storage.Client()
# buckets = list(client.list_buckets())
# for bucket in buckets:
#     print(bucket.name)
#
# def list_folders(bucket_name):
#     """Lists all the folders in the bucket."""
#     storage_client = storage.Client()
#     blobs = storage_client.list_blobs(bucket_name, delimiter='/')
#
#     print(f"Folders in bucket {bucket_name}:")
#     for prefix in blobs.prefixes:
#         print(prefix)


def generate_signed_url(bucket_name, object_name, expiration_minutes=15):
    """Generates a signed URL for the specified object."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))

    print(f"The signed URL for the image is: {url}")
    return url


def upload_image_to_folder(bucket_name, source_file_path, destination_blob_name):
    """Uploads an image to a specific folder in a GCS bucket."""
    # Initialize a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # List all blobs in the specified folder
    blobs = bucket.list_blobs(prefix=folder_prefix)

    file_urls = []
    for blob in blobs:
        # Ensure the blob is in the correct folder
        if blob.name.startswith(folder_prefix) and not blob.name.endswith('/'):
            # Generate the URL in 'gs://' format
            gs_url = f"gs://{bucket_name}/{blob.name}"
            file_urls.append(gs_url)
            print(gs_url)

    return file_urls

# Example usage
bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET_NAME')
folder_prefix = 'docs/'
list_files_and_generate_urls(bucket_name, folder_prefix)

# from google.cloud import storage
# from dotenv import load_dotenv
# from flask import request, jsonify
# from flask_login import login_required
# from datetime import timedelta
# import os
#
# load_dotenv()
#
# def list_files_and_generate_urls(bucket_name, folder_prefix):
#     """List all files in a specified GCS bucket folder and generate their URLs."""
#     # Initialize the Google Cloud Storage client
#     storage_client = storage.Client()
#
#     # Get the bucket
#     bucket = storage_client.bucket(bucket_name)
#
#     # List all blobs in the specified folder
#     blobs = bucket.list_blobs(prefix=folder_prefix)
#
#     file_urls = []
#     for blob in blobs:
#         # Ensure the blob is in the correct folder
#         if blob.name.startswith(folder_prefix) and not blob.name.endswith('/'):
#             # Generate the URL for each blob
#             url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
#             file_urls.append(url)
#             print(url)
#
#     return file_urls
#
# # Define the bucket name and the folder prefix
# bucket_name = os.getenv('GOOGLE_CLOUD_BUCKET_NAME')
# folder_prefix = 'docs/'
#
# # Call the function to list files and generate URLs
# list_files_and_generate_urls(bucket_name, folder_prefix)

# from dotenv import load_dotenv
# import os
# from google.cloud import storage
# from datetime import timedelta
#
# load_dotenv()
#
# service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
# client = storage.Client()
# # buckets = list(client.list_buckets())
# # for bucket in buckets:
# #     print(bucket.name)
# #
# # def list_folders(bucket_name):
# #     """Lists all the folders in the bucket."""
# #     storage_client = storage.Client()
# #     blobs = storage_client.list_blobs(bucket_name, delimiter='/')
# #
# #     print(f"Folders in bucket {bucket_name}:")
# #     for prefix in blobs.prefixes:
# #         print(prefix)
#
#
# def generate_signed_url(bucket_name, object_name, expiration_minutes=15):
#     """Generates a signed URL for the specified object."""
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(object_name)
#
#     url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes))
#
#     print(f"The signed URL for the image is: {url}")
#     return url
#
#
# def upload_image_to_folder(bucket_name, source_file_path, destination_blob_name):
#     """Uploads an image to a specific folder in a GCS bucket."""
#     # Initialize a storage client
#     storage_client = storage.Client()
#
#     # Get the bucket
#     bucket = storage_client.bucket(bucket_name)
#
#     # Create a blob object with the desired folder path
#     blob = bucket.blob(destination_blob_name)
#
#     # Upload the image to the specified path
#     blob.upload_from_filename(source_file_path)
#
#     print(f"Image uploaded to {destination_blob_name} in bucket {bucket_name}.")
#
# # Define bucket name, local file path, and destination blob name (including folder path)
# bucket_name = "hackathon-082024"
# source_file_path = "/Downloads/cat.jpg"  # Replace with your image file path
# destination_blob_name = "media/images/cat.jpg"  # Replace with your desired path in the bucket
#
# # Call the function to upload the image
# # upload_image_to_folder(bucket_name, source_file_path, destination_blob_name)
#
# # Replace 'hackathon-082024' with your bucket name
# # bucket_name = 'hackathon-082024'
# # list_folders(bucket_name)
# generate_signed_url(bucket_name, destination_blob_name)
