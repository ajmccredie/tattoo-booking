
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Calendar access code from Google Workspace:
from __future__ import print_function

import datetime
import os.path
# import pandas to handle the date/time information 
# (suggested from medium.com/swlh/convert-any-dates-in-spreadsheets
# -using-python)
import pandas as pd
import random

from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil.relativedelta import relativedelta

# If modifying these scopes, delete the file token.json.
SCOPE = [
    "https://www.googleapis.com/auth/calendar",  # Google Calendar scope
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)


def obtain_calendar():
    """Shows basic usage of the Google Calendar API. 
    This code is an adapted mix of code from google 
    Workspace (Python for developers)
    and CI's Love-Sandwiches.
    Prints the start and name of the next 10 events on the 
    user's calendar.
    """
    # try/except statement to access the calendar, allowing for a program break
    # if a problem is found
    try:
        bookings_calendar = build('calendar', 'v3', credentials=SCOPED_CREDS)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events:')
        artists = ['Kev', 'Bev']
        all_events = []
        for artist in artists:
            events_result = bookings_calendar.events().list(calendarId='primary', timeMin=now, singleEvents=True).execute()
            events = events_result.get('items', [])
            if not events:
                print('No upcoming events found.')
                continue
            artist_events = []
            for event in events:
                event_summary = event.get('summary', '')
                event_description = event.get('description', '')
                event_start = event['start'].get('dateTime', event['start'].get('date'))
                if artist in event_summary:
                    if 'T' in event_start:
                        event_start_details = datetime.datetime.strptime(event_start, "%Y-%m-%dT%H:%M:%SZ").date()       
                    else:
                        event_start_details = datetime.datetime.strptime(event_start, "%Y-%m-%d").date()
                    artist_events.append((event_start_details, event_summary, event_description))  
            all_events.extend(artist_events)
        # order any events found chronologically using code inspired from https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list#:~:text=Method%201%3A%20Using%20sort()%20and%20lambda%20functions&text=Use%20the%20import%20keyword%2C%20to,has%20a%20module%20called%20datetime).&text=Sort%20the%20list%20of%20dates,argument%20as%20the%20lambda%20function.
        # sorting the tuple from https://docs.python.org/3/howto/sorting.html
        all_events.sort(key=lambda x: (x[0], x[1]))
        # Prints the start and name of the next 10 events
        for event_start_details, event_summary, event_description in all_events[:10]:
            print(f"{event_start_details}: {event_summary}: {event_description}.")

        search_calendar = input("Do you wish to search the calendar for a particular booking? y/n\n")
        search_calendar = search_calendar.strip().lower()
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
        choice = input("Selection: \n").strip().lower()
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
            calendar_search()
    except HttpError as error:
        print('An error occurred: %s' % error)
    return        


def search_by_name(events):
    """
    User input of name used to filter search results
    """
    search_name = input("Please enter the client name:\n")
    search_name = search_name.strip()
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
    while True:
        search_artist = input("Please enter the artist name (Kev/Bev):\n")
        if search_artist in ['Kev', 'Bev']:
            break
        else:
            print("Invalid artist name. Please enter 'Kev' or 'Bev'.")
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
    username = input("Please enter your username: \n")
    password = input("Please enter your password: \n")

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
    """
    The main menu code
    """
    print("-----------------------------------------------------------")
    print("Please select from the following options by typing the number:")
    print("1. Place a booking")
    print("2. Find a booking")
    print("3. Cancel a booking")
    print("4. Exit the system and logout\n")
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
        confirm_logout = input("Are you sure you wish to exit the system? y/n\n")
        if confirm_logout.lower() == 'y':
            exit()
        else:
            choose_action()
    else:
        print("\nInvalid function choice. Please select a number between 1 and 4.")
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


