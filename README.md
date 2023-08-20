# Eternal Ink Tattoo Studio – Booking System
## Introduction
This booking system was created as a purely Python3 based portfolio project. It uses Python3, a variety of libraries and Google API to link to a calendar to make, view and delete bookings for the two fictional artists who work at the fictional studio created for an earlier project. The system runs in the Code Institute mock terminal in Heroku.
 ![View of deployment to Heroku mock terminal](/workspace/tattoo-booking/README_images/deployment_view.png "Heroku mock terminal view")

#### View live project here: https://eternal-ink-tattoo-booking-c7148e7ee7d3.herokuapp.com/

## User Experience
### User Goals
The system is designed for use by the studio employees and requires an admin password to enter the site to place, view, or delete bookings. 

The system navigates to a main booking menu and saves the bookings onto a Google calendar I created in my Google Dev account, which exists in theory for the fictional tattoo studio to use and access. If the calendar cannot be viewed directly, the user can still access all the bookings using the search function.

The system is quick enough to use while a client is on the phone, or could be used with information provided from text, email or web queries.

The system provides information to be able to contact the client, as well as storing some things about the booking, including age verification and whether the tattoos booked will be full or part days.

Additionally, the user can put clients on the waiting list, which can be called up when a booking is deleted, allowing the studio to contact other clients to fill the slot. 

### Developer Goals
I want to build a system that is easy to use by any of the employees, standardises data input and centralises where the information is stored, in order to streamline the activities of the company and speed up the booking and search processes.

## Design
The system navigates around a main menu with three distinct functions: make, view, and delete bookings. A large amount of user data is required and these inputs are validated as the system is used. 

### Logic flowcharts
/workspace/tattoo-booking/README_images/tattoo_main_booking_menu_logic.png

/workspace/tattoo-booking/README_images/place_tattoo_booking_logic.png

/workspace/tattoo-booking/README_images/search_calendar_logic.png

/workspace/tattoo-booking/README_images/cancel_and_move_bookings_logic.png

### Features
**Booking** – the user selects the artist and the date, but the option of ‘no preference’ for the artist is given. This allows the system to cross-reference to the date, check to see if either or both artists are free and then allocate the slot to either the free artist (or in the case of both being available, randomly selects one of them). This also returns the next date available for both artists, which may be of use if the client potentially wanted to book earlier. 

The booking period is limited to a 5 month window, and attempts to book appointments in the past are blocked.

**Viewing/searching** – the next ten appointments are shown first, which allows a good overview of the upcoming days, but without being overwhelming. The system can the be searched directly by date, artist or client name. Each of these return all matching results. This could be useful for the artists to check their bookings,  or if a client makes contact to check the details of their booking. It could also be used ahead of a formal booking process to check whether the proposed dates are free.

**Deleting** – the user needs to input three bits of information, all of which must match in order to find the booking before deletion. This it to prevent accidental deletion of information and bookings.

The option of bringing up the next people on the waiting list to contact and potentially fill the deleted slot is given here. Cancelled bookings cause lost revenue for tattoo studios, but having a useable waiting list should minimise these issues. Changes to bookings are confirmed.

## Future Features
The ability to add staff working patterns and known holidays would make this system more useable in the real world. At the moment if a staff member wanted to prevent a booking on a day, they would have to effectively book the slot to themselves. This would mean the system would not see the day as available, however it would be time consuming and cause a general need for erroneous data entry for some of the questions.
Adding a routine which was able to accept the artist name and then put the description as ‘booked leave’ or ‘not available’ (rather than requiring all the other inputs) would be a way to achieve this. 

Advanced bookings making use of the ‘length’ of the tattoos and allowing more sessions to be grouped together on days would allow for a potentially greater income for the studio artists. This could be achieved by comparing the required length of a new booking on a date to the length of any existing ones on that date. 

### Creating the Calendar
In order to not interfere with my general calendar and so that I can play with other APIs in the future, I set up a new account with Google for development activities.
### API Credentials:
To enable access from the project to Google Calendar, credentials must be created and provided.
*	Navigate to the Google Cloud Platform
*	Click "Select a project"
*	Select "New Project".
*	Enter the project name.
*	Click "Create"
*	From the project dashboard, select "APIs and services"
*	Then select "Library"
*	Search for Google Drive API and enable it.
*	Click "Create Credentials".-
*	Click "Google Drive API" from the list.
*	Select "Application data" from the first set of  buttons.
*	Select "No " from the second set of buttons.
*	Click "Done" 
*	Enter name and description for the service account details.
*	Select a role of "Editor" from the options available.
*	Click "Done" to create the service account.
*	Click on the newly created service account on the credentials page.
*	Select "Keys" from the top menu bar.
*	Select "Create new key" from the "Add Key" menu.
*	Select "JSON" and click "Create"
*	The JSON file will be downloaded to your computer. 
*	The contents need to be copied into a creds.json file within the repository. Make sure to add this file to the .gitignore file (because it is sensitive data).

