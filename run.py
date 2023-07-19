
# Write your code to expect a terminal of 80 characters wide and 24 rows high

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
    print("Please select from the following options by typing the number: \n")
    print("1. Place a booking")
    print("2. Find a booking")
    print("3. Cancel a booking")
    print("4. Enter a staff working pattern")
    choice = input("Selection: \n")
    if choice == "1":
        place_booking()
    else:
        print("Function under construction")

def place_booking():
    print("Does the client have a preferred artist? 1=Kev, 2=Bev, 3=no preference")
    artist = input("Artist selection: \n")
    print("Finding the next available date...")
    # need to add the code here to link to the calendar and check dates
    print("This date is available!")
    client_name = input("Please enter client name: \n")
    client_phone = input("Please enter client phone number: \n")
    length = input("Is the tattoo a full or half day? ('full'/'half')\n")
    waiting_list = input("Would the client like to join the waiting list? (y/n)")
    # wanting to be added to waiting list is stored as a boolean value
    waiting = True if waiting_list.lower() == 'y' else False

    # store client info as a dictionary (to be stored against the booking date)
    client_details = {
        'name': client_name,
        'phone': client_phone,
        'length': length,
        'waiting': waiting
    }

    print(client_details)

def main():
    login()
    choose_action()

main()