#CST1510 - Programming for Data Communication and Networks
#Coursework 2 - Multi-Domain Intelligence Platform
#Ali Layan Thohir - M01091333

#Inclusion/Integration of module needed for hashing passwords and other components of code 
import bcrypt
import os
import secrets
import string
from datetime import datetime,timedelta

#Text file to store user and session data
USER_DATA_FILE = "users.txt"
SESSION_DATA_FILE = "sessions.txt"
LOCKOUT_FILE = "lockout.txt"

#Function to check password strength
def check_password_strength(password):
    #Special characters
    special = string.punctuation
    
    #Flags for strength checking
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    
    #Length check for password
    if len(password) < 6:
        return  "Weak"
        
    #Loop through each character in the password and checks if all strength criteria is met
    for char in password:
        #Flags for each criteria
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        elif char in special:
            has_special = True
    
    #Length check for medium incase all flags are true but length is short
    if has_lower and has_upper and has_digit and has_special:
        #If all criteria is met and length is minimum 8
        if len(password) >= 8:
            return "Strong"
        #If all criteria is met but length is less than 8
        else: 
            return "Medium"
            
    #If criteria for length is correct but not all flags are true
    else:
        return "Weak"

#Function to hash passwords
def hash_pass(password):
    #Converting string password into bytes
    pass_bytes = password.encode("utf-8")
    #Generating a salt and hashing the password with it
    salt = bcrypt.gensalt()
    hashpass = bcrypt.hashpw(pass_bytes,salt)
    #Converting hashed password back to string for storage
    hashpass = hashpass.decode("utf-8")
    return hashpass

#Function to register a user
def register(username,password,group):
    #Checking if username already exists using premade function
    if verify_user(username):
        return f'User: {username} already exists. Please choose a different username.'
                
    #Hashing the password using premade function 
    hashed = hash_pass(password)
    
    #Group assignment according to what input user gives
    if group == 1:
        group = "Cybersecurity Analyst"
    elif group == 2: 
        group = "Data Scientist"
    elif group == 3:
        group = "IT Administrator"
        
    #Storing username, password and role in a text file
    with open ("users.txt","a") as file:
        file.write(f"{username},{hashed},{group}\n")
        
    #Confirms that the user has been registered
    return f"User: {username} is now registered."
   
#Function to verify if user exists
def verify_user(username):
    #To handle case where users.txt file does not exist yet so loop does not break automatically / end abruptly
    try:
        #Checking if username already exists
        with open("users.txt","r") as file:
            user = file.readlines()
            #Reads each line in the file one by one
            for line in user:
                #Splits the line into username, password and role but only checks the first which is the username
                if line.split(",")[0] == username:
                    return True
    #If file does not exist, returns false. 
    except FileNotFoundError:
        print("'users.txt' file not found/created.")
    return False
    
#Function to Verify password
def verify_pass(stored,provided):
    #Converting password and hashed password into bytes
    pass_bytes = provided.encode("utf-8")
    stored_bytes = stored.encode("utf-8")
    #Checking and verifying whether the provided password matches the stored hashed password
    return bcrypt.checkpw(pass_bytes,stored_bytes)

#Function to login a user
def login(username,password):
    
    #Check if user is locked out, if they are, print statement, if not, nothing happens
    if check_lockout(username):
        return "Your account '{user}' is locked, please try to login 5 minutes after you have been locked out."
    
    
    #Opens text file to read hashed password and verify input password    
    with open("users.txt","r") as file: 
        #Reads each line in file
        for line in file:
            #Gets rid of any newline characters or empty spaces
            line = line.strip()
            #Only works if line is not empty
            if line:
                #Splits the line into username and it's hashed password
                user, hash_pass, role = line.strip().split(',')
                if user == username:
                    #Verifying password using premade function
                    check = verify_pass(hash_pass,password)
                    #If password is the same, creates session token and print statement that they are logged in
                    if check == True:
                        #In the case that the user got the password right, resets the lockout just incase they got it wrong once
                        reset_lockout(username)
                        token, timestamp = create_token(username)
                        return f'Successfully logged in {username}, your session token is: {token} at {timestamp}'
                    #If password in incorrect
                    else:
                        #Record the failed login attempt 
                        record_attempt(username)
                        return "Incorrect password, please try again."

#Function to validate username
def validate_user(username):
    #Length validation for username
    if len(username) <3 or len(username) >20:
        return False, 'Error: Username should be between 3 and 20 characters long.'
    #Invalid characters for username
    for char in username:
        #Makes sure that characters are either alphabetical or numerical only.
        if not char.isalnum():
            return False, 'Error: Username can only contain letters and numbers.'
    return True, ""

#Function to validate password
def validate_pass(password):
    #Length validation for password
    if len(password) < 6 or len(password) > 50:
        return False, 'Error: Password should be between 6 and 50 characters long.'
    return True, ""

#Function to create a token of session
def create_token(username):
    #Creates token using secrets module 
    token = secrets.token_hex(16)
    #Gets current time for session 
    curtime = datetime.now().strftime("%H:%M:%S")
    #Storing token and time in a text file
    with open("sessions.txt","a") as file:
        file.write(f'{username},{token},{curtime}\n')                
    #Returns the token number after function is called
    return token, curtime

