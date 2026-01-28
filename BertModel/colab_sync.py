"""
Sync local files to Google Colab using Google Drive
"""

from google.colab import drive
import shutil
import os

# Mount Google Drive
drive.mount('/content/drive')

# Create project directory in Drive
project_dir = '/content/drive/MyDrive/BertModel'
os.makedirs(project_dir, exist_ok=True)

# Sync files from Drive to Colab workspace
local_dir = '/content/BertModel'
if os.path.exists(project_dir):
    shutil.copytree(project_dir, local_dir, dirs_exist_ok=True)
    print(f"✓ Synced files from Drive to {local_dir}")
else:
    print(f"Creating new project directory at {project_dir}")

# Function to sync back to Drive
def sync_to_drive():
    if os.path.exists(local_dir):
        shutil.copytree(local_dir, project_dir, dirs_exist_ok=True)
        print(f"✓ Synced files back to Drive")
