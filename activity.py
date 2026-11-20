"""
======================General descriptions======================
Creation Date: 20/nov/2026
File: activity.py
Created by: Eduardo J. Matos
Contributers:
- Eduardo J. Matos
    *
-----------------------------------------------------------------
Description:
This script contains the Activity class and its methods to 
interface with the backend application for the activity table.
======================Modification Info==========================
Last modification date: 20/nov/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    * Initial creation based on participant.py structure.
    * Implemented environment variable for API base URL.
    * Implemented requests.Session() for connection pooling.
================================================================
"""
import os
import requests
from rich.console import Console

class Activity:
    # Class-level session shares the TCP connection pool across all instances
    _session = requests.Session()

    def __init__(self, area_fk=None, description=None, id_pk=None):
        """
        Initializes the Activity object and syncs it with the backend.
        
        :param area_fk: ID of the associated area (optional).
        :param description: Description of the activity (optional).
        :param id_pk: Primary key. If None, a new record will be created on save.
        """
        self.id_pk = id_pk
        self.area_fk = area_fk
        self.description = description
        
        # Pulls the base URL from the environment
        base_url = os.getenv("API_BASE_URL", "http://localhost:8000")
        # Endpoint URL mapped to the FastAPI backend route
        self.url = f"{base_url}/activities"
        
        self.json = self.to_json()
        self.save()

    def __str__(self):
        """
        Provides a formatted string and JSON output for the console.
        """
        console = Console(color_system="truecolor")
        
        output = f"""id_pk: {self.id_pk}
        area_fk: {self.area_fk}
        description: {self.description}"""
        
        with console.capture() as capture:
            console.print_json(data=self.json)

        return f"{output}\n{capture.get()}"

    def refresh(self):
        """
        Updates the local activity data by fetching the latest record from the backend.
        """
        if not self.id_pk:
            print("Cannot refresh: id_pk is missing.")
            return

        try:
            response = self._session.get(f"{self.url}/{self.id_pk}", timeout=120)
            response.raise_for_status() 
            updated_record = response.json() 
            
            self.area_fk = updated_record.get("area_fk")
            self.description = updated_record.get("description")
            
            self.json = self.to_json()
            print("Refresh successful:", updated_record)
            
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            try:
                print("Details:", response.json())
            except ValueError:
                print("Details:", response.text)
        except requests.exceptions.RequestException as err:
            print(f"Connection Error: {err}")

    def to_json(self):
        """
        Creates a JSON object representation of the activity data.
        """
        return {
            "id_pk": self.id_pk,
            "area_fk": self.area_fk,
            "description": self.description
        }

    def save(self):
        """
        Saves the activity's data to the backend. Creates a new record if id_pk is None,
        otherwise updates the existing record via PUT.
        """
        self.json = self.to_json() 
        try:
            if self.id_pk is None:
                # Create new record
                response = self._session.post(self.url, json=self.json, timeout=120)
                response.raise_for_status()
                updated_record = response.json()
                self.id_pk = updated_record.get("id_pk") 
                self.json = self.to_json() 
            else:
                # Update existing record
                response = self._session.put(f"{self.url}/{self.id_pk}", json=self.json, timeout=120)
                response.raise_for_status()
                updated_record = response.json()
            
            print("Update successful:", updated_record)
            
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            try:
                print("Details:", response.json())
            except ValueError:
                print("Details:", response.text)
        except requests.exceptions.RequestException as err:
            print(f"Connection Error: {err}")

    def delete(self):
        """
        Deletes the activity data from the backend using its id_pk.
        """
        if not self.id_pk:
            print("Cannot delete: id_pk is missing.")
            return
            
        try:
            response = self._session.delete(f"{self.url}/{self.id_pk}", timeout=120)
            response.raise_for_status()
            print("Delete successful:", response.json())
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            try:
                print("Details:", response.json())
            except ValueError:
                print("Details:", response.text)
        except requests.exceptions.RequestException as err:
            print(f"Connection Error: {err}")