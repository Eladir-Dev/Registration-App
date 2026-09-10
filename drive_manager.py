"""
======================General descriptions======================
Creation Date: 9/sep/2026
File: drive_manager.py
Created by: Eduardo J. Matos
Contributers:
    *
    *
-----------------------------------------------------------------
Description:
This script takes care of the interaction with the Google Drive API. 
It handles authentication, file uploads, and downloads.
======================Modification Info==========================
Last modification date: 9/sep/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    *  authenticate_drive, upload_file, and download_file were added.
        - They are going to be finished at later date.
    * 
================================================================
"""
#============Imports============#

#=========Code Starts===========#

def authenticate_drive():
    """
    Authenticates the application with Google Drive API.
    Returns the authenticated service object.
    """
    # Authentication logic here
    pass

def upload_file(file_path, folder_id):
    """
    Uploads a file to Google Drive.

    :param file_path: Path to the local file to be uploaded
    :param folder_id: ID of the folder where the file will be uploaded
    """
    # File upload logic here
    pass

def download_file(folder_id, file_name, destination_path):
    """
    Downloads a file from Google Drive.

    :param folder_id: ID of the folder containing the file
    :param file_name: Name of the file to be downloaded
    :param destination_path: Local path where the file will be saved
    """
    # File download logic here
    pass