#Function to check if a user is currently in lockout
def check_lockout(username):
    #To handle case where lockout.txt file does not exist yet so loop does not break automatically / end abruptly
    try:
        #Opens lockout.txt file to read
        with open("lockout.txt","r") as file:
            #Goes line by line in file
            for line in file:
                #Get's information from the line and assigns it to these 3 variables
                user, attempts, latest_time = line.strip().split(",")
                #If the username is in fact in that line and the failed attempts is equal to 3
                if user == username and int(attempts) >= 3:
                    #Format to be used for later calculation
                    latest_time = datetime.strptime(latest_time, "%Y-%m-%d %H:%M:%S")
                    #Checks if it's less than 5 minutes since lockout
                    if datetime.now() - latest_time < timedelta(minutes = 5):
                        return True
    #In the case that file does not exist yet, skip and return "False"
    except FileNotFoundError:
        pass
    return False

#Function to record failed attempts
def record_attempt(username):
    #Dictionary to keep record of failed attempts, key being username, value being the attempt number
    data = {}
    #In the case lockout.txt doesn't exist yet
    try:
        #Opens file, reads it line by line, if it exists assigns information to variables
        with open("lockout.txt","r") as file:
            for line in file:
                user, attempts, latest_time = line.strip().split(",")
                #Stores the user data and the attempts along with the attempt time in dictionary
                data[user] = [int(attempts), latest_time]
    #If file isn't created yet, skips so 
    except FileNotFoundError:
        pass
    
    #If the username is in the data dictionary already, increments attempts 
    if username in data:
        data[username][0] += 1
    #If username is not in the login, add user to data and set attempts to 1 and stores timestamp
    else: 
        data[username] = [1, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    #Updates data into file / creates file if it doesn't exist and stores first user's data in it
    with open("lockout.txt","w") as file:
        for user, (attempts, latest_time) in data.items():
            file.write(f'{user},{attempts},{latest_time}\n')

#Function to reset lockout
def reset_lockout(username):
    #List to store lines from file
    lines = []
    #Opens textfile and adds lines to list
    with open("lockout.txt","r") as file:
        lines = file.readlines() 
        
    with open("lockout.txt","w") as file:
        #For each line in the list
        for line in lines:
            #If the user is in this line, skips this line
            if not line.startswith(username + ","):
                #Rewriting the file without the user who's no longer locked out
                file.write(line)
                
#Input from user for menu task as a loop until either valid input is given or user exits. 
while True:
    #Menu/Start-up display for registration/login
    print("""
    Welcome to the Multi-Domain Intelligence Platform:
    Please select an option from the following:
    1. Register as a new user
    2. Login as an existing user""")
    try:
        #Input for choice of task
        choice = int(input("Please enter 1 or 2 (enter 0 to exit): "))
        
        #If user wants to exist program
        if choice == 0: 
            print("Thank you for using the Multi-Domain Intelligence Platform. Goodbye!\nExitting...")
            break
        
        #If user wants to register a new account
        elif choice == 1:       
            #.strip() is used to remove any leading or trailing spaces or new line characters
            #Username
            username = input("Please enter your username: ").strip()
            #Validation check for username using predefined function
            valid_user, msg = validate_user(username)
            #If username is invalid, restarts loop
            if not valid_user:
                print(msg)
                continue 
            
            #Password
            password = input("Please enter a password: ").strip() 
            #Validation check for password using predefined function
            valid_pass, msg = validate_pass(password)
            #If password is invalid, restarts loop
            if not valid_pass:
                print(msg)
                continue
            #Password strength check using predefined function
            strength = check_password_strength(password)
            #If password strength is not strong, restarts loop 
            if strength != "Strong":
                print(f'''
                      Your password strength is: {strength}. Please choose a stronger password.
                      It should be a minimum of 8 characters and contain one of each of the following:
                      - Uppercase letter
                      - Lowercase letter
                      - A digit
                      - A special character like '!','@','#',etc...''')
                continue 
            
            #Group to be assigned to
            group = int(input("1. Cybersecurity Analysts\n2. Data Scientists\n3. IT Administrators\nPlease enter what group you belong to: "))
            
            #If user enters an invalid group number - restarts loop
            if group <1 or group >3:
                print("The input you have entered is not among the options. Please enter only 1, 2 or 3.")      
                continue
            
            #If all validations are passed, registers user and prints confirmation
            result = register(username,password,group)
            print(result)
        
        #If user wants to login to an existing account                
        elif choice == 2:
            #.strip() is used to remove any leading or trailing spaces or new line characters
            
            #Making sure username is valid / exists, if not - restarts loop
            username = input("Please enter your registered username: ").strip()
            verified_user = verify_user(username)
            if not verified_user:
                print("Incorrect username or this user doesn't exist.")
                continue 
            
            #Password for login
            password = input("Please enter your password: ").strip()
            
            #Login user function called and checked using the inputs given above, prints whether successful or not
            result = login(username,password)
            print(result)
            
        #If user inputs invalid option, print statement and restarts loop 
        elif choice < 0 or choice > 2:
            print("The input you have entered is not valid. Please enter either 1 or 2, thank you.")
    
    #If non-integer value is given, restarts loop after printing statement        
    except ValueError:
        print("The input you have entered is not valid. Please enter either 1 or 2, thank you.")