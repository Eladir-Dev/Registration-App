
"""
======================General descriptions======================
Creation Date: 25/nov/2026
File: room.py
Created by: Bryan Rivera Rivera
Contributors:
    - Bryan Rivera Rivera
-----------------------------------------------------------------
Description:
This script contains the Room class and its methods to
interface with the backend application for the room table.

The class provides functionality to create, retrieve, update,
and delete room records through HTTP requests. Each room is
associated with an area through its foreign key.
======================Modification Info==========================
Last modification date: 25/nov/2026
Last modified by: Bryan Rivera Rivera
-----------------------------------------------------------------
Last modifications:
    * Initial creation based on the activity.py structure.
    * Implemented CRUD operations for room management.
    * Implemented environment variable for API base URL.
    * Implemented requests.Session() for connection pooling.
    * Added validation for required room attributes.
================================================================
"""

# ==================== Imports ==================== #

import os
import requests
from rich.console import Console


# ==================== Room Class ==================== #

class Room:
    """
    Represents a room within an event area.

    This class manages room information and communicates
    with the backend API to perform CRUD operations.

    Attributes:
        id_pk: Primary key of the room.
        area_fk: Foreign key of the associated area.
        type: Type of room.
        description: Additional information about the room.
        url: Backend API endpoint for room management.
        json: Dictionary representation of the room data.
    """

    # Class-level session shares the TCP connection pool
    # across all Room instances.
    _session = requests.Session()

    def __init__(self, area_fk, room_type,
                 description=None, id_pk=None):
        """
        Initializes a Room object and synchronizes its
        information with the backend.

        :param area_fk: ID of the associated area.
        :param room_type: Type of room.
        :param description: Optional room description.
        :param id_pk: Primary key of the room. If None,
                       a new record will be created.
        """

        # Initialize room attributes according to the ERD.
        self.id_pk = id_pk
        self.area_fk = area_fk
        self.type = room_type
        self.description = description

        # Retrieve the backend URL from the environment.
        # Default to localhost if no URL is configured.
        base_url = os.getenv(
            "API_BASE_URL",
            "http://localhost:8000"
        ).rstrip("/")

        # Proposed endpoint for room management.
        # Must be confirmed with the backend implementation.
        self.url = f"{base_url}/rooms"

        # Generate the dictionary representation.
        self.json = self.to_json()

        # Synchronize the room information with the backend.
        self.save()

    def __str__(self):
        """
        Returns a formatted string representation of
        the room information using the Rich library.

        :return: Formatted room data as a string.
        """

        console = Console(color_system="truecolor")

        # Capture the formatted JSON output instead of
        # printing it directly to the console.
        with console.capture() as capture:
            console.print_json(data=self.to_json())

        return capture.get()

    def to_json(self):
        """
        Converts the room attributes into a dictionary
        that can be serialized as JSON when communicating
        with the backend API.

        :return: Dictionary containing the room data.
        """

        return {
            "id_pk": self.id_pk,
            "area_fk": self.area_fk,
            "type": self.type,
            "description": self.description
        }

    def refresh(self):
        """
        Retrieves the latest room information from the
        backend and updates the local object attributes.

        Uses an HTTP GET request to retrieve the record
        associated with the room's primary key.

        :return: Updated room record from the backend.
        :raises ValueError: If the primary key is missing.
        :raises requests.exceptions.RequestException:
            If the HTTP request fails.
        """

        # A room must have an ID before it can be retrieved.
        if self.id_pk is None:
            raise ValueError(
                "Cannot refresh a room without an ID."
            )

        # Request the room record from the backend.
        response = self._session.get(
            f"{self.url}/{self.id_pk}",
            timeout=120
        )

        # Raise an exception if the HTTP request fails.
        response.raise_for_status()

        # Convert the response into a Python dictionary.
        record = response.json()

        # Update local attributes with the backend data.
        self.area_fk = record.get("area_fk")
        self.type = record.get("type")
        self.description = record.get("description")

        # Update the local dictionary representation.
        self.json = self.to_json()

        return record

    def save(self):
        """
        Saves the room information to the backend.

        If id_pk is None, an HTTP POST request is used
        to create a new room record.

        If id_pk already exists, an HTTP PUT request is
        used to update the corresponding room record.

        :return: Room record returned by the backend.
        :raises ValueError: If required attributes are
                            missing or invalid.
        :raises requests.exceptions.RequestException:
            If the HTTP request fails.
        """

        # Validate that the room has an associated area.
        if self.area_fk is None:
            raise ValueError("area_fk is required.")

        # Validate that the room type is a non-empty string.
        if not isinstance(self.type, str) or not self.type.strip():
            raise ValueError("Room type is required.")

        # Remove unnecessary leading and trailing spaces.
        self.type = self.type.strip()

        # Update the dictionary before sending the request.
        self.json = self.to_json()

        if self.id_pk is None:

            # Create a new room record using POST.
            response = self._session.post(
                self.url,
                json=self.json,
                timeout=120
            )

        else:

            # Update an existing room record using PUT.
            response = self._session.put(
                f"{self.url}/{self.id_pk}",
                json=self.json,
                timeout=120
            )

        # Verify that the request was successful.
        response.raise_for_status()

        # Retrieve the record returned by the backend.
        record = response.json()

        # Store the primary key generated by the backend
        # when a new room record is created.
        if self.id_pk is None:
            self.id_pk = record["id_pk"]

        # Synchronize the local dictionary representation.
        self.json = self.to_json()

        return record

    def delete(self):
        """
        Deletes the room record from the backend using
        its primary key.

        An HTTP DELETE request is sent to the endpoint
        corresponding to the specified room.

        The backend is responsible for enforcing foreign
        key constraints and handling participants that
        may still be assigned to the room.

        :return: True if the deletion is successful.
        :raises ValueError: If the primary key is missing.
        :raises requests.exceptions.RequestException:
            If the HTTP request fails.
        """

        # A room must have an ID before it can be deleted.
        if self.id_pk is None:
            raise ValueError(
                "Cannot delete a room without an ID."
            )

        # Send the deletion request to the backend.
        response = self._session.delete(
            f"{self.url}/{self.id_pk}",
            timeout=120
        )

        # Verify that the deletion was successful.
        response.raise_for_status()

        return True