## Technologies Used
### Languages
Python3

### Python Packages
**Datetime**: used to return the full date by providing classes for manipulating dates and times. It is crucial for entering, tracking and displaying dates in a user-friendly format.<br>
**Os.path**: a submodule of ‘os’ in Python, used for common file and directory path manipulation. It is essential for determining whether necessary files are available for authentication and access.<br>
**Random**: a module that provides functions to generate random numbers and make random selections. It is used for when the user selects ‘no preference’ to distribute potential bookings fairly. <br>
**Dateutil.relativedelta relativedelta**: part of the ‘dateutil’ library, which provides further extensions to ‘datetime’. This allows arithmetic operations on dates. It is specifically used to set the 5 month booking window. <br>
**from __future__ import print_function** - Handles backwards compatibility of print statements.<br>

**Google API and related modules**: modules used to specifically facilitate interactions with the Google Calendar: 
 - from google.auth.transport.requests import Request - Handles authentication requests and responses
 - from google.oauth2.service_account import Credentials – Represents OAuth2 credentials for a service account
 - from google_auth_oauthlib.flow import InstalledAppFlow – Helps with the OAuth2 authorisation flow
 - from googleapiclient.discovery import build – Creates a service object for interacting with Google APIs
 - from googleapiclient.errors import HttpError - Handles HTTP errors that may occur during API requests

### Frameworks, Libraries and Programmes Used:
* GitHub
* Gitpod
* Google Cloud
* Google Drive API
* Google Calendar
* Heroku
* PEP8

## Testing
### Functional Testing

| Test	| Pass? |
|-------|-------|
| Login works when correct password and username given	| Yes |
| Main menu loads |	Yes |
|The menu navigates to where the user requests |	Yes |
| Incorrect inputs to request are handled appropriately |	Yes |
| Artist can be selected from the two names or as ‘No preference’ |	Yes |
| ‘No preference’ correctly searches the date provided and returns ‘none available’, which one is available or ‘both available’ (then selecting one at random), depending on what the search provides. |	Yes |
| Dates can only be entered in a 5 month window from today.	| Yes |
| Client name input validated as alpha and only one word (names and surnames need to be entered as follows: AjMcCredie. No spaces are allowed)	| Yes |
| Client phone number validated |	Yes |
| Client age validated and option given to return to main menu if client less than 18 years old	| Yes |
| Client choice of tattoo lengths validated and stored correctly | Yes |
| Client choice to join waiting list validated and stored correctly	| Yes |
| Summary of booking printed to terminal for user to check | Yes |
| Booking saves to calendar when instructed |	Yes |
| Programme navigates back to main booking menu when instructed at the end of the booking	| Yes |
| Next ten bookings are printed to the screen when ‘Find a booking’ is selected from the main menu	| Yes |
| Correct navigation from validated input for whether to search the calendar for a specific booking | Yes |
| Correct navigation from validated input to search by client name, artist name or date	| Yes |
| System finds and displays all relevant bookings found to the terminal	| Yes |
| Programme navigates back to main booking menu when instructed at the end of the searches	| Yes |
| Cancel booking accepts validated artist input |	Yes |
| Client name can be entered, but this is not validated (the system is not storing this information, simply using it as a search criteria and will be rejected if no direct match exists anyway) |	Yes |
| Valid date entered and used for search (user may easily mis-type this)	| Yes |
| System returns any matches found. |	Yes |
| No matches returns user to main menu	| Yes |
| User confirms whether to delete a match	| Yes |
| If user does not wish to delete the match, programme returns to main menu	| Yes |
| If users elects to delete the match, confirmation of this is given |	Yes |
| System interprets user input for whether or not to display waiting list correctly |	Yes |
| Choosing no waiting list navigates back to main menu	| Yes |
| Choosing waiting list displays up to next 5 clients identified for the same artist with ‘waiting list’ showing as ‘True’	| Yes |
| System interprets validated user input for whether to replace the deleted booking with one from the list (or returns to main menu on demand) | Yes |
| System confirms altered booking and returns to main menu	| Yes |

### Validator Testing
PEP8 Online returned a number of issues with line length. The whole programme was taken through a routine ‘black’ to allow a greater degree of compliance.

