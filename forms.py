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
Last modification date: 2/nov/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    * Esential functions were made.
        - Interaction with the backend was made possible.
    * 
================================================================
"""
import requests

class forms():
    def __init__(self, user_fk, data, id_pk=None, event_fk=None):
        self.id_pk = id_pk
        self.user_fk = user_fk
        self.event_fk = event_fk
        self.data = data
        self.json = self.create_form_json()
        self.url = "https://reg-app-backend.onrender.com/forms"

    def __str__(self):
        return "Forms class"

    def create_form_json(self):
        """
        This function will be used to create a JSON object from the form data.
        :return: JSON object
        """
        form_json = {
            "id_pk": self.id_pk,
            "user_fk": self.user_fk,
            "event_fk": self.event_fk,
            "data": self.data
        }
        return form_json

    def save(self):
        try:
            if self.id_pk is None:
                # If id_pk is None, it's a new record; use POST to create it
                response = requests.post(self.url, json=self.json)
            else:
                # The json= parameter automatically sets the Content-Type header to application/json
                # and serializes the Python dictionary into a JSON string
                response = requests.put(f"{self.url}/{self.id_pk}", json=self.json)
            
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

    def import_data(name:int, email:int, phone:int = None):
        """
        This function will be used to import data from the participants.
        :param name: Number of column for name.
        :param email: Number of column for email.
        :param phone: Number of column for phone. (Optional)
        :return: None
        """
        excel_file = "participants.xlsx"




       