def ask_artist_preference_for_deletion():
    """
    Determine, vadildate and return the preferred artist
    """
    while True:
        print("Which artist? 1=Kev, 2=Bev")
        artist_input = input("Artist selection: \n").strip()
        # check validity of input and ask again if issue found
        if artist_input in ['1', '2']:
            if artist_input == '1':
                return "Kev"
            elif artist_input == '2':
                return "Bev"
        else:
            print("Invalid input. Please enter 1 or 2 to choose between (1)Kev and (2)Bev.")


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
            else:
                continue
    # Check if anyone/both is free and return information to allow the booking to continue
    if len(busy_artists) == 0:
        return None
    elif len(busy_artists) == 1:
        return busy_artists[0]
    else:
        print("Neither artist busy on date selected.")
        return random.choice(busy_artists)


def calendar_check(date_request, artist):
    """
    Checks the calendar for the date selected and the artist selected
    Returns whether that date is free, the next available date with that artist
    And whether not the other artist is free on the date selected.
    """
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

        # check that the requested date is within a 5 month window from today's date to prevent bookings beyond the scope
        five_months_time = (datetime.datetime.now() + relativedelta(months=5)).date()
        requested_date = datetime.datetime.strptime(date_request, "%Y-%m-%d").date()
        if requested_date > five_months_time:
            print("Error: The date requested is beyond the booking window of 5 months.\nReturning you to the main menu...")
            choose_action()
            return
        elif requested_date < datetime.datetime.now().date():
            print("Error: The date requested is in the past.\nReturning you to the main menu...")
            choose_action()
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

        # Determines the next available date for both artists
        # set a default to be returned
        next_date_kev = None
        next_date_bev = None
        today = datetime.date.today()
        current_date = datetime.date.today()
        
        # find all the dates without events
        completely_free_dates = []
        while True:
            date_info = current_date.isoformat()
            event_found = False
            for event in events:
                event_start = event['start'].get('dateTime', event['start'].get('date'))[0:10]
                if date_info == event_start:
                    event_found = True
                    break
            if not event_found:
                completely_free_dates.append(date_info)
            current_date += datetime.timedelta(days=1)
            if current_date > today + datetime.timedelta(days=90):
                break

        # if a booking is found on that date, the nature of the booking needs to be found
        for event in events:
            summary = event.get('summary', '')
            booked_artist = summary[12:15]
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            # Compare to requested date (assuming every booking is a full day at this point)
            if date_request == start_time:
                if artist == booked_artist:
                    date_available = False
                else:
                    continue          
            earliest_totally_free_date = completely_free_dates[0]
                
            if not booked_artist == "Kev" and not next_date_kev:
                next_date_k = event['start'].get('dateTime', event['start'].get('date'))[0:10]
                if earliest_totally_free_date < next_date_k:
                    next_date_kev = earliest_totally_free_date
                else:
                    next_date_kev = next_date_k               
            if not booked_artist == "Bev" and not next_date_bev:
                next_date_b = event['start'].get('dateTime', event['start'].get('date'))[0:10]
                if earliest_totally_free_date < next_date_b:
                    next_date_bev = earliest_totally_free_date
                else:
                    next_date_bev = next_date_b
        return date_available, next_date_kev, next_date_bev, assigned_artist

    except HttpError as error:
        print('An error occurred: %s' % error)


