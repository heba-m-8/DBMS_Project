# Heba Marei - 20200400
# Taya Jarrar - 20200813
# Lina Matar - 20200277

import pandas as pd
import hashlib

# reading the Excel sheet:
data = pd.read_csv('password_file.csv')


def check_permission(user_id):

    user_role_data = data.loc[
        data['workID'] == int(user_id), 'role']

    user_role = user_role_data.values[0]
    print("Role:", user_role)

    if user_role == 'Project Manager':
        print("Full access granted for project manager, here is the database:\n")
        print(data)

        answer = input("Do you want to change any employee's salary? (yes/no)\n")
        if answer == 'yes':
            while True:
                emp_id = input("Enter the employee ID:\n")
                if int(emp_id) not in data['workID']:
                    print(emp_id, 'is not a valid employee ID. \n')
                    continue

                new_sal = input("Enter the new salary:\n")
                edit_table(emp_id, new_sal)
                data.to_csv('password_file.csv', index=False)
                break

    elif user_role == 'Supervisor':
        print("Access granted for supervisor, you can view the employees' names and emails.\n")
        columns_to_view = ['first_name', 'last_name', 'email']
        selected_data = data[columns_to_view]
        print(selected_data)

    else:
        print("You have no access.\n")


def edit_table(emp_id, new_sal):

    employee_id_from_table = data.loc[
        data['workID'] == int(emp_id)].index[0]

    # Update the salary for the corresponding employee
    data.at[employee_id_from_table, 'salary'] = new_sal
    print("Salary updated successfully.")


def hashing(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed


def register():
    while True:
        employee_id = input("Enter your employee ID to register: \n")

        if int(employee_id) not in data['workID']:
            print(employee_id, 'is not a valid employee ID. \n')
            continue

        if data.loc[data['workID'] == int(employee_id), 'password'].notna().values[0]:
            print(employee_id, 'is already registered. \n')
            continue

        pwd = input("Enter a password: \n")
        confirm_pwd = input("Confirm your password: \n")

        if pwd == confirm_pwd:
            hashed_password = hashing(pwd)
            data.loc[
                data['workID'] == int(employee_id), 'password'] = hashed_password  # locating ID to add hashed password
            print("You have successfully registered. \n")
            break
        else:
            print("Passwords do not match. \n")


def login():
    while True:
        employee_id = input("Enter your employee ID to log in: \n")

        if int(employee_id) not in data['workID'].values:
            print(employee_id, 'is not a valid employee ID.\n')
            continue

        pwd = input("Enter your password: \n")
        hashed_password = hashing(pwd)

        stored_hashed_password = data.loc[data['workID'] == int(employee_id), 'password'].values[0]
        if hashed_password == stored_hashed_password:
            print("Login successful. \n")
            check_permission(employee_id)
            break
        else:
            print("Incorrect password. \n")


while True:
    choice = input("Welcome! Enter L for login, and R for registration. \n")
    if choice == 'L':
        login()
        break

    elif choice == 'R':
        register()
        # save updated data:
        data.to_csv('password_file.csv', index=False)
        break
    else:
        print("Invalid choice.\n")
