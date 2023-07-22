
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Calendar access code from Google Workspace:
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPE = [
    "https://www.googleapis.com/auth/calendar",  # Google Calendar scope
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]


def obtain_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    CREDS = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('eicreds.json'):
        CREDS = Credentials.from_service_account_file('eicreds.json')
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    else:
        print("Sorry, unable to access the calendar")
    
    # try/except statement to access the calendar, allowing for a program break
    # if a problem is found
    try:
        bookings_calendar = build('calendar', 'v3', credentials=SCOPED_CREDS)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = bookings_calendar.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


# calendar = service.calendars().get(calendarId='primary').execute()

# print calendar['summary']

# ask for username and password to be entered
def login():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

# open the user_login secure file in 'read' and check whether
# credentials are accurate

    with open("user_login.txt", "r") as file:
        for line in file:
            valid_username, correct_password = line.strip().split(":")
            if username == valid_username and password == correct_password:
                print("Login successful. Welcome to your booking system!")
                return
            else:
                print("Invalid username or password, please try again")
            # this will need changing to a while loop at some point    

def choose_action():
    print("Please select from the following options by typing the number:")
    print("1. Place a booking")
    print("2. Find a booking")
    print("3. Cancel a booking")
    print("4. Enter a staff working pattern\n")
    choice = input("Selection: \n")
    if choice == "1":
        place_booking()
    else:
        print("Function under construction")

def phone_valid(client_phone):
    phone_entry = (str.isdigit, client_phone)
    if len(phone_entry) == 10:
        return
    else:
        print("Invalid phone number. Please check and enter a 10-digit phone number.\n")
        phone_entry = (str.isdigit, client_phone)
        if len(phone_entry) == 10:
            return
        else:
            print("Unable to place booking at this time")
            choose_action()


def place_booking():
    print("Does the client have a preferred artist? 1=Kev, 2=Bev, 3=no preference")
    artist = input("Artist selection: \n")
    # check validity of input and ask again if issue found
    print("Finding the next available date...")
    # need to add the code here to link to the calendar and check dates
    print("This date is available!")
    client_name = input("Please enter client name: \n")
    # check validity of input and ask again if issue found
    age_check = input("Please confirm client is 18 years old or older (y/n)\n")
    # check validity of input and ask again if issue found
    client_phone = input("Please enter client phone number: \n")
    phone_valid(client_phone)
    length = input("Is the tattoo a full or half day? ('full'/'half')\n")
    # check validity of input and ask again if issue found
    waiting_list = input("Would the client like to join the waiting list? (y/n)\n")
    # check validity of input and ask again if issue found
    # age check and wanting to be added to waiting list are stored as a boolean values
    age_appropriate = True if age_check.lower() == 'y' else False
    waiting = True if waiting_list.lower() == 'y' else False

    if age_appropriate == False:
        print("Unable to place booking")
        return
    else:
        # store client info as a dictionary (to be stored against the booking date)
        client_details = {
            'name': client_name,
            'phone': client_phone,
            'length': length,
            'waiting': waiting
        }

    print(client_details)

def main():
    #login()
    obtain_calendar()
    choose_action()

main()