def add_to_calendar(client_details):
    """
    Brings in the access code from obtain_calendar and allows an event to be written
    """
    # try/except statement to access the calendar, allowing for a program break
    # if a problem is found
    try:
        bookings_calendar = build('calendar', 'v3', credentials=SCOPED_CREDS)

        # Call the Calendar API
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
        return event
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
    if date_available is False:
        print("This date is unavailable, please select another date/artist (next available shown): \n")
    else:
        print("The date you selected is free and will be used in the booking.\n-------\nFor information, the next available dates are also shown:")
    print(f"The next available date for Kev is:  {kev_next_date}")
    print(f"The next available date for Bev is:  {bev_next_date}")
    print("-------")
    # need to add the code here to link to the calendar and check dates
    while date_available is False:
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
        print(f"Your date is confirmed as {date_input}")
        print(f"Your artist is confirmed as {assigned_artist}")
    
    # once a date for the booking is found, the rest of the details are obtained
    # input the client name
    while True:
        client_name = input("Please enter client name (no spaces or non-alphabetical characters please): \n")
        if client_name.isalpha():
            break
        else:
            print("Invalid input. Please enter a client name with alphabetical characters only.")
    # check the client age (but will not break booking until later)
    while True:
        age_check = input("Please confirm client is 18 years old or older y/n\n")
        if age_check == 'y' or 'n':
            if age_check == 'n':
                continue_anyway = input("Booking will not be able to go ahead, do you wish to continue anyway? y/n\n")
                while True:
                    if continue_anyway == 'y' or 'n':
                        if continue_anyway == 'y':
                            break
                        else:
                            print("Returning to main menu...")
                            choose_action()
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    # phone number entry
    client_phone = input("Please enter client phone number: \n")
    validated_phone = phone_valid(client_phone)
    if validated_phone:
        print("Valid phone number: ", validated_phone)
    while True:
        length = input("Is the tattoo a full or half day? ('full'/'half')\n").lower()
        if length == 'full' or length == 'half':
            break
        else:
            print("Invalid input. Please enter 'full' or 'half'.")    
    date_and_time = convert_date_time_info(length, date_input, time_input)
    start = date_and_time[0]
    end = date_and_time[1]
    
    while True:
        waiting_list = input("Would the client like to join the waiting list? y/n\n")
        if waiting_list == 'y' or 'no':
            break
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    # check validity of input and ask again if issue found
    # age check and wanting to be added to waiting list are stored as a boolean values
    age_appropriate = True if age_check.lower() == 'y' else False
    waiting = True if waiting_list.lower() == 'y' else False

    if age_appropriate is False:
        print("Unable to place booking, clients must be aged 18 or older. Returning to main booking programme...")
        choose_action()
        return
    else:
        # store client info as a dictionary (to be stored against the booking date)
        client_details = {
            'artist': assigned_artist,
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
            while True:
                book_another = input("Client booking confirmed.\n Do you wish to continue using the system? y/n\n")
                if book_another == 'y' or 'no':
                    if book_another.lower() == 'y':
                        print("Returning to the main menu\n")   
                        choose_action()
                    else:
                        logout_confirm = input("Are you sure you wish to logout of the system? y/n\n")
                        if logout_confirm == 'y':
                            exit()
                        else:
                            print("Returning to the main menu\n")   
                            choose_action()
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        else:
            print("Please restart the booking procedure")
            choose_action()
            return


def waiting_list_view(events, matched_events):
    """
    Brings up the next 5 clients on the waiting list for the same artist booked on later dates, and displays them 
    with phone numbers and tattoo lengths.
    There is an option to then replace the deleted booking with the first one to confirm on the phone they want the
    earlier slot
    """
    print(f"The booking which is being removed is {matched_events[0]['summary'], matched_events[0]['description']}")
    removed_date = datetime.datetime.strptime(matched_events[0]['start']['dateTime'], "%Y-%m-%dT%H:%M:%S%z").date()
    removed_artist = matched_events[0]['summary'][12:15]
    print(removed_artist)
    waiting_list_clients = []
    # if a booking is found on that date, the nature of the booking needs to be found
    for event in events:
        summary = event.get('summary', '')
        booked_artist = summary[12:15]
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        start_hour = event['start'].get('dateTime', event['start'].get('time'))[11:13]
        end_time = event['end'].get('dateTime', event['end'].get('time'))[11:13]
        length = int(end_time) - int(start_hour)
        if length == 7:
            tattoo_length = "full day"
        else:
            tattoo_length = "half day"
        event_date = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z").date()
        description = event.get('description','')
        description_split = description.split()
        waiting_boolean = description_split[-1]
        if waiting_boolean == "True" and event_date > removed_date and removed_artist == booked_artist:
            client_name = description_split[0]
            client_phone = description_split[1]
            client_tattoo_length = tattoo_length
            waiting = True
            waiting_list_clients.append({
                'artist': booked_artist,
                'name': client_name,
                'phone': client_phone,
                'tattoo_length': client_tattoo_length,
                'start': event_date,
                'waiting': waiting
            })            
    print("Here are the next (upto) 5 clients on the waiting list for the same artist:")
    index = 1
    for client in waiting_list_clients[0:5]:
        print(f"{index}. Name: {client['name']} Phone: {client['phone']} Tattoo length: {client['tattoo_length']} Date: {client['start']}")
        index += 1
    select_client_for_replacement = input("Select a client from the waiting list to take the cancelled slot by entering the index number (1-5).\n(Select any other key to return to the main menu)\n")
    try:
        select_index = int(select_client_for_replacement)
        if 1<= select_index <= min(len(waiting_list_clients), 5):
            selected_client = waiting_list_clients[select_index - 1]
            print(selected_client)
            event_set_to_move = event
            print(f"You've selected: Name: {selected_client['name']} Phone: {selected_client['phone']} \nThis booking will be moved into the free slot.")
            selected_client["start"] = removed_date.strftime('%Y-%m-%d')
            selected_client["end"] = removed_date.strftime('%Y-%m-%d') 
            event_id = event_set_to_move['id']
            return selected_client, event_id
        else:
            print("Invalid selection. No further changes have been made.")
    except ValueError:
        print("Returning to main menu...")
        choose_action() 


def cancel_booking():
    """
    A series of validated user inputs to determine, check and delete the unwanted booking
    """
    print("Please provide answers to the following questions to find the booking: ")
    artist = ask_artist_preference_for_deletion()
    print(artist)
    summary = f"Tattoo with {artist}"
    client_name = input("Please provide the name of the person booked in: \n")
    date_search = input("Please enter the date of the booking (YYYY-MM-DD): \n")
    # search function for appropriate events - use of q query and search parameters adapted from 
    # https://www.jayasekara.blog/2021/07/how-to-search-google-calendar-events-using-python.html

    try:
        # access the calendar in order to search
        bookings_calendar = build('calendar', 'v3', credentials=SCOPED_CREDS)
        events_result = bookings_calendar.events().list(calendarId='primary').execute()
        events = events_result.get('items', [])
        
        # filter all the results obtained to just the ones matching the search criteria
        matched_events = []
        for event in events:
            event_summary = event.get('summary', '')
            start_time = event['start'].get('dateTime', event['start'].get('date'))[0:10]
            event_client_name = event.get('description', '').split(', ')[0]
            if summary in event_summary and date_search == start_time and client_name == event_client_name:
                matched_events.append(event)
                print(f"The following booking(s) matching your description has been found: \n", start_time,": ", event['summary'],".", event['description'],".")
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
                        while True:
                            waiting_list_request = input("Do you wish to see the next few clients on the waiting list? y/n\n")
                            if waiting_list_request == 'n':
                                print("Returning to main menu....\n")
                                choose_action()
                                break
                            elif waiting_list_request == 'y':
                                selected_client, event_id = waiting_list_view(events, matched_events)
                                print("Waiting list client has been moved")
                                tattoo_length_string = selected_client.get("tattoo_length", "")
                                length = tattoo_length_string[0:4]
                                date_request = selected_client["start"]
                                time_input = 11
                                selected_client["start"], selected_client["end"] = convert_date_time_info(length, date_request, time_input)
                                # ensure the details for the replacement_client are formatted for the routine
                                replacement_client = {
                                    'artist': selected_client['artist'],
                                    'name': selected_client['name'].replace(',', ''),
                                    'phone': selected_client['phone'].replace(',', ''),
                                    'start': selected_client['start'],
                                    'end': selected_client['end'],
                                    'length': length,
                                    'waiting': selected_client['waiting']
                                }
                                updated_event = add_to_calendar(replacement_client)
                                print(f"Here are the new details for that booking: {updated_event['start']}: {updated_event['summary']}, {updated_event['description']}")
                                print("Deleting the altered booking")
                                bookings_calendar.events().delete(calendarId='primary', eventId=event_id).execute()
                                print("Returning to main menu...")
                                choose_action()
                                break
                            else:
                                print("Invalid input, please enter 'y' or 'n'.")                            
                else:
                    print("Invalid command, unable to complete booking deletion.\n")
                    choose_action()
                    break
        else:
            print("No matching bookings were found, please check your search criteria.\nReturning to main menu...")
            choose_action()
    except HttpError as error:
        print('An error occurred: %s' % error)


def main():
    #login()
    #obtain_calendar()
    choose_action()

# run the main programme on launch
main()