## Bugs and Issues
### Solved Bugs
Many small and annoying bugs were caused by minor typos and fixed fairly easily. Below is a report of the more major bugs which took more time and brain power to resolve:
1.	Code returning a statement of ‘no matching bookings’, but also returning matching bookings in a list. This was fixed by reviewing and changing a level of indentation in the code.
2.	Initially setting up the ‘No preference’ code for artist allocation caused some bother, until I realised that I had (right from the start of writing the code) marked both artists as ‘busy’ automatically for the dates. This was easily rectified once I finally realised my mistake.
3.	There was an issue where the code was only displaying the first event multiple times instead of looping through all events. This was resolved by adjusting the indentation of the event display loop and making sure the events were stored properly in the all_events list.
4.	Erroneous free dates and incorrect information regarding who was free was an issue near the start. This was again caused by accidentally overwriting data, and fixed by creating and storing to new variable names on appropriate indentation levels.
5.	Initially, the event dates were not being properly converted to the correct datetime format, which affected the ability to display the events chronologically. This was fixed by ensuring consistent datetime conversion for event start dates.
6.	Despite fixing the conversion for datetime, there was still an issue where the events were not being sorted chronologically for the event dates. This was fixed by adjusting the sorting key, and the order in which the data was saved to the tuples, and the logic to consider the event start gate as the primary sorting key. 
7.	The sorted dates list was then not allowing both artists’ bookings to be displayed on a duplicate date. This was resolved by ensuring that events with the same date are stored as separate items in the all_events list.
8.	There was an issue with SCOPED_CREDS when the project was deployed to Heroku (which had not been an issue when running the code in Gitpod). This was resolved in stages by changing the file name of the creds.json file and then making the CREDS and SCOPED_CREDS global variables in the code.
9.	Issues were encountered when trying to change the date of an existing booking. The function suggested from the Google developers information did not appear to do the job required, so instead a new booking was made as replacement and the previous one deleted (which has the same over all effect, but felt like a less neat solution).
10.	The manner in which the username and password were stored and retrieved also needed to be altered for the deployment to Heroku. These were changed from being read from a txt file to being called directly from the Config Vars in Heroku.

### Unsolved Bugs
The link provided to confirm the booking within the window (which should lead to the google calendar) has never worked for some reason. I have conducted extensive research into available information, but this has not returned anything useable. I have removed the links from the confirmations of fresh bookings and updated bookings.

## Deployment
### Cloning this project:
1.	Go to the main repository page on GitHub.com
2.	Select the ‘Code’ button above the list of files
3.	Choose from https, SSH or GitHub CLI
4.	Click the clipboard icon to copy the URL
5.	Open your terminal
6.	Navigate to the directory where you want to place the cloned project
7.	Type ‘git clone’ in the terminal and then paste the URL copied in step 4.
### Python project deployment in Heroku:
1.	Ensure that any prompts for data entry have a new line after them (“\n”)
2.	Use the command pip3 freeze > requirements.txt (to save all the requirements for the project in a txt file)
3.	Login to Heroku account and select “Create a New App”.
4.	Give the new app a unique project name, and select the correct region. Then confirm you wish to create the app.
5.	On the new screen for the app, click on the “settings” tab.
6.	Go to the “Config Vars” section (to set up the Environment Variables), to allow the app access to files which are kept hidden from the GitHub repository.
7.	Firstly add a credential called PORT with the value of 8000. Next add the CREDS file (and copy and paste all the details from the file straight into the box). Next add the additional passwords, but splitting the inputs into VALID_USERNAME and CORRECT_PASSWORD.
8.	The code in the project that checks the username and password against the .txt file needs to be replaced with code to retrieve the credentials from the Config Vars: valid_username = os.environ.get(“VALID_USERNAME”) and correct_password = os.environ.get(“CORRECT_PASSWORD”).
9.	Then go to the “Buildpacks”, click “Add buildpack” and add “Python” by clicking on it. Save the changes. Then repeat the process, but adding “Nodejs” to handle the user interface. The Python Buildpack must appear at the top of the list, and can be dragged into place if not already there.
10.	Then click on the “Deploy” tab from the main tabs list at the top. This leads to the deploy section. Select “GitHub” as the “Deployment Method” and then confirm to connect to GitHub. The name of the GitHub repository should be entered into the search bar and then selected once found.
11.	You can then select whether to use automatic deploys (each time a change is pushed to GitHub) or to manually control deployments.
12.	You should then have a notification that your app was successfully deployed and an option to view it.
13.	The programme will automatically run in the window and can be restarted by clicking the “Run Programme” button. It is worth testing the programme with both correct and incorrect data in order to check that it still behaves as expected.


## References and Credits

- Order any events found chronologically using code inspired from https://www.tutorialspoint.com/How-to-sort-a-Python-date-string-list#:~:text=Method%201%3A%20Using%20sort()%20and%20lambda%20functions&text=Use%20the%20import%20keyword%2C%20to,has%20a%20module%20called%20datetime).&text=Sort%20the%20list%20of%20dates,argument%20as%20the%20lambda%20function.

- Sorting the tuple from https://docs.python.org/3/howto/sorting.html

- Search function for appropriate events - use of q query and search parameters adapted from https://www.jayasekara.blog/2021/07/how-to-search-google-calendar-events-using-python.html

- Extensive advice and guidance and odd code snippets from developers.google.com

- Encouragement and guidance from Code Institute Mentor Mitko Bachvarov.

- Extensive experience in Python from before joining Code Institute from videos on SkillShare (mostly Tony Staunton).

- Help from the Tutor Support team from Code Institute with a number of deployment issues.

