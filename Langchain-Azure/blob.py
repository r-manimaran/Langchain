from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv  
load_dotenv()
# Retrieve the connection string from an environment variable
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
print(connect_str)
container_name = "filescontainer"
blob_name ="pwamsstorage"
directory_path = "Data"

# create the client 
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

#upload the files in the directory in directory_path
for root, dirs, files in os.walk(directory_path):
    for file in files:
        file_path = os.path.join(root, file)
        blob_name = file
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)
        print(f"File {file} uploaded to container {container_name}")