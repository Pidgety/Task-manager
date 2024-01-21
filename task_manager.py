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
from tabulate import tabulate

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# FUNCTIONS

# Menu functions:

def main_menu():
    """Presents the main menu to the user and calls relevant functions
    depending on user choice"""
    while True:
        # presents the menu to the user and converts input to lower case.
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
            clear_screen()
            reg_user()

        elif menu == 'a':
            clear_screen()
            add_task()

        elif menu == 'va':
            clear_screen()
            view_all()

        elif menu == 'vm':
            clear_screen()
            view_mine()

        elif menu == 'gr':
            clear_screen()
            generate_reports()

        elif menu == 'ds' and curr_user == 'admin':
            clear_screen()
            display_stats()

        elif menu == 'e':
            clear_screen()
            print('Thank you for using this task management program.')
            exit()

        else:
            clear_screen()
            print("You have entered an invalid option. Please try again.")


# Functions to add users and tasks:

def reg_user():
    '''Add a new user to the user.txt file'''

    print("\033[1mRegister a new user\033[0m")
    # Loop until user enters a username that is not already in the
    # list of registered users.
    new_username = input("\nNew Username: ")
    while True:
        if new_username in username_password.keys():
            new_username = input("\nThat username already exists. Please enter another: ")
        else:
            break

    # Loop until new_password and confirm_password match.
    # When they match, add new_username and new_password to
    # username_password dictionary and write dictionary to
    # users.txt output file.
    while True:
        new_password = input("\nNew Password: ")
        confirm_password = input("Confirm Password: ")

        if new_password == confirm_password:
            username_password[new_username] = new_password
            clear_screen()
            print(f"\nNew user successfully added: {new_username}")

            with open("user.txt", "w", encoding="utf-8") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))
            break
        print("\nPasswords do not match. Please enter your password again.")


def add_task():
    '''Allow user to add a new task to task.txt file
    Prompt user for the following: 
        - the user to assign the task to,
        - the title of the task,
        - the description of the task and 
        - the due date of the task.'''

    print("\033[1mAdd a task\033[0m")

    # Loop until user enters the username of a registered user.
    # If not registered, display a list of registered users.
    while True:
        task_username = input("\nUser to be assigned to the task: ")
        if task_username not in username_password.keys():
            print(f"\n{task_username} is not a registered user.\n"
                  "\nPlease enter a name from the list below.")
            print("\n\033[1mRegistered users:\033[0m\n")
            for r_user in username_password.keys():
                print(f"{r_user}")
            continue
        break

    # Loop until 0 < len(task_title) <= 60.
    while True:
        task_title = input("\nTitle of Task (max 60 characters): ")
        if not task_title:
            print("\nPlease enter a title for this task.")
        elif len(task_title) > 60:
            print("\nTitle too long - maximum length is 60 characters.")
        else:
            break
    # add code to check the title is not already in the list for the assigned user
    # if it is, prompt user to choose a different title
    task_description = input("\nDescription of Task: ")

    # Get the current date.
    curr_date = date.today()

    # Loop until due date is in the correct format and is >= today.
    while True:
        try:
            task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("\nInvalid datetime format. Please use the format specified.")
            continue
        if due_date_time.date() < curr_date:
            print("\nPlease set a due date of today or later.")
        else:
            break

    # Add input values to a new_task dictionary and append to task_list
    # Loop through task_list and create list of ';'- separated strings.
    # Write the data to task.txt with each task on a new line.
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
    clear_screen()
    print("\nTask successfully added.")


# Functions to view tasks:

def view_all():
    '''Reads the task from the task list generated from task.txt file 
    and prints to the console in the format of Output 2 presented in the
    task pdf (i.e. includes spacing and labelling) '''

    # If task_list is empty, inform user and exit function.
    if not task_list:
        print("\nNo tasks have been created yet.\n")
        return

    # Loop through task_list and call display_task for each task.
    print("\n\033[1mAll tasks (detailed view):\033[0m\n")
    for i, t in enumerate(task_list, start=1):
        print(f"Task {i}")
        display_task(t)
    current_view = "detailed"
    print(f"{len(task_list)} tasks displayed above.\n")

    while True:
        change_view = input("\nEnter 'v' to toggle between detailed and "
                            "summary view\n or 'q' to return to the "
                            "main menu: ")
        if change_view.lower() == "v" and current_view == "detailed":
            clear_screen()
            print("\n\033[1mAll tasks (summary view)\033[0m\n")
            summary_view(task_list)
            current_view = "summary"
        elif change_view.lower() == "v" and current_view == "summary":
            clear_screen()
            view_all()
        elif change_view.lower() == "q":
            main_menu()
        else:
            print("\nPlease enter a valid letter.")
            continue

