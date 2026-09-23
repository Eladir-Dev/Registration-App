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
Last modification date: 22/sep/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    *  Create_Service, get_drive_service, upload_to_drive,
       download_from_drive, and get_folder_id_by_path were added.
        - This were function I created for another proyect they 
          should work fine for this proyect.
    * 
================================================================
"""
#============Imports============#
import io
import pickle
import os
import datetime
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

#=========Configuration=========#
CLIENT_SECRET_FILE = 'credentials/google_credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
# This scope allows full read/write access to Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

#=========Code Starts===========#

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    """
    Create and return an authorized Google API service object.

    This helper centralizes OAuth2 credential creation and caching for a
    specific Google API (for example, Drive). It attempts to load a
    previously-saved credential pickle named `token_{api_name}_{api_version}.pickle`.
    If no valid credentials are found, it runs the OAuth flow in a local
    server (browser) to obtain new credentials and saves them to the pickle
    file for subsequent runs.

    Parameters:
        client_secret_file (str): Path to the OAuth 2.0 client secrets JSON file
            downloaded from Google Cloud Console.
        api_name (str): Google API service name (for example, 'drive').
        api_version (str): Version of the API (for example, 'v3').
        *scopes (tuple): Single iterable of OAuth scopes required by the API.

    Returns:
        googleapiclient.discovery.Resource | None: An authorized service
        instance on success (from `googleapiclient.discovery.build`), or
        `None` if the service could not be created.

    Behavior:
        - Loads credentials from `token_{api_name}_{api_version}.pickle` when
          available and valid.
        - Refreshes expired credentials when a refresh token is present.
        - Launches a local webserver OAuth flow to get new credentials when
          required and then persists them to the pickle file.

    Notes:
        - Exceptions from the underlying `build()` call are caught, logged to
          stdout, and cause the function to return `None`.
        - This function prints simple progress messages; remove prints for
          production use if noisy output is undesirable.
    """
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

# def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
#     """
#     Convert discrete date/time components to an RFC3339 / RFC3339-UTC string.

#     Example output: '2026-09-09T14:30:00Z'

#     Parameters:
#         year (int): Four-digit year. Defaults to 1900.
#         month (int): Month (1-12). Defaults to 1.
#         day (int): Day of month (1-31). Defaults to 1.
#         hour (int): Hour (0-23). Defaults to 0.
#         minute (int): Minute (0-59). Defaults to 0.

#     Returns:
#         str: RFC3339-formatted datetime string with a trailing 'Z' to indicate UTC.

#     Notes:
#         - This helper constructs a naive `datetime.datetime` from the provided
#           components and appends the literal 'Z'. If you need timezone-aware
#           values, convert to UTC explicitly using `datetime.timezone.utc`.
#     """
#     dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
#     return dt

def get_drive_service():
    """
    Create and return an authorized Google Drive API service object.

    This wraps the project's `Create_Service` helper (from Google.py) and
    applies the module-level configuration for client secrets, API name,
    version and scopes. The returned object is a `googleapiclient.discovery.Resource`
    that can be used to call Drive methods (files().list, files().create, etc.).

    Returns:
        googleapiclient.discovery.Resource: Authorized Drive service instance.

    Raises:
        Exception: Propagates any error raised by `Create_Service` during
        initialization (for example, missing credentials file or invalid scope).
    """
    return Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


def upload_to_drive(service, local_file_path, drive_file_name, drive_folder_path=''):
    """
    Upload or replace a file at a given Drive path.

    The function searches only within the specified Drive folder path for an
    existing file with the same name. If found, the existing file is updated
    with the contents of `local_file_path`. If not found, a new file is
    created inside the target folder.

    Parameters:
        service (Resource): Authorized Drive API service (from `get_drive_service`).
        local_file_path (str): Path to the local file to upload.
        drive_file_name (str): Target filename to use in Drive (e.g. 'data.txt').
        drive_folder_path (str): Optional slash-separated folder path in Drive
            (e.g. 'Folder/Subfolder'). If empty or '/', the file is placed in
            the Drive `root` folder.

    Returns:
        None

    Side effects:
        - Prints status messages for upload/update operations.
    """

    folder_id = get_folder_id_by_path(service, drive_folder_path)
    if folder_id is None:
        return  # Stop if the folder path doesn't exist

    # 1. Search for the file ONLY inside the specific folder
    query = f"name='{drive_file_name}' and '{folder_id}' in parents and mimeType='text/plain' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])

    media = MediaFileUpload(local_file_path, mimetype='text/plain', resumable=True)

    if files:
        # Update existing
        file_id = files[0].get('id')
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"Updated: '{drive_folder_path}/{drive_file_name}' (ID: {file_id})")
    else:
        # Create new inside the folder
        file_metadata = {
            'name': drive_file_name,
            'parents': [folder_id]  # This is how Drive assigns files to folders
        }
        new_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"Uploaded new to: '{drive_folder_path}/{drive_file_name}' (ID: {new_file.get('id')})")


