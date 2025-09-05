import os
import shutil

def organize_downloads(download_folder):
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
        'Documents': ['.pdf', '.docx', '.txt', '.xlsx', '.csv'],
        'Audio': ['.mp3', '.wav', '.m4a'],
        'Videos': ['.mp4', '.mov', '.avi'],
    }

    for filename in os.listdir(download_folder):
        file_path = os.path.join(download_folder, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        _, file_ext = os.path.splitext(file_path)

        for folder, extensions in file_types.items():
            if file_ext.lower() in extensions:
                folder_path = os.path.join(download_folder, folder)
                os.makedirs(folder_path, exist_ok=True)
                shutil.move(file_path, os.path.join(folder_path, filename))
                break  # Move to the next file once it's sorted

# Replace 'Downloads' folder path with the Mac-specific one
organize_downloads(os.path.expanduser('~/Downloads'))

