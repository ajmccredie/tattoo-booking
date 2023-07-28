
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Calendar access code from Google Workspace:
from __future__ import print_function

import datetime
import os.path
# import pandas to handle the date/time information (suggested from medium.com/swlh/convert-any-dates-in-spreadsheets-using-python)
import pandas as pd

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
    This code is an adapted mix of code from google Workspace (Python for developers)
    and CI's Love-Sandwiches.
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
            print(start,":", event['summary'],".", event['description'],".")

    except HttpError as error:
        print('An error occurred: %s' % error)

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
    elif choice == "3":
        cancel_booking()
    elif choice == "2":
        print("Function under construction")
    elif choice == "4":
        print("Function under construction")
    else:
        print("Invalid function choice, terminating programme.")

def ask_artist_preference():
    """
    Determine, vadildate and return the preferred artist
    """
    while True:
        print("Does the client have a preferred artist? 1=Kev, 2=Bev, 3=no preference")
        artist_input = input("Artist selection: \n")
        # check validity of input and ask again if issue found
        if artist_input in ['1', '2', '3']:
            if artist_input == '1':
                return "Kev"
            elif artist_input == '2':
                return "Bev"
            else:
                return "No preference"
        else:
            print("Invalid input. Please enter 1, 2 or 3.")
            continue

def phone_valid(client_phone):
    """
    Check the phone number provided is a number and has 10 digits.
    """
    while True:
        phone_entry = client_phone.replace(" ", "")
        if phone_entry.isdigit() and len(phone_entry) == 10:
            return phone_entry
        else:
            print("Invalid phone number. Please check and enter a 10-digit phone number:\n")
            client_phone = input("Please entter client phone number: \n")
    else:
        print("Unable to place booking at this time")
        choose_action()

def convert_date_format(date_str):
    """
    Code adapted from https://medium.com/swlh/convert-any-dates-in-
    spreadsheets-using-python-56cd7549cee7 to make the inputs compatible 
    with the ones the calendar will expect
    """
    return pd.to_datetime(date_str).strftime("%Y-%m-%d")


def convert_date_time_info(length, date_input, time_input):
    """
    Begin adaptation of data entry to convert for the calendar entry
    """
    start = f"{date_input} {time_input}:00"
    if length == 'full':
        duration  = 7
        ending = time_input + duration
    elif length == 'half':
        duration = 4
        ending = time_input + duration
    else:
        print("Sorry, duration invalid, restarting booking process...")
        return
    end = f"{date_input} {ending}:00"
    return (start, end)

def add_to_calendar(client_details):
    """
    Brings in the access code from obtain_calendar and allows an event to be written
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
        start_time = datetime.datetime.strptime(client_details['start'], '%Y-%m-%d %H:%M').isoformat()
        end_time = datetime.datetime.strptime(client_details['end'], '%Y-%m-%d %H:%M').isoformat()

        event = {
            'summary': f"Tattoo with {client_details['artist']}",
            'location': 'Eternal Ink Studios',
            'description': f"{client_details['name']}, {client_details['phone']}, Waiting list? {client_details['waiting']}",
            'start': {
                'dateTime': start_time,
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'Europe/London'
            },
        }

        # insert the event into the calendar
        event = bookings_calendar.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % event.get('htmlLink'))
    except HttpError as error:
        print('An error occurred: %s' % error)

def place_booking():
    artist = ask_artist_preference()
    print(artist)
    # print("Finding the next available date...")
    # need to add the code here to link to the calendar and check dates
    date_input = input("Please enter the date for booking (YYYY-MM-DD): ")
    # set default start time to 11am
    time_input = 11
    print("This date is available!")
    client_name = input("Please enter client name: \n")
    # check validity of input and ask again if issue found
    age_check = input("Please confirm client is 18 years old or older (y/n)\n")
    # check validity of input and ask again if issue found
    client_phone = input("Please enter client phone number: \n")
    validated_phone = phone_valid(client_phone)
    if validated_phone:
        print("Valid phone number: ", validated_phone)
    length = input("Is the tattoo a full or half day? ('full'/'half')\n")
    # check validity of input and ask again if issue found
    date_and_time = convert_date_time_info(length, date_input, time_input)
    start = date_and_time[0]
    end = date_and_time[1]
    
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
            'artist': artist,
            'name': client_name,
            'phone': client_phone,
            'start': start,
            'end': end,
            'length': length,
            'waiting': waiting
        }

        print(f"Please check through the information provided: ", client_details)
        confirm_booking = input("Are all the details provided correct? y/n\n")
        if confirm_booking.lower() == 'y':
            # access the calendar and store the details
            add_to_calendar(client_details)
            book_another = input("Client booking confirmed.\n Do you wish to continue using the system? ('y'/'n')\n")
            if book_another.lower() == 'y':
                choose_action()
            else:
                return
        else:
            print("Please restart the booking procedure")
            choose_action()
            return



def cancel_booking():
    print("Please provide answers to the following questions to find the booking: ")
    artist = ask_artist_preference()
    print(artist)
    summary = f"Tattoo with {artist}"
    client_name = input("Please provide the name of the person booked in: \n")
    description = f"{client_name}"
    date_search = input("Please enter the date of the booking (YYYY-MM-DD): \n")
    # search function for appropriate events - use of q query and search parameters adapted from 
    # https://www.jayasekara.blog/2021/07/how-to-search-google-calendar-events-using-python.html
    if os.path.exists('eicreds.json'):
        CREDS = Credentials.from_service_account_file('eicreds.json')
        SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    else:
        print("Sorry, unable to access the calendar")
    
    try:
        # access the calendar in order to search
        bookings_calendar = build('calendar', 'v3', credentials=SCOPED_CREDS)
        events_result = bookings_calendar.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])
        
        # filter all the results obtained to just the ones matching the search criteria
        matched_events = []
        for event in events:
            if summary in event.get('summary', ''):
                matched_events.append(event)
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"The following booking(s) matching your description has been found: ", start,":", event['summary'],".", event['description'],".")
                confirm_action = input("Do you wish to delete the booking(s)? ('y'/'n')\n")
                if confirm_action.lower() == 'n':
                    print("Booking deletion cancelled")
                    exit()
                elif confirm_action.lower() == 'y':
                    for event in matched_events:
                        event_identifier = event['id']
                        bookings_calendar.events().delete(calendarId='primary', eventId=event_identifier).execute()
                        print("Booking deleted.")
                else:
                    print("Invalid command, unable to complete booking deletion.\n")
                    choose_action()
            else:
                print("No matching bookings found, please check your search criteria.")

    except HttpError as error:
        print('An error occurred: %s' % error)


def main():
    #login()
    obtain_calendar()
    choose_action()

# run the main programme on launch
main()