from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
load_dotenv()

class AzureSync:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_CONNECTION_KEY_STRING")

    def synch_folder_to_az(self, container: str, directory: str, blob_prefix = ""):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_container_client(container)

        try:
            container_client.create_container()
        except Exception:
            pass

        for root, _, files in os.walk(directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, directory).replace("\\", '/')
                blob_path = f"{blob_prefix}/{relative_path}".lstrip("/")

                with open(local_path, 'rb') as data:
                    container_client.upload_blob(name = blob_path, data = data, overwrite = True)