"""
======================General descriptions======================
Creation Date: 19/nov/2026
File: participant.py
Created by: Eduardo J. Matos
Contributers:
- Eduardo J. Matos
    *
-----------------------------------------------------------------
Description:
This script contains the participant class and its methods to 
interface with the backend application.
======================Modification Info==========================
Last modification date: 19/nov/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    * Implemented environment variable for API base URL.
    * Implemented requests.Session() for connection pooling.
        - This improves performance by reusing TCP connections for multiple requests.
        - Still most be tested to see if it works as expected.
    * Fixed string capture and JSON parsing bugs in refresh and __str__.
================================================================
"""
import os
import requests
from rich.console import Console

class Participant:
    # Class-level session shares the TCP connection pool across all instances
    _session = requests.Session()

    def __init__(self, event_fk, name, email, phone=None, user_fk=None, room_fk=None, id_pk=None):
        self.id_pk = id_pk
        self.event_fk = event_fk
        self.user_fk = user_fk
        self.room_fk = room_fk
        self.name = name
        self.email = email
        self.phone = phone
        
        # Pulls the base URL from the environment, defaulting to the Render URL if not found
        base_url = os.getenv("API_BASE_URL", "https://reg-app-backend.onrender.com")
        self.url = f"{base_url}/participant"
        
        self.json = self.to_json()
        self.save()

    def __str__(self):
        console = Console(color_system="truecolor")
        
        output = f"""id_pk: {self.id_pk}
        event_fk: {self.event_fk}
        user_fk: {self.user_fk}
        room_fk: {self.room_fk}
        name: {self.name}
        email: {self.email}
        phone: {self.phone}"""
        
        with console.capture() as capture:
            console.print_json(data=self.json)

        return f"{output}\n{capture.get()}"

    def refresh(self):
        """
        Updates the local participant data by fetching the latest record from the backend.
        """
        if not self.id_pk:
            print("Cannot refresh: id_pk is missing.")
            return

        try:
            response = self._session.get(f"{self.url}/{self.id_pk}", timeout=120)
            response.raise_for_status() 
            updated_record = response.json() 
            
            self.event_fk = updated_record.get("event_fk")
            self.user_fk = updated_record.get("user_fk")
            self.room_fk = updated_record.get("room_fk")
            self.name = updated_record.get("name")
            self.email = updated_record.get("email")
            self.phone = updated_record.get("phone")
            
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
        Creates a JSON object representation of the participant data.
        """
        return {
            "id_pk": self.id_pk,
            "event_fk": self.event_fk,
            "user_fk": self.user_fk,
            "room_fk": self.room_fk,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

    def save(self):
        """
        Saves the participant's data to the backend. Creates a new record if id_pk is None,
        otherwise updates the existing record.
        """
        self.json = self.to_json() 
        try:
            if self.id_pk is None:
                response = self._session.post(self.url, json=self.json, timeout=120)
                response.raise_for_status()
                updated_record = response.json()
                self.id_pk = updated_record.get("id_pk") 
                self.json = self.to_json() 
            else:
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
        Deletes the participant data from the backend.
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