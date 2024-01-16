"""This program is a task management tool which allows users to:
ADD MORE INFO"""

# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.


#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# FUNCTIONS

def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    new_username = input("New Username: ")
    while True:
        if new_username in username_password.keys():
            new_username = input("That username already exists. Please enter another: ")
        else:
            break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w", encoding="utf-8") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task,
        - A description of the task and 
        - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        return
    task_title = input("Title of Task: ")
    # add code to print character limit
    # Check that the task title is below character limit and reprompt if not.
    # add code to check the title is not already in the list (i.e. is unique)
    # if it is, prompt user to choose a different title
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            # OPTIONAL TO DO - check if due_date_time(as date only) >= date.today()
            # If so, break
            # else, continue
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    # Add the data to the file task.txt and
    # Include 'No' to indicate if the task is complete.
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w", encoding="utf-8") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    '''
    # OPTIONAL - add a submenu to allow user to select:
            # all tasks - due and completed
            # all due tasks
            # all completed tasks
    # OPTIONAL - display a summary first and allow access to details when selected
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(
            DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(
            DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine():
    '''Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    '''
    # PC - display all tasks in a manner that is easy to read.
    # Initialise a list for storing the current user's assigned tasks
    user_task_lookup = []
    # Loop through the task_list and append user's tasks to user_task_lookup
    for t in task_list:
        if t['username'] == curr_user:
            user_task_lookup.append(t)

    # print a summary of all the current user's assigned tasks - use tabulate to tidy up?
    clear_screen()
    print("\n\033[1mTask summary:\033[0m\n")

    # TO DO - Check if user_task_lookup is empty
    # TO DO - If empty, print a message saying this and return to main menu.

    # OPTIONAL TO DO - print in two sections with separate headings -
    # incomplete tasks first and then completed
    # TO DO - fix yes/no alignment issue
    print("No.\tDue date\tTask\t\t\t\tCompleted?")
    for i, t in enumerate(user_task_lookup, start=1):
        print(f"{i}.\t{t['due_date'].strftime(
            DATETIME_STRING_FORMAT)}\t{t['title']}\t\t\t{
                "yes" if t['completed'] is True else "no"}")

    # OPTIONAL TO DO - heading for completed section

    # exit function if user_select = "-1". Check validity of user input
    while True:
        user_select = input("\nPlease enter a task number to view / edit a task\n"
                        "or type '-1' to return to the main menu: ")
        if user_select == "-1":
            return
        if not user_select.isnumeric():
            continue
        user_select = int(user_select)
        if 0 < user_select <= len(user_task_lookup):
            break

    # Loop that displays selected task with details and allows editing
    while True:
        print("\n\033[1mTask details:\033[0m\n")

        for t in task_list:
            if t == user_task_lookup[user_select-1]:
                selected_task = t

        disp_str = f"Task: \t\t {selected_task['title']}\n"
        disp_str += f"Assigned to: \t {selected_task['username']}\n"
        disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(
            DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {selected_task['due_date'].strftime(
            DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {selected_task['description']}\n"
        print(disp_str)

        # Display view / edit options to the user.
        print("\nOptions:\n"
            "c - mark this task as completed\n"
            "u - change the assigned user\n"
            "d - change the due date\n"
            "r - return to the task summary screen\n"
            "q - return to the main menu\n")
        vm_choice = input("Please enter a letter: ")

        if vm_choice.lower() == "c":
            # Allow user to mark the current task as completed.
            print("\nPlease note: once marked as completed, the selected task "
                  "can no longer be edited.")
            while True:
                confirm_complete = input("\nPlease type 'y' to confirm task "
                                     "completion or 'n' to go back: ")
                if confirm_complete.lower() == "y":
                    selected_task['completed'] = True
                    update_output()
                    print("\nThe selected task has been marked as completed "
                          "and can no longer be edited.")
                    break
                if confirm_complete.lower() == "n":
                    print("\nNo change has been made - the task is "
                          "still active.")
                    break
                print("\nPlease select a valid option.")
            # Return to task summary display
            view_mine()

        elif vm_choice.lower() == "u":
            # Allow user to assign the current task to a different user.
            if selected_task['completed'] is True:
                # clear screen
                clear_screen()
                print("\nThis task is already marked as completed and can "
                      "no longer be edited.")
                continue
            changed_user = input("\nPlease enter the user "
                                "who you would like to assign this task to: ")
            # OPTIONAL TO DO - check that the assigned user is registered.
            # If not, display list of registered users and ask to reinput.
            # Update username in task_list
            selected_task['username'] = changed_user

            # Write updated task_list to tasks.txt, print message
            # and return to summary.
            update_output()
            print("\nAssigned user has been updated. You can no longer edit this task.\n")
            view_mine()

        elif vm_choice.lower() == "d":
            # Allow user to change the due date.
            if selected_task['completed'] is True:
                # clear screen
                clear_screen()
                print("\nThis task is already marked as completed and can "
                      "no longer be edited.")
                continue
            # Collect new data input, update task_list and output file
            # Display confirmation of change to date.
            while True:
                try:
                    changed_due_date = input("Please enter a new due date "
                                             "for this task (YYYY-MM-DD): ")
                    selected_task['due_date'] = datetime.strptime(
                        changed_due_date, DATETIME_STRING_FORMAT)
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format "
                          "specified")
                # Optional TO DO: check that date is valid - later than or equal to today?
            update_output()
            print("The due date for this task has now been updated.")
            # Return to start of detailed display loop

        elif vm_choice.lower() == "r":
            # return to summary list
            view_mine()
        elif vm_choice.lower() == "q":
            # return to main menu
            return
        else:
            print("\nPlease select a valid option.")
            continue


def generate_reports():
    """Generates two .txt reports: task_overview.txt and 
    user_overview.txt"""

    # Generate task overview report
    # Calculate task overview report data
    no_tasks = len(task_list)
    no_completed = 0
    no_overdue = 0
    for t in task_list:
        if t['completed'] is True:
            no_completed += 1
        if t['completed'] is False and t['due_date'].date() < datetime.today().date():
            no_overdue += 1
    no_incomplete = no_tasks - no_completed
    # TO DO - if task_list empty, percent_incomplete = "No data message" Else:
    percent_incomplete = round((no_incomplete / no_tasks  *100), 2)
    percent_overdue = round((no_overdue / no_tasks * 100), 2)

    # Write task overview report to output file.
    with open("task_overview.txt", "w", encoding = "utf-8") as t_rpt:
        t_rpt.write("Task overview:\n")
        if not task_list:
            t_rpt.write("No task data has been generated.")
        else:
            t_rpt.write(f"\nTotal tasks in task list: {no_tasks}")
            t_rpt.write(f"\nNumber of completed tasks: {no_completed}")
            t_rpt.write(f"\nNumber of incomplete tasks: {no_incomplete}")
            t_rpt.write(f"\nNumber of overdue incomplete tasks: {no_overdue}")
            t_rpt.write(f"\nPercentage of tasks that are incomplete: {percent_incomplete} %")
            t_rpt.write(f"\nPercentage of tasks that are overdue: {percent_overdue} %")

    # Generate user overview report
    # Calculate data for user overview report

    # Write user overview report to output file
    with open("user_overview.txt", "w", encoding = "utf-8") as u_rpt:
        u_rpt.write("User overview\n")
        u_rpt.write(f"\nNumber of registered users: {len(user_data)}")
        u_rpt.write(f"\nTotal tasks in task list: {no_tasks}\n")
        # Calculate data for each user
        # TO DO - REFACTOR AND SIMPLIFY calculations below
        # FIX bug with Garry showing as having a task
        for u in username_password.keys():
            num_user_tasks = 0
            num_comp_tasks = 0
            num_incomp_tasks = 0
            num_overdue_tasks = 0
            for t in task_list:
                if t['username'] == u:
                    num_user_tasks += 1
                    if t['completed'] is True:
                        num_comp_tasks += 1
                    elif t['completed'] is False:
                        num_incomp_tasks += 1
                        if t['due_date'].date() < datetime.today().date():
                            num_overdue_tasks += 1
            percent_of_total = round(num_user_tasks / no_tasks * 100, 2)
                    # TO DO - defend against zero division errors in lines below
                    # if BLAH = 0 u_percent_comp = "N/a"
            try:
                u_percent_comp = round(num_comp_tasks / num_user_tasks * 100, 2)
            except ZeroDivisionError:
                u_percent_comp = "N/a"
            try:
                u_percent_incomp = round(num_incomp_tasks / num_user_tasks * 100, 2)
            except ZeroDivisionError:
                u_percent_incomp = "N/a"
            try:
                u_percent_overdue = round(num_overdue_tasks / num_incomp_tasks * 100, 2)
            except ZeroDivisionError:
                u_percent_overdue = "N/a"

            u_rpt.write(f"\nUser: {u}")
            u_rpt.write("\n-------------------")
            u_rpt.write(f"\nTasks assigned: {num_user_tasks}")
            u_rpt.write(f"\nPercentage of all tasks: {percent_of_total}")
            u_rpt.write(f"\nPercentage of assigned tasks completed: {u_percent_comp}")
            u_rpt.write(f"\nPercentage of assigned tasks incomplete: {u_percent_incomp}")
            u_rpt.write(f"\nPercentage of incomplete tasks overdue: {u_percent_overdue}\n")
    # clear_screen()
    print("\nUser and task overview reports have been generated.")


def update_output():
    """Updates the tasks.txt output file with strings generated from
    tasks in task_list"""
    task_file = open("tasks.txt", "w", encoding="utf-8")
    task_list_to_write = []
    for t in task_list:
        str_attrs = [
            t['username'],
            t['title'],
            t['description'],
            t['due_date'].strftime(DATETIME_STRING_FORMAT),
            t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
            "Yes" if t['completed'] else "No"
        ]
        task_list_to_write.append(";".join(str_attrs))
    task_file.write("\n".join(task_list_to_write))
    task_file.close()

def clear_screen():
    """Clears the screen to refresh display"""
    os.system("cls")

    # check that saving the task_list dictionary to selected_task allows changes.
    # IMPORTANT TO ACCESS & EDIT MAIN TEXT FILE ITSELF HERE

# PC - FILE CREATION

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

# PC - reads each string in the task txt file?
# PC - creates a list called task_data which is populated by the tasks?
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# PC - creates an empty list called task_list
# PC - for each string in task_data, create a current task dictionary?
task_list = []
for t_str in task_data:
    curr_t = {}
    # create current task dictionary and adds values from task_components
    # task_components is a list created by splitting the input strings
    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
"""This code reads usernames and password from the user.txt file to
 allow a user to login."""

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read user.txt and create a list containing a string
# for each line of input
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Separate user names and passwords and add to a dictionary
# with usernames as keys and passwords as values.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        clear_screen()
        print("Login successful!")
        logged_in = True

#  MAIN PROGRAM ROUTINE
while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following options below:\n
r -  Register a user
a -  Add a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e -  Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == 'gr':
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':

        # Put the below in a function
        # Generate the info below from tasks.txt and user.txt
        # Generate these files if they don't already exist
        # (PC - aren't they generated at the start?)
        # because user has not selected to generate them yet
        # call the code to generate the txt files
        '''If the user is an admin they can display statistics about number of users
        and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice. Please Try again")
