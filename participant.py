"""
======================General descriptions======================
Creation Date: 19/nov/2026
File: participant.py
Created by: Eduardo J. Matos
Contributers:
    * Eduardo J. Matos
    *
-----------------------------------------------------------------
Description:
This script containes the participant class and its methods.
======================Modification Info==========================
Last modification date: 19/nov/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    * file was created.
        - Some basic methods were added.
    * refresh method created.
        - updates the local data from the backend.
    * save method created.
        - saves the participant's data to the backend.
================================================================
"""

class Participant:
    def __init__(self, name, email, phone=None, data=None, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.data = data if data is not None else {} # json that contains every other information that is not name, email, and phone number.
        self.refresh()

    def refresh(self):
        """
        This method will be used to update the local data from the backend.
        """
        pass
        

    def save(self):
        """
        This method will be used to save the participant's data to the backend.
        """
        # Here you would implement the logic to save the participant's data to the backend
        # For example, you might make a request to an API endpoint with the participant's data
        pass