import pandas as pd
import hashlib

# reading the Excel sheet:
data = pd.read_csv('password_file.csv')


def hashing(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed


def register():
    while True:
        employee_id = input("Enter your employee ID to register: \n")
        pwd = input("Enter a password: \n")
        confirm_pwd = input("Confirm your password: \n")

        if pwd == confirm_pwd:
            hashed_password = hashing(pwd)
            data.loc[data['workID'] == int(employee_id), 'password'] = hashed_password   # locating ID to add hashed password
            print("You have successfully registered. \n")
            break
        else:
            print("Passwords do not match. \n")


def login():
    employee_id = input("Enter your employee ID to log in: \n")
    pwd = input("Enter your password: \n")

    hashed_password = hashing(pwd)

    if employee_id in data['workID'].astype(str).values:
        stored_hashed_password = data.loc[data['workID'] == int(employee_id), 'password'].values[0]
        if hashed_password == stored_hashed_password:
            print("Login successful. \n")
        else:
            print("Incorrect password. \n")
    else:
        print("Employee ID not found. \n")


choice = input("Welcome! Enter A for login, and B for registration. \n")

if choice == 'A':
    login()
elif choice == 'B':
    register()
    # save updated data:
    data.to_csv('password_file.csv', index=False)
else:
    print("Invalid choice.\n")
