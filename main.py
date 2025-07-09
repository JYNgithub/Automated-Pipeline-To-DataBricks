import os
from dotenv import load_dotenv
from prefect import flow, task
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.workspace import ImportFormat

#####################################################
# Configuration
#####################################################

# Load confidential information from .env file (if running locally)
load_dotenv()

# Set up project root and cookies path
project_root = os.path.dirname(os.path.abspath(__file__))
audio_file = os.path.join(project_root, "audio.m4a")

# Set up target path in Databricks workspace
save_audio_path = "/Workspace/Users/chongjinjye@gmail.com/audio.m4a"

#####################################################
# Prefect Tasks and Flows
#####################################################

@task
def upload_to_databricks(local_file_path: str, host: str, token: str):
    
    print("Uploading audio to Databricks workspace...")
    try:
        host = os.getenv("DATABRICKS_HOST")
        token = os.getenv("DATABRICKS_TOKEN")
        if not host or not token:
            raise ValueError("Databricks credentials not set in environment.")
    
        w = WorkspaceClient(
            host = host,
            token = token
        )
        remote_path = save_audio_path
        with open(local_file_path, "rb") as f:
            data = f.read()
        w.workspace.upload(
            path=remote_path,
            content=data,
            format=ImportFormat.AUTO,
            overwrite=True
        )
        print("[SUCCESS] Uploaded audio to Databricks workspace.")
    except Exception as e:
        raise RuntimeError(f"Failed to upload to Databricks: {e}")


@flow
def upload_to_databricks_flow(host: str, token: str):
    try:
        upload_to_databricks(audio_file, host, token)
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    upload_to_databricks_flow()