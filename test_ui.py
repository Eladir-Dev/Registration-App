"""
======================General descriptions======================
Creation Date: 22/sep/2026
File: test_ui.py
Created by: Eduardo J. Matos
Contributers:
    * Eduardo J. Matos
    *
-----------------------------------------------------------------
Description:
This script will be used to test the functionality of the app
without the need of a graphical user interface.
======================Modification Info==========================
Last modification date: 28/oct/2026
Last modified by: Eduardo J. Matos
-----------------------------------------------------------------
Last modifications:
    *  test_ui method was made.
        - works as a menu to test the app without the need of a graphical user interface.
    * get_users method was made.
        - sends a GET request to the middleman to get all users from the database.
================================================================
"""

#========Imports========
import requests


#========Methods========
def test_ui():
    """
    This function will be used to test the functionality of the app
    without the need of a graphical user interface.
    """
    menu_str = """
    ======================Test UI Menu======================
    1. Get all users
    0. Exit
    ========================================================
    >>> """
    while True:
        choice = input(menu_str)
        if choice == "1":
            get_users()
        elif choice == "0":
            print("Exiting the test UI.")
            break
        else:
            print("Invalid choice. Please try again.")
def get_users():
    # Use http://localhost:8000/users if you are testing on your own computer
    api_url = "https://reg-app-backend.onrender.com/users" 

    # 1. Send the GET request to the middleman
    response = requests.get(api_url)

    # 2. Check if the request was successful (HTTP 200 OK)
    if response.status_code == 200:
        # 3. Unpack the JSON response back into standard Python dictionaries
        users = response.json()
        
        print("Here are all the users:")
        # print(users)
        for user in users:
            print(f"ID: {user['id_pk']} | Username: {user['name']} | Email: {user['email']}")
    else:
        print(f"Error: Received status code {response.status_code}")

if __name__ == "__main__":
    test_ui()