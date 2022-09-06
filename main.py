import sqlite3
import datetime
import pandas as pd
import bcrypt

connection = sqlite3.connect('Competency_Tracking_Tool.db')
cursor = connection.cursor()

while True:
    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    main_menu = input("Competency Tracking Tool\n(1) Login\n(2) Quit\nOption: ")
    if main_menu == "1":
        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        enter_username = input("Enter Email: ")
        enter_password = input("Enter Password: ")
        login_info = (enter_username, enter_password,)

        is_valid_login = cursor.execute("SELECT id_num, first_name, last_name, active, user_type FROM Users WHERE email =? and password =?",(enter_username, enter_password,)).fetchone()
        if not is_valid_login:
            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print("Could not find User with the following info.")
            continue

        id_num = is_valid_login[0]
        first_name = is_valid_login[1]
        last_name = is_valid_login[2]
        active = is_valid_login[3]
        user_type = is_valid_login[4]

        if active == 0:
            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
            print("User is not Active.")
            continue

# USER MENU ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if user_type == "1":
            while True:
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                user_menu = input(f"Welcome User, {first_name}.\n(1) View Competency and Assessment Data\n(2) Edit information\n(3) Exit Program\nOption: ")

    # VIEW ASSESSMENT RESULTS FOR THIS USER ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                
                if user_menu == "1":
                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    print("Competency and Assessment Data")
                    rows = cursor.execute("SELECT assessment, score, date_taken, manager_id FROM Assessment_Results WHERE user_id =?",(id_num,)).fetchall()

                    columns = ["Assessment", "Score", "Date Taken", "Manager"]
                    print(f'{columns[0]:<40}{columns[1]:<40}{columns[2]:<40}{columns[3]:<20}')

                    for row in rows:
                        print(f'{(row[0] if row[0] != None else "None"):<40}{(row[1] if row[1] != None else "None"):<40}{(row[2] if row[2] != None else "None"):<40}{(row[3] if row[3] != None else "None"):<40}')

    # EDIT PERSONAL INFO FOR THIS USER ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

            if user_menu == "2":
                while True:
                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                    update_option = input("To update a field, enter:\n(1) Name\n(2) Contact Info\n(3) Password\nTo return to the main menu, press 'Enter': ")

                    if update_option == "1":
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        updated_first_name = input("Update Name\nEnter First Name: ")
                        updated_last_name = input("Enter Last Name: ")

                        updated_info = (updated_first_name, updated_last_name, id_num)

                        update_sql = "UPDATE Users SET first_name=?, last_name=? WHERE id_num=?"
                        cursor.execute(update_sql, updated_info)
                        connection.commit()

                        print(f"\nYour name has been updated.")

                    if update_option == "2":
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        updated_email = input("Update Contact Info\nEnter Email: ")
                        updated_phone = input("Enter Phone Number: ")

                        updated_info = (updated_email, updated_phone, id_num)

                        update_sql = "UPDATE Users SET email=?, phone_number=? WHERE id_num=?"
                        cursor.execute(update_sql, updated_info)
                        connection.commit()

                        print(f"\nYour contact info has been updated.")

                    if update_option == "3":
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        updated_password = input("Update Password: ")

                        updated_password.encode("utf-8")

                        updated_info = (updated_password, id_num)

                        update_sql = "UPDATE Users SET password=? WHERE id_num=?"
                        cursor.execute(update_sql, updated_info)
                        connection.commit()

                        print(f"\nYour password has been updated.")
                        
                    if not update_option:
                        break

            if user_menu == "3":
                break