# PC - check that the below can be used to view individual tasks
def display_task(selected_task):
    """Displays the details of the selected task passed as an argument"""

   # print("\n\033[1mTask details:\033[0m\n")
    disp_str = ("-------------------------------------------------------------"
                "----------------\n")
    disp_str += f"Task: \t\t {selected_task['title']}\n"
    disp_str += f"Assigned to: \t {selected_task['username']}\n"
    disp_str += f"Date Assigned: \t {selected_task['assigned_date'].strftime(
        DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Due Date: \t {selected_task['due_date'].strftime(
        DATETIME_STRING_FORMAT)}\n"
    disp_str += f"Task complete? \t {"Yes" if selected_task['completed'] else "No"}\n"
    disp_str += f"Task Description: \n {selected_task['description']}\n"
    disp_str += ("-------------------------------------------------------------"
                 "----------------\n")
    print(disp_str)
    # editing_menu(selected_task)

def summary_view(list_name):
    """Loops through the list of tasks passed as an argument and
    displays a table containing a one-row summary of each task
    with an accompanying number)"""

    table_data = []
    for i, t in enumerate(list_name, start=1):
        table_data.append([i,
                           t['title'],
                           "yes" if t['completed'] is True else "no", 
                           t['due_date'].strftime(DATETIME_STRING_FORMAT)])
    print(tabulate(table_data,
                   headers=["No.", "Task", "Completed?", "Due date"]))


def view_mine():
    '''Reads the tasks from a user-specific task list generated from 
    task.txt and prints to the console in the format of Output 2
    presented in the task pdf (i.e. includes spacing and labelling)'''

    # Loop through task_list and append user's tasks to user_task_list
    user_task_list = []
    for t in task_list:
        if t['username'] == curr_user:
            user_task_list.append(t)

    # If user_task_list is empty, inform user and exit function.
    if not user_task_list:
        print("You do not have any assigned tasks.\n")
        return

    # For each task in user_task_list, print a task number and pass
    # task to display_task()
    print("\n\033[1mMy tasks (detailed view):\033[0m\n")
    for i, t in enumerate(user_task_list, start=1):
        print(f"Task No: {i}")
        display_task(t)
    current_view = "detailed"
    print(f"\nYou currently have {len(user_task_list)} tasks assigned to you.")

    while True:

        print("\n\033[1mView / edit options:\033[0m")
        print(f"\n   - enter a task number (1 to {len(user_task_list)}) to edit"
        "\n v - toggle between detailed and summary view"
        "\n-1 - return to the main menu: ")
        user_select = input("\nPlease enter your choice: ")

        if user_select.lower() == "-1":
            # Clear screen and return to main menu.
            clear_screen()
            main_menu()

        elif user_select.lower() == "v" and current_view == "detailed":
            # Switch to summary view of all user's tasks.
            clear_screen()
            print("\n\033[1mMy tasks (summary view):\033[0m\n")
            summary_view(user_task_list)
            current_view = "summary"

        elif user_select.lower() == "v" and current_view == "summary":
            # Switch to default detailed view by returning to start
            # of current function.
            clear_screen()
            view_mine()

            # If input is numeric, cast as Int and check that it is
            # within the range of displayed task numbers.
            # If it is, use input to match the task to that in main
            # task_list and set task to selected_task, passing it to
            # display_task() and editing_menu().
        elif user_select.isnumeric():
            user_select = int(user_select)
            while user_select < 1 or user_select > len(user_task_list):
                user_select = input("\nPlease enter a task number "
                      f"between 1 and {len(user_task_list)}: ")
                user_select = int(user_select)
            clear_screen()
            for t in task_list:
                if t == user_task_list[user_select-1]:
                    selected_task = t
            print("\033[1mSelected task:\033[0m\n")
            display_task(selected_task)
            editing_menu(selected_task)

        else:
            print("\nInvalid choice")
            continue


def mark_complete(selected_task):
    """Marks a selected task as completed, if not already marked as such, 
    and calls the update_output function to update the output file."""

    # Inform user if the task has already been marked as complete.
    # Return to detailed view of selected task.
    if selected_task['completed'] is True:
        print("\nThis task has already been marked as completed "
              "and can no longer be edited.")
        display_task(selected_task)
    else:
        # If user confirms choice, mark selected task as complete.
        # Return to summary display.
        print("\nPlease note: once marked as completed, the selected task "
            "can no longer be edited.")
        while True:
            confirm_complete = input("\nPlease type 'y' to confirm task "
                                    "completion or 'n' to go back: ")
            if confirm_complete.lower() == "y":
                selected_task['completed'] = True
                update_output()
                print("\nThe selected task has now been marked as completed "
                        "and can no longer be edited.")
                break
            if confirm_complete.lower() == "n":
                print("\nNo change has been made - the task is "
                        "still active.")
                break
            print("\nPlease select a valid option.")
        view_mine()


