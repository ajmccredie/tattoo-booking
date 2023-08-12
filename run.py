
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Calendar access code from Google Workspace:
from __future__ import print_function

import datetime
import os.path
# import pandas to handle the date/time information (suggested from medium.com/swlh/convert-any-dates-in-spreadsheets-using-python)
import pandas as pd
import random

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
        events_result = bookings_calendar.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, ":", event['summary'], ".", event['description'], ".")

        search_calendar = input("Do you wish to search the calendar for a particular booking? y/n\n")
        if search_calendar.lower() == 'y':
            calendar_search()
        elif search_calendar.lower() == 'n':
            print("Returning to booking actions...\n")
            choose_action()
            return
        else:
            print("Invalid input. Returning to booking actions...\n")
            choose_action()
            return
    except HttpError as error:
        print('An error occurred: %s' % error)

def calendar_search():
    """
    Accesses all of the information available in the calendar in order to allow searches
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
        events_result = bookings_calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        print("Future events found. Please choose how you wish to search the calendar: ")
        print("a. By client name")
        print("b. By artist")
        print("c. By date")
        print("d. Return to main menu")
        choice = input("Selection: \n").strip()
        if choice.lower() == "a":
            name_matches = search_by_name(events)
            print("The search found the following results...")
            for name_match in name_matches:
                start = name_match['start'].get('dateTime', name_match['start'].get('date'))
                print(start, ":", name_match['summary'], ".", name_match['description'], ".")
            print("Returning to bookings menu...\n")
            choose_action()
        elif choice.lower() == "b":
            artist_matches = search_by_artist(events)
            print("The search found the following results...")
            for artist_match in artist_matches:
                start = artist_match['start'].get('dateTime', artist_match['start'].get('date'))
                print(start, ":", artist_match['summary'], ".", artist_match['description'], ".")
            print("Returning to bookings menu...\n")
            choose_action()
        elif choice.lower() == "c":
            date_matches = search_by_date(events)
            print("The search found the following results...")
            for date_match in date_matches:
                start = date_match['start'].get('dateTime', date_match['start'].get('date'))
                print(start, ":", date_match['summary'], ".", date_match['description'], ".")
            print("Returning to bookings menu...\n")
            choose_action()
        elif choice.lower() == "d":
            choose_action()
        else:
            print("Invalid input. Please try again.")
            calendar_search(events)
    except HttpError as error:
            print('An error occurred: %s' % error)
    return        


def search_by_name(events):
    """
    User input of name used to filter search results
    """
    search_name = input("Please enter the client name:\n")
    matched_by_name = []
    for event in events:
        descriptions = event.get('description', '')
        description_split = descriptions.split(', ')
        name = description_split[0]
        if name.lower() == search_name.lower():
            matched_by_name.append(event)
    return matched_by_name

def search_by_date(events):
    """
    User input of date used to filter search results
    """
    search_date_input = input("Please enter the date you wish to search(YYYY-MM-DD): \n")
    # check validity of date input
    while not date_valid(search_date_input):
        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        search_date_input = input("Please enter the date for booking (YYYY-MM-DD): \n")
    matched_by_date = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        date_string = start.split('T')
        date = date_string[0]
        # check date
        if date == search_date_input:
            matched_by_date.append(event)
    return matched_by_date

def search_by_artist(events):
    """
    User input of artist used to filter search results
    """
    search_artist = input("Please enter the artist name (Kev/Bev):\n")
    matched_by_artist = []
    for event in events:
        summaries = event.get('summary', '')
        summaries_split = summaries.split(' ')
        artist = summaries_split[2]
        if artist.lower() == search_artist.lower():
            matched_by_artist.append(event)
    return matched_by_artist


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
    print("-----------------------------------------------------------")
    print("Please select from the following options by typing the number:")
    print("1. Place a booking")
    print("2. Find a booking")
    print("3. Cancel a booking")
    print("4. Enter a staff working pattern")
    print("5. Exit the system and logout\n")
    choice = input("Selection: \n")
    if choice == "1":
        print("-----------------------------------------------------------")
        place_booking()
    elif choice == "3":
        print("-----------------------------------------------------------")
        cancel_booking()
    elif choice == "2":
        print("-----------------------------------------------------------")
        obtain_calendar()
    elif choice == "4":
        print("Function under construction")
    elif choice == '5':
        confirm_logout = input("Are you sure you wish to exit the system? y/n\n")
        if confirm_logout.lower() == 'y':
            exit()
        else:
            choose_action()
    else:
        print("\nInvalid function choice. Please select a number between 1 and 5.")
        choose_action()

def ask_artist_preference():
    """
    Determine, vadildate and return the preferred artist
    """
    while True:
        print("Which artist? 1=Kev, 2=Bev, 3=no preference")
        artist_input = input("Artist selection: \n").strip()
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
            client_phone = input("Please enter client phone number: \n")
    else:
        print("Unable to place booking at this time")
        choose_action()


def date_valid(date_str):
    """
    Check whether the user input of date meets the requirements stipulated
    """
    # Use a try/except statement in order to quickly sort valid inputs
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


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
        print("Sorry, duration invalid, please enter a valid length of 'full' or 'half'")
        choose_action()
        return
    end = f"{date_input} {ending}:00"
    return (start, end)

def assign_artist(events, date_request):
    """ 
    When the user selects there is no artist preference, the date is checked against both
    It will then return one of the following: a message that both artists are busy, assign 
    it to the free artist if only one is busy, or randomly assign one if both are free
    """
    busy_artists = ["Kev", "Bev"]
    print("Attempting to assign an artist")

    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        booked_artist = event.get('summary', '')[12:15]
        if date_request == start_time[0:10]:
            if booked_artist in busy_artists:
                busy_artists.remove(booked_artist)
                print(busy_artists)
            else:
                print("Neither artist busy on date selected.")
    # Check if anyone/both is free and return information to allow the booking to continue
    if len(busy_artists) == 0:
        return None
    elif len(busy_artists) == 1:
        return busy_artists[0]
    else:
        return random.choice(busy_artists)


def calendar_check(date_request, artist):
    """
    Checks the calendar for the date selected and the artist selected
    Returns whether that date is free, the next available date with that artist
    And whether not the other artist is free on the date selected.
    """
    # Calendar is called the same way as in other bits of calendar access code
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
        events_result = bookings_calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True).execute()
        events = events_result.get('items', [])
        if not events:
            print('The whole upcoming calendar is clear of future bookings.')
            return
        
        # set the default for the date to be 'available'
        date_available = True
        assigned_artist = None
        
        # Runs a calendar search for the given dates and artist (or assigns an artist first if user stated 'no preference')
        if artist == "No preference":
            print("You selected no preference, so checking the requested date for free artists.")
            assigned_artist = assign_artist(events, date_request)
            if assigned_artist is None:
                date_available = False
        else:
            assigned_artist = artist

        print(f"Your artist is {assigned_artist}")
        # Determines the next available date for both artists
        busy_artists = ["Kev", "Bev"]
        
        # set a default to be returned
        next_date_kev = None
        next_date_bev = None
        current_date = datetime.date.today()
        print(f"Today's date is {current_date}")

        date_completely_free = date_request not in [event['start'].get('dateTime', event['start'].get('date')) for event in events]

        # if a booking is found on that date, the nature of the booking needs to be found
        for event in events:
            summary = event.get('summary', '')
            booked_artist = summary[12:15]
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            event_date = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z").date()
            # Compare to requested date (assuming every booking is a full day at this point)
            if date_request == start_time:
                if artist == booked_artist:
                    date_available = False
                else:
                    continue
                
            if event_date >= current_date and not booked_artist == "Kev" and not next_date_kev:
                next_date_kev = event['start'].get('dateTime', event['start'].get('date'))[0:10]
               
            if event_date >= current_date and not booked_artist == "Bev" and not next_date_bev:
                next_date_bev = event['start'].get('dateTime', event['start'].get('date'))[0:10]
           
        return date_available, next_date_kev, next_date_bev, assigned_artist

    except HttpError as error:
            print('An error occurred: %s' % error)


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
    """
    A series of user input questions, validated and used to produce a client booking
    """
    # choose artist (this comes first because it will allow the calendar to be searched more effectively)
    artist = ask_artist_preference()
    # check the date the user wants
    date_input = input("Please enter the date for booking (YYYY-MM-DD): \n")
    # check validity of date input
    while not date_valid(date_input):
        print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
        date_input = input("Please enter the date for booking (YYYY-MM-DD): \n")
    # set default start time to 11am
    time_input = 11
    print("Checking the calendar...")
    date_available, kev_next_date, bev_next_date, assigned_artist = calendar_check(date_input, artist)
    if assigned_artist is not None:
        print(f"Your assigned artist for the booking is {assigned_artist}")
    if date_available == False:
        print("This date is unavailable, please select another date/artist (next available shown): \n")
    else:
        print("The date you selected is free and will be used in the booking.\n For information, the next available dates are also shown:\n")
    print(f"The next available date for Kev is:  {kev_next_date}")
    print(f"The next available date for Bev is:  {bev_next_date}")
    # need to add the code here to link to the calendar and check dates
    while date_available == False:
        print("You will need to select another date for that artist to continue your booking (press 'n' to be directed to new date input)\n")
        leave_booking = input("Do you wish to return to the main menu? y/n\n")
        if leave_booking == 'y':
            choose_action()
            break
        else:
            artist = ask_artist_preference()
            # check the date the user wants
            date_input = input("Please enter the date for booking (YYYY-MM-DD): \n")
            # check validity of date input
            while not date_valid(date_input):
                print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
                date_input = input("Please enter the date for booking (YYYY-MM-DD): \n")
            # set default start time to 11am
            time_input = 11
            print("Finding the next available date...")
            date_available = calendar_check(date_input, artist)[0]
    else:
        print("Date is available and will be used in the booking.")
        print(f"Your artist is confirmed as {artist}")
    
    # once a date for the booking is found, the rest of the details are obtained
    client_name = input("Please enter client name: \n")
    # check validity of input and ask again if issue found
    age_check = input("Please confirm client is 18 years old or older y/n\n")
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
    
    waiting_list = input("Would the client like to join the waiting list? y/n\n")
    # check validity of input and ask again if issue found
    # age check and wanting to be added to waiting list are stored as a boolean values
    age_appropriate = True if age_check.lower() == 'y' else False
    waiting = True if waiting_list.lower() == 'y' else False

    if age_appropriate == False:
        print("Unable to place booking, clients must be aged 18 or older. Returning to main booking programme...")
        choose_action()
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
            book_another = input("Client booking confirmed.\n Do you wish to continue using the system? y/n\n")
            if book_another.lower() == 'y':
                print("Returning to the main menu\n")   
                choose_action()
            else:
                logout_confirm = input("Are you sure you wish to logout of the system? y/n\n")
                if logout_confirm == 'y':
                    return
                else:
                    print("Returning to the main menu\n")   
                    choose_action()
        else:
            print("Please restart the booking procedure")
            choose_action()
            return


def cancel_booking():
    """
    A series of validated user inputs to determine, check and delete the unwanted booking
    """
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
                confirm_action = input("Do you wish to delete the booking(s)? y/n\n")
                if confirm_action.lower() == 'n':
                    print("Booking deletion cancelled, returning to main menu.\n")
                    choose_action()
                elif confirm_action.lower() == 'y':
                    for event in matched_events:
                        event_identifier = event['id']
                        bookings_calendar.events().delete(calendarId='primary', eventId=event_identifier).execute()
                        print("Booking deleted.")
                        # question user here as to whether they want to see the next name on the waiting list?
                        print("Returning to main menu....\n")
                        choose_action()
                else:
                    print("Invalid command, unable to complete booking deletion.\n")
                    choose_action()
            else:
                print("No matching bookings found, please check your search criteria.")

    except HttpError as error:
        print('An error occurred: %s' % error)


def main():
    #login()
    #obtain_calendar()
    choose_action()

# run the main programme on launch
main()