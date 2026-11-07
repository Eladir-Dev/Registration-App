"""
======================General descriptions======================
Creation Date: 2/nov/2026
File: forms.py
Created by: Eduardo J. Matos
Contributers:
    * Eduardo J. Matos
    *
-----------------------------------------------------------------
Description:
This script will be used to handle the forms data and send it to the backend.
======================Modification Info==========================
Last modification date: 7/nov/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    * code fix.
        - Some bugs fixed.
    * added error handeling to the get functions.
================================================================
"""
import requests
import os
from openpyxl import load_workbook

"""
data format:
{
    "name": "A", #Letter of the column where the name is located.
    "email": "B", #Letter of the column where the email is located.
    "phone": "C" #Letter of the column where the phone is located.
    .
    .
    .
    Other columns.
}
"""
class Forms():
    def __init__(self, user_fk, drive_url, data=None, id_pk=None, event_fk=None):
        self.id_pk = id_pk
        self.user_fk = user_fk
        self.event_fk = event_fk
        self.data = data # json that contains: for example {"name"= "A", "email"="B", "phone"="C"}
        self.drive_url = drive_url
        self.json = self.to_json()
        self.url = "https://reg-app-backend.onrender.com/forms"

        self.save()  # Call save method to send data to the backend
        
        if self.data is None:
            self.import_data()  # Import data from the associated Excel file
        
        

    def __str__(self):
        return f"Forms class: {self.json}"

    def to_json(self):
        """
        This function will be used to create a JSON object from the form data.
        :return: JSON object
        """
        form_json = {
            "id_pk": self.id_pk,
            "user_fk": self.user_fk,
            "event_fk": self.event_fk,
            "data": self.data,
            "drive_url": self.drive_url
        }
        return form_json

    def save(self):
        self.json = self.to_json()  # Update the JSON representation before saving
        try:
            if self.id_pk is None:
                # If id_pk is None, it's a new record; use POST to create it
                response = requests.post(self.url, json=self.json, timeout=120)
                response.raise_for_status()
                updated_record = response.json()
                self.id_pk = updated_record.get("id_pk") # Update the ID here
                self.json = self.to_json()  # Update the JSON representation with the new ID
            else:
                # The json= parameter automatically sets the Content-Type header to application/json
                # and serializes the Python dictionary into a JSON string
                response = requests.put(f"{self.url}/{self.id_pk}", json=self.json, timeout=120)
            
            # Check if the HTTP status code is 200-299; raises an exception if not
            response.raise_for_status()
            
            updated_record = response.json()
            print("Update successful:", updated_record)
            # return updated_record
            
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            # Print the detailed error message returned by FastAPI (e.g., validation errors)
            print("Details:", response.json())
        except requests.exceptions.RequestException as err:
            print(f"Connection Error: {err}")

    def get_by_name(self, name):
        """
        This function will be used to get a row from the excel file 
        by the name of a person.
        :return: JSON object of the form if found, else None.
        """
        try:
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except FileNotFoundError:
            self.download_excel_from_middleman()
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except Exception as e:
            print(f"An error occurred while loading the workbook: {e}")
            return []

        # Select the active sheet (usually the first one)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2):
            row_data = {cell.column_letter: cell.value for cell in row}
            if row_data.get(self.data["name"]) == name:
                wb.close()
                return row_data
        wb.close()
        return None

    def get_by_email(self, email):
        """
        This function will be used to get a row from the excel file 
        by the email of a person.
        :return: JSON object of the form if found, else None.
        """
        try:
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except FileNotFoundError:
            self.download_excel_from_middleman()
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except Exception as e:
            print(f"An error occurred while loading the workbook: {e}")
            return []

        # Select the active sheet (usually the first one)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2):
            row_data = {cell.column_letter: cell.value for cell in row}
            if row_data.get(self.data["email"]) == email:
                wb.close()
                return row_data
        wb.close()
        return None

    def get_all_rows(self):
        """
        This function will be used to get all the rows from the excel file.
        :return: List of JSON objects of the forms.
        """
        try:
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except FileNotFoundError:
            self.download_excel_from_middleman()
            wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        except Exception as e:
            print(f"An error occurred while loading the workbook: {e}")
            return []

        # Select the active sheet (usually the first one)
        sheet = wb.active
        all_rows = []
        # Remove values_only=True
        for row in sheet.iter_rows(min_row=2): 
            row_data = {cell.column_letter: cell.value for cell in row}
            all_rows.append(row_data)
        wb.close()
        return all_rows

    def import_data(self):
        """
        This function will be used to import data from the asociated excel file and save 
        it to the backend's cache.
        :return: None
        """
        
        # TODO: Implement the logic to read the Excel file and import data into self.data
        self.download_excel_from_middleman()
        wb = load_workbook(f"cache/forms_{self.id_pk}.xlsx", data_only=True)
        sheet = wb.active
        for row in sheet.iter_rows(min_row=2, max_row=10, min_col=1, max_col=3, values_only=True):
            print(row)

        wb.close()

    def download_excel_from_middleman(self, save_path=None):
        os.makedirs("cache", exist_ok=True) # Create the cache directory if it doesn't exist
        if save_path is None:
            save_path = f"cache/forms_{self.id_pk}.xlsx"
        # if os.path.isfile(save_path):
        #     return  # File already exists, no need to download again
        
        middleman_url = self.url.replace("forms", "download-excel")
        
        payload = {
            "link": self.drive_url
        }
        
        try:
            # Stream=True is good practice for downloading files
            response = requests.post(middleman_url, json=payload, stream=True, timeout=120)
            response.raise_for_status() # Check for HTTP errors
            
            # Write the binary content to a local file
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    
            print(f"File successfully downloaded and saved to {save_path}")
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to download the file: {e}")