# MANAGER MENU ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if user_type == "2":
            while True:
                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                user_menu = input(f"Welcome Manager, {first_name}.\n(1) View & Search Data\n(2) Create new Records\n(3) Edit Records\n(4) Delete an Assessment Report\n(5) Import / Export Assessment Reports\nOption: ")
     
     # VIEW REPORTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if user_menu == "1":
                    while True:
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        view_option = input("View Competency and Assessment Data\n(1) View all Users\n(2) Search for User by Name\n(3) View an Assessment Result\n(4) View a User's Assessment Results\nPress 'Enter' to return to main menu: ")

                        if view_option == "1":
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            rows = cursor.execute("SELECT * FROM Users")
                            columns = ["ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"]
                            print(f'{columns[0]:<5}{columns[1]:<20}{columns[2]:<20}{columns[3]:<20}{columns[4]:<15}{columns[5]:<20}{columns[6]:<10}{columns[7]:<30}{columns[8]:<20}{columns[9]:<20}')

                            for row in rows:
                                print(f'{(row[0] if row[0] != None else "None"):<5}{(row[1] if row[1] != None else "None"):<20}{(row[2] if row[2] != None else "None"):<20}{(row[3] if row[3] != None else "None"):<20}{(row[4] if row[4] != None else "None"):<15}{(row[5] if row[5] != None else "None"):<20}{(row[6] if row[6] != None else "None"):<10}{(row[7] if row[7] != None else "None"):<30}{(row[8] if row[8] != None else "None"):<20}{(row[9] if row[9] != None else "None"):<20}')


                        if view_option == "2":
                            search_by_name = input("Search by:\n(1) First Name\n(2) Last Name\nPress 'Enter' to return to main menu: ")
                            
                            if not search_by_name:
                                break
                            
                            if search_by_name == "1":
                                search_term = input("Enter the first name of the user you wish to find: ")
                                search_term = "%" + str(search_term) + "%"

                                rows = cursor.execute("SELECT * FROM Users WHERE first_name LIKE ?", (search_term,)).fetchall()
                                columns = ["ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"]
                                print(f'{columns[0]:<5}{columns[1]:<20}{columns[2]:<20}{columns[3]:<20}{columns[4]:<15}{columns[5]:<20}{columns[6]:<10}{columns[7]:<30}{columns[8]:<20}{columns[9]:<20}')
                                break


                            if search_by_name == "2":
                                search_term = input("Enter the first name of the user you wish to find: ")
                                search_term = "%" + str(search_term) + "%"

                                rows = cursor.execute("SELECT * FROM Users WHERE first_name LIKE ?", (search_term,)).fetchall()
                                columns = ["ID", "First Name", "Last Name", "Phone", "Email", "Password", "Active", "Date Created", "Hire Date", "User Type"]
                                print(f'{columns[0]:<5}{columns[1]:<20}{columns[2]:<20}{columns[3]:<20}{columns[4]:<15}{columns[5]:<20}{columns[6]:<10}{columns[7]:<30}{columns[8]:<20}{columns[9]:<20}')
                                break


                        if view_option == "3":
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                view_assessment_results = input("Enter the Assessment you wish view. Press 'Enter' to return the main menu: ")

                                if not view_assessment_results:
                                    break

                                is_valid_assessment_result = cursor.execute("SELECT * FROM assessments WHERE id_num =?",(view_assessment_results,)).fetchone()

                                if not is_valid_assessment_result:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the Assessment with the entered ID Number.")
                                    continue

                            
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                rows = cursor.execute("SELECT * FROM Assessment_Results WHERE assessment =?",(view_assessment_results,))
                                columns = ["Test #", "User Tested", "Assessment ID Num", "Competency Score", "Date Taken", "Testing Manager"]
                                print(f'{columns[0]:<15}{columns[1]:<20}{columns[2]:<20}{columns[3]:<20}{columns[4]:<30}{columns[5]:<20}')

                                for row in rows:
                                    print(f'{(row[0] if row[0] != None else "None"):<15}{(row[1] if row[1] != None else "None"):<20}{(row[2] if row[2] != None else "None"):<20}{(row[3] if row[3] != None else "None"):<20}{(row[4] if row[4] != None else "None"):<30}{(row[5] if row[5] != None else "None"):<20}')

                                break

                        if view_option == "4":
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                view_assessment_results = input("Enter the User's ID you wish view. Press 'Enter' to return the main menu: ")

                                if not view_assessment_results:
                                    break

                                is_valid_assessment_result = cursor.execute("SELECT first_name, last_name FROM Users WHERE id_num =?",(view_assessment_results,)).fetchone()

                                if not is_valid_assessment_result:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the User with the entered ID Number.")
                                    continue
                            
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print("Competency and Assessment Data")
                                rows = cursor.execute("SELECT assessment, score, date_taken, manager_id FROM Assessment_Results WHERE user_id =?",(id_num,)).fetchall()

                                columns = ["Assessment", "Score", "Date Taken", "Manager"]
                                print(f'{columns[0]:<40}{columns[1]:<40}{columns[2]:<40}{columns[3]:<20}')

                                for row in rows:
                                    print(f'{(row[0] if row[0] != None else "None"):<40}{(row[1] if row[1] != None else "None"):<40}{(row[2] if row[2] != None else "None"):<40}{(row[3] if row[3] != None else "None"):<40}')
                                
                                break

                        if not view_option:
                            break

    # CREATE REPORTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if user_menu == "2":
                    while True:
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        option = input("Create Records\n(1) Create new User\n(2) Create new Competency Ranking\n(3) Create new Assessment\n(4) Create Assessment Result for a User\nPress 'Enter' to return to main menu.\nOption: ")

                        if option == "1":
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

                            insert_sql = "INSERT INTO Users (first_name, last_name, phone_number, email, password, date_created, hire_date, user_type) VALUES (?,?,?,?,?,?,?,?)"

                            create_first_name = input("Enter First Name: ")
                            create_last_name = input("Enter Last Name: ")
                            create_phone_number = input("Enter Phone Number: ")
                            create_email = input("Enter Email: ")
                            create_password = input("Enter Password: ")
                            create_date_created = datetime.datetime.today()
                            create_hire_date = input("Enter Hire Date: ")
                            create_user_type = input("Account Type\n(1) User\n(2) Manager\nEnter :")

                            create_password.encode("utf-8")

                            values = (create_first_name, create_last_name, create_phone_number, create_email, create_password, create_date_created, create_hire_date, create_user_type)
                            cursor.execute(insert_sql, values)

                            connection.commit()
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')     
                            print(f"User {create_first_name}, {create_last_name} has been sucessfuly created.")

                        if option == "2":
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                create_competencies = "INSERT INTO Competencies(id_num, name, date_created) VALUES (?,?,?)"

                                enter_ranking = input("Enter Competency score: ")

                                is_valid_competency = cursor.execute("SELECT * FROM Competencies WHERE id_num =?",(enter_ranking,)).fetchone()

                                if is_valid_competency:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("A Competency with that score already exists.")
                                    continue

                                enter_name = input("Enter name of Competency: ")
                                date_created = datetime.datetime.today()

                                values = (enter_ranking, enter_name, date_created)
                                cursor.execute(create_competencies, values)

                                connection.commit()
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')  
                                print(f'Competency "{enter_name}" has been sucessfuly created.')
                                break

                            
                        if option == "3":
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            create_competencies = "INSERT INTO Assessments(name, date_created) VALUES (?,?)"

                            enter_name = input("Enter Assessment name: ")
                            date_created = datetime.datetime.today()

                            values = (enter_name, date_created)
                            cursor.execute(create_competencies, values)

                            connection.commit()
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            print(f'Assessment "{enter_name}" has been sucessfuly created.')

                        if option == "4":
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

                                create_user = input("Enter the id number of the User who was tested.\nPress 'Enter' to return to the Menu: ")

                                if not create_user:
                                    break

                                is_valid_user = cursor.execute("SELECT first_name, last_name FROM Users WHERE id_num =?",(create_user,)).fetchone()

                                if not is_valid_user:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the User with the following id number.")
                                    continue

                                update_first_name = is_valid_user[0]
                                update_last_name = is_valid_user[1]


                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print(f"Creating a new Assessment Report for User {update_first_name}, {update_last_name}.")
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                
                                create_assignment = input("Enter the id number of the Assignment:\nPress 'Enter' to return to the Menu: ")
                            
                                if not create_assignment:
                                    break

                                is_valid_assignment = cursor.execute("SELECT name FROM Assessments WHERE id_num =?",(create_assignment,)).fetchone()

                                if not is_valid_assignment:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the Assessment with the following id number.")
                                    continue

                                valid_assignment_name = is_valid_assignment[0]

                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print(f"Assessment Name: {valid_assignment_name}.")
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            
                                create_score = input(f"Enter the Competency's Score:\nPress 'Enter' to return: ")
                            
                                if not create_score:
                                    break

                                is_valid_score = cursor.execute("SELECT * FROM Competencies WHERE id_num =?",(create_score,)).fetchone()

                                if not is_valid_score:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the Competency Score.")
                                    continue

                                date_created = datetime.datetime.today()

                                create_assessment_results = "INSERT INTO Assessment_Results(user_id, assessment, score, date_taken, manager_id) VALUES (?,?,?,?,?)"
                                values = (create_user, create_assignment, create_score, date_created, id_num)
                                cursor.execute(create_assessment_results, values)
                                connection.commit()

                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print(f"Assesment Report Created Sucessfully.")
                                break
                                      
                        if not option:
                            break

    # EDIT REPORTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if user_menu == "3":
                    while True:
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        update_menu = input("Edit Records:\n(1) Edit User Info \n(2) Edit Competency Scale\n(3) Edit Assessments\n(4) Edit Assessment Results\nTo return to the main menu, press 'Enter': ")

                        if update_menu == "1":                            
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

                                user_id_num = input("Enter the User's id number whose info you wish to edit.\nPress 'Enter' to return to the Main Menu: ")

                                if not user_id_num:
                                    break

                                is_valid_user = cursor.execute("SELECT first_name, last_name FROM Users WHERE id_num =?",(user_id_num,)).fetchone()

                                if not is_valid_user:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find the User with the following info.")
                                    continue

                                update_first_name = is_valid_user[0]
                                update_last_name = is_valid_user[1]

                                while True:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    update_option = input(f"Editing {update_first_name}, {update_last_name}'s information.\nTo update a field, enter:\n(1) Name\n(2) Contact Info\n(3) Password\n(4) Deactivate / Reactivate User\n(5) Change User Type\nTo return to the main menu, press 'Enter': ")

                                    if update_option == "1":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        updated_first_name = input("Update Name\nEnter First Name: ")
                                        updated_last_name = input("Enter Last Name: ")

                                        updated_info = (updated_first_name, updated_last_name, user_id_num)
                                        update_first_name = updated_first_name
                                        update_last_name = updated_last_name

                                        update_sql = "UPDATE Users SET first_name=?, last_name=? WHERE id_num=?"
                                        cursor.execute(update_sql, updated_info)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')                                
                                        print(f"The user's name has been updated.")

                                    if update_option == "2":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        updated_email = input("Update Contact Info\nEnter Email: ")
                                        updated_phone = input("Enter Phone Number: ")

                                        updated_info = (updated_email, updated_phone, user_id_num)

                                        update_sql = "UPDATE Users SET email=?, phone_number=? WHERE id_num=?"
                                        cursor.execute(update_sql, updated_info)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print(f"The user's contact info has been updated.")

                                    if update_option == "3":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        updated_password = input("Update Password: ")

                                        updated_info = (updated_password, user_id_num)

                                        update_sql = "UPDATE Users SET password=? WHERE id_num=?"
                                        cursor.execute(update_sql, updated_info)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print(f"The user's password has been updated.")
                                        
                                    if update_option == "4":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        updated_active = input("Deactivate / Reactivate Record\nEnter '1' to Activate.\nEnter '0' to Deactivate.\nPress 'Enter' to return to the main menu: ")
                                        updated_info = (updated_active, user_id_num)

                                        if not updated_active:
                                            continue

                                        update_sql = "UPDATE Users SET active=? WHERE id_num=?"
                                        cursor.execute(update_sql, updated_info)
                                        connection.commit()

                                        if updated_active == "1":
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("The users's records have been activated.")

                                        if updated_active == "0":
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("The users's records have been deactivated.")

                                    if update_option == "5":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        updated_user_type = input("Change User Type\nEnter '1' to make User\nEnter '2' to make Manager\nPress 'Enter to return to the main menu: ")
                                        updated_user_type = str(updated_user_type)
                                        updated_info = (updated_user_type, user_id_num)

                                        if not updated_user_type:
                                            continue

                                        if updated_user_type == "1":
                                            update_sql = "UPDATE Users SET user_type = ? WHERE id_num = ?"
                                            cursor.execute(update_sql, updated_info)
                                            connection.commit()

                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print(f"Manager {update_first_name}, {update_last_name} is now a User.") 

                                        if updated_user_type == "2":
                                            update_sql = "UPDATE Users SET user_type = ? WHERE id_num = ?"
                                            cursor.execute(update_sql, updated_info)
                                            connection.commit()

                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print(f"User {update_first_name}, {update_last_name} is now a Manager.")  

                                
                                    if not update_option:
                                            break

                        if update_menu == "2":                            
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                competency_id_num = input("Enter the Competency's score number that you wish to edit.\nPress 'Enter' to exit: ")

                                if not competency_id_num:
                                    break

                                is_valid_competency = cursor.execute("SELECT * FROM Competencies WHERE id_num =?",(competency_id_num,)).fetchone()

                                if not is_valid_competency:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find a Competency with that score.")
                                    continue

                                updated_id_num = input("Enter the new Competency's score: ")

                                is_valid_competency = cursor.execute("SELECT * FROM Competencies WHERE id_num =?",(updated_id_num,)).fetchone()

                                if is_valid_competency:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("A Competency with that score already exists.")
                                    continue

                                updated_name = input("Enter the new Name of the Competency: ")
                                updated_date_created = datetime.datetime.today()

                                updated_info = (updated_id_num, updated_name, updated_date_created, competency_id_num)

                                update_sql = "UPDATE Competencies SET id_num =?, name=?, date_created =? WHERE id_num=?"
                                cursor.execute(update_sql, updated_info)
                                connection.commit()

                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print("The Competency has been updated.")

                        if update_menu == "3":                            
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                assessment_id_num = input("Enter the Assessment's id number you wish to edit.\nPress 'Enter' to exit: ")

                                if not assessment_id_num:
                                    break

                                is_valid_competency = cursor.execute("SELECT name FROM Assessments WHERE id_num =?",(assessment_id_num,)).fetchone()

                                name_of_assessments = is_valid_competency[0]

                                if not is_valid_competency:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find an Assessment with that id number.")
                                    continue

                                updated_name = input("Enter the new Name of the Competency: ")
                                updated_date_created = datetime.datetime.today()

                                updated_info = (updated_name, updated_date_created, assessment_id_num)

                                update_sql = "UPDATE Assessments SET name=?, date_created =? WHERE id_num=?"
                                cursor.execute(update_sql, updated_info)
                                connection.commit()

                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                print("The Assessment has been updated.")

                        if update_menu == "4":
                            while True:
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                assessment_result_id_num = input("Enter the Assessment Result's id number that you wish to edit.\nPress 'Enter' to exit: ")

                                if not assessment_result_id_num:
                                    break

                                is_valid_assessment_result = cursor.execute("SELECT * FROM Assessment_Results WHERE id_num =?",(assessment_result_id_num,)).fetchone()

                                if not is_valid_assessment_result:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    print("Could not find a Assessment Result with that id number.")
                                    continue

                                while True:
                                    print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                    assessment_result_update = input("Update Assessment Result\n(1) Change User who was tested\n(2) Change Assessment that was tested\n(3) Change Competency Score\n(4) Change Manager who admistered the test\nPress 'Enter' to return to the previous menu: ")

                                    if assessment_result_update == "1":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        user_id_num = input("Enter the new User's id number.\nPress 'Enter' to return to the Main Menu:  ")
                                    
                                        is_valid_user = cursor.execute("SELECT first_name, last_name FROM Users WHERE id_num =?",(user_id_num,)).fetchone()

                                        if not is_valid_user:
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("Could not find the User with the following info.")
                                            continue

                                        values = (user_id_num, assessment_result_update)
                                        update_sql = "UPDATE Assessment_Results SET user_id=? WHERE id_num=?"
                                        cursor.execute(update_sql, values)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print("Successfully updated Assessment Results.")
                                        
                                    if assessment_result_update == "2":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        user_id_num = input("Enter the new Assessment's id number.\nPress 'Enter' to return to the Main Menu:  ")
                                    
                                        is_valid_user = cursor.execute("SELECT * FROM Assessments WHERE id_num =?",(user_id_num,)).fetchone()

                                        if not is_valid_user:
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("Could not find the Assessment with the following info.")
                                            continue

                                        values = (user_id_num, assessment_result_update)
                                        update_sql = "UPDATE Assessment_Results SET assesssment=? WHERE id_num=?"
                                        cursor.execute(update_sql, values)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print("Successfully updated Assessment Results.")

                                    if assessment_result_update == "3":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        user_id_num = input("Enter the Competency Score.\nPress 'Enter' to return to the Main Menu:  ")
                                    
                                        is_valid_user = cursor.execute("SELECT * FROM Competencies WHERE id_num =?",(user_id_num,)).fetchone()

                                        if not is_valid_user:
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("Could not find the Competency with the following info.")
                                            continue

                                        values = (user_id_num, assessment_result_update)
                                        update_sql = "UPDATE Assessment_Results SET score=? WHERE id_num=?"
                                        cursor.execute(update_sql, values)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print("Successfully updated Assessment Results.")

                                    if assessment_result_update == "4":
                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        user_id_num = input("Enter the new Manager.\nPress 'Enter' to return to the Main Menu:  ")
                                    
                                        is_valid_user = cursor.execute("SELECT first_name, last_name FROM Users WHERE id_num =? and user_type =2",(user_id_num,)).fetchone()

                                        if not is_valid_user:
                                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                            print("Could not find the Manager with the following info.")
                                            continue

                                        values = (user_id_num, assessment_result_update)
                                        update_sql = "UPDATE Assessment_Results SET user_id=? WHERE id_num=?"
                                        cursor.execute(update_sql, values)
                                        connection.commit()

                                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                                        print("Successfully updated Assessment Results.")

                                    if not assessment_result_update:
                                        break

                        if not update_menu:
                            break

     # DELETE ASSESSMENT REPORTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if user_menu == "4":
                    while True:
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        delete_assessment_result = input("Enter the ID number of the Assessment Result you wish to delete.\nPress 'Enter' to Exit: ")

                        if not delete_assessment_result:
                            break

                        is_valid_assessment_result = cursor.execute("SELECT * FROM Assessment_Results WHERE id_num =?",(delete_assessment_result,)).fetchone()

                        if not is_valid_assessment_result:
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            print("Could not find an Assessment Result with the provided id number.")
                            continue

                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                        safeguard = input("Are you sure you want to delete this?\n(1) Yes\n(2) No\nOption: ")

                        if safeguard == "2":
                            break

                        if safeguard == "1":

                            delete_sql = cursor.execute("DELETE FROM Assessment_Results WHERE id_num =?",(delete_assessment_result,)).fetchone()
                            connection.commit()

                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
                            print(f"Assignment:{delete_assessment_result} has been deleted.")
                            break

