import sqlite3

connection = sqlite3.connect('Competency_Tracking_Tool.db')
cursor = connection.cursor()

insert_sql = "INSERT INTO Users (first_name, last_name, phone_number, email, password, date_created, hire_date, user_type) VALUES (?,?,?,?,?,?,?,?)"

first_name = input("Enter First Name: ")
last_name = input("Enter Last Name: ")
phone_number = input("Enter Phone Number: ")
email = input("Enter Email: ")
password = input("Enter Password: ")
date_created = print("Today's Date in Datetime")
hire_date = input("Enter Hire Date : ")
user_type = input("Account Type\n(1) User\n(2) Manager\nEnter :")

values = (first_name, last_name, phone_number, email, password, date_created, hire_date, user_type)
cursor.execute(insert_sql, values)

connection.commit()

print(f"\nUser {first_name}, {last_name} has been sucessfuly created.")