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
from forms import Forms


#========Methods========
def test_ui():
    """
    This function will be used to test the functionality of the app
    without the need of a graphical user interface.
    """
    menu_str = """
    ======================Test UI Menu======================
    1. Get all users
    2. Get all forms
    3. Create a test form
    0. Exit
    ========================================================
    >>> """
    while True:
        choice = input(menu_str)
        if choice == "1":
            get_users()
        elif choice == "2":
            get_forms()
        elif choice == "3":
            # test_form = create_test_form()
            # print("Test form created:")
            # print(test_form)
            print("The forms was already created")
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

def create_test_form():
    """
    Creates and returns a test Forms object with dummy data.
    """
    test_data = {
        "name": "B",
        "email": "C",
        "phone": "D",
        "tipo_entrada": "E",
        "alergias": "F",
        "comentarios": "G",
    }
    
    test_user_fk = 1
    test_event_fk = 1
    test_drive_url = "https://docs.google.com/spreadsheets/d/1wm8dO2hlW3gGA5IsAG2jM1Ujq5ELi_NkwiZCDNh77CY/edit?resourcekey=&gid=1035676178#gid=1035676178"
    
    # Instantiate the Forms object
    # Note: id_pk is left as None, assuming the backend assigns it upon saving.
    test_form = Forms(
        user_fk=test_user_fk,
        drive_url=test_drive_url,
        data=test_data,
        event_fk=test_event_fk
    )
    
    return test_form

def get_forms():
    # Use http://localhost:8000/forms if you are testing on your own computer
    api_url = "https://reg-app-backend.onrender.com/forms" 

    # 1. Send the GET request to the middleman
    response = requests.get(api_url)

    # 2. Check if the request was successful (HTTP 200 OK)
    if response.status_code == 200:
        # 3. Unpack the JSON response back into standard Python dictionaries
        forms = response.json()
        
        print("Here are all the forms:")
        forms_lst = []
        for form in forms:
            print(f"ID: {form['id_pk']} | User FK: {form['user_fk']} | Event FK: {form['event_fk']}")
            forms_lst.append(Forms(user_fk=form['user_fk'], drive_url=form['drive_url'], data=form['data'], id_pk=form['id_pk'], event_fk=form['event_fk']))
        for form in forms_lst:
            print(form)
    else:
        print(f"Error: Received status code {response.status_code}")

if __name__ == "__main__":
    test_ui()