def edit_assigned_user(selected_task):
    # Allow user to assign the current task to a different user.
    if selected_task['completed'] is True:
        # clear screen
        clear_screen()
        print("\nThis task is already marked as completed and can "
                "no longer be edited.")
        display_task(selected_task)

    # Display list of registered users and ask user to
    # enter new assigned user's name. If in username_password,
    # update relevant value in task_list.
    while True:
        print("\n\033[1mRegistered users:\033[0m\n")
        for r_user in username_password.keys():
            print(f"{r_user}")
        changed_user = input("\nWho would you like "
                        "to assign this task to: ")
        if changed_user in username_password.keys():
            selected_task['username'] = changed_user
            break
        clear_screen()
        print(f"\n{changed_user} is not a registered user.")

    # Write updated task_list to tasks.txt, print message
    # and return to summary display.
    update_output()
    clear_screen()
    print(f"\nAssigned user has been changed to {changed_user}.\n"
          "You can no longer edit this task.\n")
    view_mine()


def edit_due_date(selected_task):
    """Allows user to change the due date of a selected task.
    Checks new due date is valid and calls update_output() to
    write changes to the tasks.txt output file. Accepts 1 argument -
    the task dictionary to be edited."""
    # Allow user to change the due date.
    if selected_task['completed'] is True:
        # clear screen
        clear_screen()
        print("\nThis task is already marked as completed and can "
                "no longer be edited.")
        display_task(selected_task)

    # Loop until user has entered a new due date that is in
    # the correct format and >= today.
    while True:
        try:
            changed_due_date = input("Please enter a new due date "
                                        "for this task (YYYY-MM-DD): ")
            selected_task['due_date'] = datetime.strptime(
                changed_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("Invalid datetime format. Please use the format "
                    "specified")
            continue
        if selected_task['due_date'].date() < date.today():
            print("Please set a due date of today or later.")
        else:
            break
    # Update tasks.txt with new data, clear screen and display
    # confirmation of the change made to due date.
    update_output()
    clear_screen()
    print("The due date for this task has now been updated "
            f"to {selected_task['due_date'].date()}.")


def editing_menu(selected_task):
    """Displays a menu to the user and directs to the relevant function
    allowing the task to be edited. Accepts 1 argument - the task
    dictionary selected for editing"""
    # Display editing options to the user.
    print("\nOptions:\n"
        "c - mark this task as completed\n"
        "u - change the assigned user\n"
        "d - change the due date\n"
        "r - return to my task list\n"
        "q - return to the main menu\n")
    vm_choice = input("Please enter a letter: ")

    if vm_choice.lower() == "c":
        clear_screen()
        mark_complete(selected_task)

    elif vm_choice.lower() == "u":
        edit_assigned_user(selected_task)

    elif vm_choice.lower() == "d":
        edit_due_date(selected_task)

    elif vm_choice.lower() == "r":
        # return to current user's task list
        clear_screen()
        view_mine()
    elif vm_choice.lower() == "q":
        # return to main menu
        main_menu()
    else:
        # redisplay editing_menu
        print("\nPlease select a valid option.")
        editing_menu(selected_task)


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


def display_stats():
    '''If the user is an admin they can display statistics about number of users
    and tasks.'''

    # Generate tasks.txt and user.txt if they don't already exist
    # because user has not selected to generate them yet

    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as user_input:
            default_file.write("admin;password")

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as task_input:
            pass

    # Generate the info below from tasks.txt and user.txt
    # call the code to generate the txt files

    with open("user.txt", "r", encoding="utf-8") as user_input:
        user_count = len(user_input.readlines())

    with open("tasks.txt", "r", encoding="utf-8") as task_input:
        task_count = len(task_input.readlines())

    print("\nUsage statistics:")
    print("\n-----------------------------------")
    print(f"Number of users: \t\t {user_count}")
    print(f"Number of tasks: \t\t {task_count}")
    print("-----------------------------------\n")


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

# Default file creation:

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w", encoding="utf-8") as default_file:
        pass

# Create a list of task strings read from the tasks.txt input file
with open("tasks.txt", 'r', encoding="utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# Creates an empty list called task_list, and for each line in input
# file, split data into components and store in a dictionary before
# appending to task_list.
task_list = []
for t_str in task_data:
    curr_t = {}
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)


#====Login Section====
# Read usernames and passwords from user.txt and store values in
# username_password dictionary.

# If no user.txt file exists, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w", encoding="utf-8") as default_file:
        default_file.write("admin;password")

# Read user.txt and create a list of input line strings
with open("user.txt", 'r', encoding="utf-8") as user_file:
    user_data = user_file.read().split("\n")

# Separate user names and passwords and add to a dictionary
# with usernames as keys and passwords as values.
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

print("\n\033[1mWelcome to this task management program.\033[0m\n")
print("If you do not have an account, please ask a registered user to add you.\n")

logged_in = False
while not logged_in:

    print("Please enter your login details below.\n")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("\nThat username does not exist.")
        continue
    if username_password[curr_user] != curr_pass:
        print("\nIncorrect password.")
        continue
    clear_screen()
    print("Login successful!")
    logged_in = True

#  MAIN PROGRAM ROUTINE:

main_menu()
