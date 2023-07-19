
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# ask for username and password to be entered
username = input("Please enter your username: ")
password = input("Please enter your password: ")

print(username)
print(password)

# open the user_login secure file in 'read' and check whether
# credentials are accurate

with open("user_login.txt", "r") as file:
    for line in file:
        valid_username, correct_password = line.strip().split(":")
        if username == valid_username and password == correct_password:
            print("Login successful. Welcome to your booking system!")
        else:
            print("Invalid username or password, please try again")