# EXPORT / IMPORT REPORTS ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                if user_menu == "5":
                    while True:
                        print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')      
                        csv_files_menu = input("Import Files\n(1) Export Assessent Results\n(2) Import CSV File\n Press 'Enter' to return to main menu: ")

                        if csv_files_menu == "1":
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')      
                            export_option == input("Export Assessment Results\n(1) Competency reports by Assessment\n(2) Competency report for a single user\n Press 'Enter' to return to main menu: ")

                            if export_option == "2":
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')      
                                export_user_info = input("Enter the User's ID number you wish to export: ")

                                sql_query = pd.read_sql_query("SELECT * FROM Assessment_Results WHERE user_id=?",(export_user_info,)).fetchall()
                                squl_query.to_csv(r'E:\output\assessment_results.csv', index = False)
                                break

                            if export_option == "1":
                                print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')      
                                export_user_info = input("Enter the Assessment's ID number you wish to export: ")

                                sql_query = pd.read_sql_query("SELECT * FROM Assessment_Results WHERE assessment_id=?",(export_user_info,)).fetchall()
                                squl_query.to_csv(r'E:\output\assessment_results.csv', index = False)
                                break

                            if not export_option:
                                break


                        if csv_files_menu == "2":
                            print('-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')      
                            name_of_file = input("Enter the name of the file: ")

                            df = pandas.read_csv(name_of_file , usecols = ['user_id', "assessment_id",'score', 'date_taken'])
                            df.to_csv(name_of_file , index = False)

                        if not csv_files_menu:
                            break

                if user_menu == "6":
                    break

    if main_menu == "2":
        break