def download_from_drive(service, drive_file_name, local_file_path, drive_folder_path=''):
    """
    Download a file from a specific Drive path to local disk.

    The function searches only inside the provided Drive folder path for a
    file with the given name. If found, it streams the file contents and
    writes them to `local_file_path`. If not found, the function prints an
    error message and returns without raising.

    Parameters:
        service (Resource): Authorized Drive API service.
        drive_file_name (str): Name of the file to download from Drive.
        local_file_path (str): Local destination path for the downloaded file.
        drive_folder_path (str): Optional slash-separated folder path in Drive
            to restrict the search. Empty means `root`.

    Returns:
        None

    Side effects:
        - Writes a file to `local_file_path` if download succeeds.
        - Prints an error message if the target file or folder cannot be found.
    """

    folder_id = get_folder_id_by_path(service, drive_folder_path)
    if folder_id is None:
        return

    # 1. Search for the file ONLY inside the specific folder
    query = f"name='{drive_file_name}' and '{folder_id}' in parents and mimeType='text/plain' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
    files = response.get('files', [])

    if not files:
        print(f"Error: File '{drive_file_name}' not found in path '{drive_folder_path}'.")
        return

    file_id = files[0].get('id')
    request = service.files().get_media(fileId=file_id)

    with io.FileIO(local_file_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

    print(f"Downloaded from '{drive_folder_path}/{drive_file_name}' -> '{local_file_path}'.")

def get_folder_id_by_path(service, folder_path):
    """
    Resolve a slash-separated Drive folder path to a Drive folder ID.

    Given a path such as 'Parent/Child/Grandchild', this function walks from
    the Drive `root` and finds the first matching folder at each path segment,
    returning the Drive ID of the final folder. If `folder_path` is empty or
    '/', it returns the special ID string `'root'`.

    Note: Google Drive allows duplicate folder names; this routine always
    picks the first match returned by the API for each segment.

    Parameters:
        service (Resource): Authorized Drive API service.
        folder_path (str): Slash-separated path to resolve (e.g. 'A/B').

    Returns:
        str | None: Drive folder ID for the final path segment, `'root'` for
        an empty path, or `None` if any segment could not be found.
    """
    if not folder_path or folder_path == '/':
        return 'root'

    # Standardize slashes and split the path into parts
    parts = [p for p in folder_path.replace('\\', '/').split('/') if p]
    parent_id = 'root'

    for part in parts:
        # Search for a folder with this name inside the current parent_id
        query = f"name='{part}' and mimeType='application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed=false"
        response = service.files().list(q=query, spaces='drive', fields='files(id)').execute()
        files = response.get('files', [])

        if not files:
            print(f"Error: Folder '{part}' in the path '{folder_path}' was not found.")
            return None

        # Drive allows duplicate names, so we just assume the first match is correct
        parent_id = files[0].get('id')

    return parent_id


# ==========================================
# Example Usage
# ==========================================
# if __name__ == '__main__':
#     # Initialize the service
#     drive_service = get_drive_service()

#     if drive_service:
#         # Define file names
#         local_target = 'my_local_data.txt'
#         drive_target = 'my_cloud_data.txt'

#         # Create a dummy local file to test the upload
#         with open(local_target, 'w') as f:
#             f.write("This is some sample text data.")

#         print("--- Testing Upload ---")
#         # Run upload (will create it the first time, update it on subsequent runs)
#         upload_to_drive(drive_service, local_target, drive_target)

#         print("\n--- Testing Download ---")
#         # Run download (will fetch the cloud file and overwrite the local file)
#         download_from_drive(drive_service, drive_target, 'downloaded_data.txt')