"""This program is a task management tool which reads data from
tasks.txt and user.txt and allows users to:
- register new users
- add new tasks
- view all tasks
- view their own assigned tasks
- mark own tasks as completed
- reassign own incomplete tasks to other users
- edit the due date for own incomplete tasks
- generate task and user overview statistical reports as .txt files
- display number of users and tasks (if user is admin)
All additions and changes are written to tasks.txt or user.txt
"""

# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code
# otherwise the program will look in your root directory for the
# text files.


#=====importing libraries===========
import os
from datetime import datetime, date
from tabulate import tabulate

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# FUNCTIONS

# Functions to add users and tasks:

def reg_user():
    '''Collect user input, verify that it meets conditions and then 
    write new user data to the user.txt file'''

    print("\033[1mRegister a new user\033[0m")

    # Loop until new_username meets required conditions.
    new_username = input("\nNew Username (5 - 15 characters, no spaces): ")
    while True:
        if new_username in username_password.keys():
            new_username = input("\nThat username already exists. "
                                 "Please enter another: ")
        elif len(new_username) < 5 or len(new_username) > 15:
            new_username = input("\nPlease enter a username with between "
                                 "5 and 15 characters: ")
        elif " " in new_username:
            new_username = input("\nPlease enter a username that does not "
                                 "contain spaces: ")
        else:
            break

    # Loop until new_password meets required conditions.
    while True:
        new_password = input("\nNew Password (8 - 20 characters, "
                             "no spaces): ")
        while True:
            if len(new_password) < 8 or len(new_password) > 20:
                new_password = input("\nPlease enter a password with between "
                                     "8 and 20 characters: ")
            elif " " in new_password:
                new_password = input("\nPlease enter a password that does "
                                     "not contain spaces: ")
            elif new_password == new_username:
                new_password = input("\nPlease enter a password that is "
                                     "different from your username: ")
            else:
                break

        confirm_password = input("\nConfirm Password: ")

        # When confirm_password matches new_password, write username
        # and password to user.txt, else return to start of loop.
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
        - the name of the user to assign the task to,
        - the title of the task,
        - the description of the task and 
        - the due date of the task.'''

    print("\033[1mAdd a task\033[0m")

    # Loop until user enters the username of a registered user.
    # If not registered, display a list of registered users
    # and reprompt.
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
        task_title = input("\nTitle of task (max 60 characters): ")
        if not task_title:
            print("\nPlease enter a title for this task.")
        elif len(task_title) > 60:
            print("\nTitle too long - maximum length is 60 characters.")
        else:
            break

    task_description = input("\nDescription of task: ")

    # Get the current date.
    curr_date = date.today()

    # Loop until due date is in the correct format and is >= today.
    while True:
        try:
            task_due_date = input("\nDue date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date,
                                              DATETIME_STRING_FORMAT)
        except ValueError:
            print("\nInvalid datetime format. Please use the format "
                  "specified.")
            continue
        if due_date_time.date() < curr_date:
            print("\nPlease set a due date of today or later.")
        else:
            break

    # Add input values to a new_task dictionary and append to task_list
    # Loop through task_list and create list of ';'- separated strings.
    # Write the data to task.txt, with each task on a new line.
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
    '''Reads the tasks from the task list generated from task.txt file
    and, for each task, calls the function display_task() to display
    task details to the console. Presents a menu to the user giving the
    option to switch between detailed and summary views of the tasks.'''

    while True:

        # If task_list is empty, inform user and exit function.
        if not task_list:
            print("\n** No tasks have been created yet. **\n")
            return

        # Loop through task_list and call display_task() for each task.
        print("\n\033[1mAll tasks (detailed view):\033[0m\n")
        for i, t in enumerate(task_list, start=1):
            print(f"Task {i}")
            display_task(t)
        current_view = "detailed"
        print(f"Total number of tasks (all users): {len(task_list)}")

        # Give user the option to toggle between detailed and summary
        # list views or to return to the main menu.
        while True:

            change_view = input("\nOptions:\nv - toggle detailed / "
                                "summary view\nq - return to the "
                                "main menu\n: ")

            if change_view.lower() not in ["q", "v"]:
                print("\nPlease enter a valid letter.")
                continue

            if change_view.lower() == "q":
                clear_screen()
                return

                # if user selects summary view, call the summary_view
                # function and reset current_view to "summary"
            if change_view.lower() == "v" and current_view == "detailed":
                clear_screen()
                print("\n\033[1mAll tasks (summary view)\033[0m\n")
                summary_view(task_list)
                current_view = "summary"
                continue

                # if user selects detailed view, exit this loop and
                # return to start of view_mine() loop with default
                # detailed view.
            if change_view.lower() == "v" and current_view == "summary":
                clear_screen()
                break

        continue


def display_task(selected_task):
    """Displays the details of a selected task passed as an argument"""

    disp_str = ("-------------------------------------------------------------"
                "----------------\n")
    disp_str += f"Task: \t\t {selected_task['title']}\n"
    disp_str += f"Assigned to: \t {selected_task['username']}\n"
    disp_str += f"""Date Assigned: \t {selected_task['assigned_date'].strftime(
        DATETIME_STRING_FORMAT)}\n"""
    disp_str += f"""Due Date: \t {selected_task['due_date'].strftime(
        DATETIME_STRING_FORMAT)}\n"""
    disp_str += f"""Task complete? \t {'Yes' if (
        selected_task['completed']) else 'No'}\n"""
    disp_str += f"Task Description: \n {selected_task['description']}\n"
    disp_str += ("-------------------------------------------------------------"
                 "----------------\n")
    print(disp_str)


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
                   headers=["No.", "Task", "Completed?", "Due date"]) + "\n\n")


def view_mine():
    '''Reads the tasks from a user-specific task list generated from 
    task.txt and, for each task, prints a task number and calls
    display_task(). Allows user to toggle between detailed and summary
    views and to select a task for editing.'''

    def view_mine_options():
        """Displays view / edit options to user"""
        print("\033[1mView / edit options:\033[0m")
        print("\n   - enter the number of an uncompleted task to edit "
                   f"({incomplete_count} remaining of "
                   f"{len(user_task_list)} assigned tasks)"
                    if len(user_task_list) > 1 else
                   " 1 - edit the above task if not marked as completed")
        print(" v - toggle between detailed and summary view")
        print("-1 - return to the main menu: ")

    while True:

        # Loop through task_list and append current user's tasks
        # to user_task_list.
        user_task_list = []
        for t in task_list:
            if t['username'] == curr_user:
                user_task_list.append(t)

        # If user_task_list is empty, inform user and
        # return to main menu.
        if not user_task_list:
            print(f"** You do not have any assigned tasks {curr_user}. **")
            return

        # For each task in user_task_list, print a task number and pass
        # task to display_task() to display.  Count number of user's
        # complete and incomplete tasks and call view_mine_options()
        # to display options to user
        complete_count = 0
        incomplete_count = 0
        print("\n\033[1mMy tasks (detailed view):\033[0m\n")
        for i, t in enumerate(user_task_list, start=1):
            if t["completed"]:
                complete_count += 1
            else:
                incomplete_count += 1
            print(f"Task No: {i}")
            display_task(t)
        current_view = "detailed"
        view_mine_options()

        # Loop until user chooses to return to main menu or
        # toggles view back to default detailed list,
        while True:

            user_select = input("\nPlease enter your choice: ")

            if user_select.lower() == "-1":
                # Clear screen and return to main menu.
                clear_screen()
                return

            if user_select.lower() == "v" and current_view == "detailed":
                # Switch to summary view of all user's tasks.
                clear_screen()
                print("\n\033[1mMy tasks (summary view):\033[0m\n")
                summary_view(user_task_list)
                current_view = "summary"
                view_mine_options()
                continue

            if user_select.lower() == "v" and current_view == "summary":
                # Switch to default detailed view by returning to start
                # of current function.
                clear_screen()
                break

                # If input is numeric, cast as Int and check that it is
                # within the range of displayed task numbers.
            if user_select.isnumeric():
                user_select = int(user_select)
                while user_select < 1 or user_select > len(user_task_list):
                    # if user only has one task and enters a
                    # number, select it by default.
                    if len(user_task_list) == 1:
                        user_select = 1
                    else:
                        user_select = input("Please enter a task number "
                                            "between 1 and "
                                        f"{len(user_task_list)}: ")
                        user_select = int(user_select)
                clear_screen()
                # Loop through task_list to find the task matching the
                # user's selected task and store this as
                # selected_task to allow changes to the task.
                for t in task_list:
                    if t == user_task_list[user_select-1]:
                        selected_task = t
                # If the selected task is already marked as complete,
                # inform user that it can no longer be edited.
                if selected_task["completed"] is True:
                    print("\n** The selected task has already been marked as "
                        "complete and can no longer be edited. **")
                    input("\nPlease press Enter to return to your list of "
                          "tasks: ")
                    clear_screen()
                    break

                # Else, display selected task and editing menu.
                print("\033[1mSelected task:\033[0m\n")
                display_task(selected_task)
                editing_menu(selected_task)
                # After returning from editing_menu, break this inner
                # loop and continue to start of view_mine() loop.
                break

            print("\nInvalid choice")
            continue

        continue


def editing_menu(selected_task):
    """Displays a menu to the user and directs to the relevant function
    allowing the task to be edited. Accepts 1 argument - the task
    dictionary selected for editing"""

    while True:

        # If task has been marked as complete, return to view_mine()
        if selected_task['completed'] is True:
            return

        # Display editing options to the user.
        print("\nOptions:\n"
        "c - mark this task as completed\n"
        "u - change the assigned user\n"
        "d - change the due date\n"
        "r - return to my task list\n")

        vm_choice = input("Please enter a letter: ")

        while vm_choice.lower() not in ["c", "u", "d", "r"]:
            vm_choice = input("\nPlease enter a valid letter: ")

        if vm_choice.lower() == "c":
            mark_complete(selected_task)
            continue

        if vm_choice.lower() == "u":
            clear_screen()
            # call function to edit assigned user.
            exit_editing = edit_assigned_user(selected_task)
            # check the return value of edit_assigned_user
            # if True (assigned to a different user) return to
            # view_mine()
            if exit_editing:
                return
            continue

        if vm_choice.lower() == "d":
            edit_due_date(selected_task)
            continue

        if vm_choice.lower() == "r":
            # return to current user's task list
            clear_screen()
            return


# Functions for editing tasks:


def mark_complete(selected_task):
    """Marks a selected task as completed, if not already marked as such,
    and calls the update_output function to update the output file."""

    # If user confirms choice, mark selected task as complete.
    # Inform user whether change has been made, redisplay task
    # and exit function.
    print("\nPlease note: once marked as completed, the selected task "
        "can no longer be edited.")
    while True:
        confirm_complete = input("\nPlease type 'y' to confirm task "
                                "completion or 'n' to go back: ")

        if confirm_complete.lower() == "y":
            selected_task['completed'] = True
            update_output()
            clear_screen()
            print("\nThe selected task has now been marked as completed "
                    "and can no longer be edited.\n")
            input("Please press Enter to return to your list of tasks: ")
            clear_screen()
            return

        if confirm_complete.lower() == "n":
            clear_screen()
            print("\nNo change has been made - the task is "
                    "still active.\n")
            display_task(selected_task)
            return

        print("\nPlease select a valid option.")


def edit_assigned_user(selected_task):
    '''Allow user to reassign an uncompleted task to a different
    user. Takes one argument - the selected task dictionary.
    Returns True to allow code in editing_menu() to return the user
    directly to view_mine()'''

    # Display list of registered users and prompt user to enter new
    # assigned user's name until input matches a key in
    # username_password.
    while True:
        print("\n\033[1mRegistered users:\033[0m\n")
        for r_user in username_password.keys():
            print(f"{r_user}")
        changed_user = input("\nWho would you like "
                        "to assign this task to?\n: ")

        # If user attempts to reassign to self, inform them and return
        # to editing_menu()
        if changed_user == selected_task['username']:
            clear_screen()
            print("\n** You are already assigned to this task"
                " - no change has been made. **\n")
            display_task(selected_task)
            return False

        # If input user name is a registered user, change the
        # username value in the selected task dictionary.
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
    input("\nPlease press Enter to continue: ")
    clear_screen()
    return True


def edit_due_date(selected_task):
    """Allows user to change the due date of a selected task.
    Checks new due date is valid and calls update_output() to
    write changes to the tasks.txt output file. Accepts 1 argument -
    the task dictionary to be edited."""

    # Loop until user has entered a new due date that is in
    # the correct format and >= today.
    while True:
        try:
            changed_due_date = input("\nPlease enter a new due date "
                                        "for this task (YYYY-MM-DD): ")
            selected_task['due_date'] = datetime.strptime(
                changed_due_date, DATETIME_STRING_FORMAT)
        except ValueError:
            print("\nInvalid datetime format. Please use the format "
                    "specified")
            continue

        if selected_task['due_date'].date() < date.today():
            print("\nPlease set a due date of today or later.")
        else:
            break

    # Update tasks.txt with new data, clear screen and display
    # confirmation of the change made to due date.
    update_output()
    clear_screen()
    print("The due date for this task has now been updated "
            f"to {selected_task['due_date'].date()}.\n")
    display_task(selected_task)
    return


def generate_reports():
    """Generates two .txt reports: task_overview.txt and 
    user_overview.txt"""
    generate_task_overview()
    generate_user_overview()
    clear_screen()
    print("\nUser and task overview reports have been generated.\n"
          "They can be found in the current folder and are named:\n" 
          "\ttask_overview.txt\n\tuser_overview.txt")

def generate_task_overview():
    '''Generates a .txt file containing the following data:
       - total number of tasks in task_list
       - total number of completed tasks
       - total number of uncompleted tasks
       - total number of overdue tasks
       - percentage of tasks that are incomplete
       - percentage of tasks that are overdue'''

    # Calculate task overview report data.
    no_tasks = len(task_list)
    no_completed = 0
    no_overdue = 0
    for t in task_list:
        if t['completed'] is True:
            no_completed += 1
        if t['completed'] is False and (t['due_date'].date() <
                                        datetime.today().date()):
            no_overdue += 1
    no_incomplete = no_tasks - no_completed
    if not task_list:
        percent_incomplete = None
        percent_overdue = None
    else:
        percent_incomplete = round((no_incomplete / no_tasks  *100), 1)
        percent_overdue = round((no_overdue / no_tasks * 100), 1)

    # Write task overview report to output file.
    with open("task_overview.txt", "w", encoding = "utf-8") as t_rpt:
        t_rpt.write("Task overview:\t\t\t\t\t\t\t\t\t\t\t\tReport generated: "
                    f"""{datetime.strftime(
                        datetime.today(),'%Y-%m-%d %H:%M:%S' )}\n""")
        if not task_list:
            t_rpt.write("\nNo tasks exist so no data has been generated.")
        else:
            t_rpt.write("\nTotal tasks in task list:\t\t\t\t\t"
                        f"{no_tasks}\n")
            t_rpt.write("\nNumber of completed tasks:\t\t\t\t\t"
                        f"{no_completed}\n")
            t_rpt.write("\nNumber of incomplete tasks:\t\t\t\t\t"
                        f"{no_incomplete}\n")
            t_rpt.write("\nNumber of overdue incomplete tasks:\t\t\t"
                        f"{no_overdue}\n")
            t_rpt.write(
                ("\nPercentage of tasks that are incomplete:\t"
                f"""{'N/a' if percent_incomplete is None else (
                f'{percent_incomplete} %')}\n""")
                    )
            t_rpt.write(
                ("\nPercentage of tasks that are overdue:\t\t"
                f"""{'N/a' if percent_overdue is None else (
                f'{percent_overdue} %')}""")
                    )


def generate_user_overview():
    '''Generates a .txt file containing the following statistics:
          - total number of registered users
          - total number of tasks in task_list
          - for each user:
            - total number of tasks assigned to them
            - percentage of total tasks assigned to them
            - percentage of their assigned tasks that are completed
            - percentage of their assigned tasks that are incomplete
            - percentage of their assigned tasks that are overdue'''

    num_tasks = len(task_list)
    # Write totals section of overview report to output file
    with open("user_overview.txt", "w", encoding = "utf-8") as u_rpt:
        u_rpt.write("User overview:\t\t\t\t\t\t\t\t\t\t\t\tReport generated: "
            f"{datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')}\n")
        u_rpt.write(f"\nNumber of registered users:\t\t{len(user_data)}")
        u_rpt.write(f"\nTotal tasks in task list:\t\t{num_tasks}\n")

        # For each user in username_password:
        # Loop through tasks in task_list and increment counters
        # when relevant conditions are met.
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
            if not task_list:
                percent_of_total = None
            else:
                percent_of_total = round(num_user_tasks / num_tasks * 100, 1)

            # If number of a user's assigned tasks == 0, meaning the
            # following calculations fail, set values to None.
            try:
                u_percent_comp = round(
                    num_comp_tasks / num_user_tasks * 100, 1
                    )
            except ZeroDivisionError:
                u_percent_comp = None
            try:
                u_percent_incomp = round(
                    num_incomp_tasks / num_user_tasks * 100, 1
                    )
            except ZeroDivisionError:
                u_percent_incomp = None
            try:
                u_percent_overdue = round(
                    num_overdue_tasks / num_incomp_tasks * 100, 1
                    )
            except ZeroDivisionError:
                u_percent_overdue = None

            # For each user in username_password, write the following
            # data to the output file.  Show "N/a" where zero sum
            # division errors above meant values were set to None.
            u_rpt.write(f"\nUser: {u}")
            u_rpt.write("\n-------------------")
            u_rpt.write(f"\nTasks assigned:\t{num_user_tasks}")
            u_rpt.write(
                        ("\nPercentage of all tasks:\t\t\t\t\t"
                        f"""{'N/a' if percent_of_total is None else (
                        f'{percent_of_total} %')}""")
                        )
            u_rpt.write(
                        ("\nPercentage of assigned tasks completed:\t\t"
                        f"""{'N/a' if u_percent_comp is None else (
                        f'{u_percent_comp} %')}""")
                        )
            u_rpt.write(
                        ("\nPercentage of assigned tasks incomplete:\t"
                        f"""{'N/a' if u_percent_incomp is None else (
                        f'{u_percent_incomp} %')}""")
                        )
            u_rpt.write(
                        ("\nPercentage of incomplete tasks overdue:\t\t"
                        f"""{'N/a' if u_percent_overdue is None else (
                        f'{u_percent_overdue} %')}\n""")
                        )


def display_stats():
    '''Allows the admin user to display statistics 
    about number of users and tasks, generated from user.txt and
    tasks.txt.'''

    # Generate tasks.txt and user.txt if they don't already exist.

    if not os.path.exists("user.txt"):
        with open("user.txt", "w", encoding="utf-8") as user_input:
            default_file.write("admin;password")

    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w", encoding="utf-8") as task_input:
            pass

    # Generate the info below from tasks.txt and user.txt
    # call the code to generate the txt files.

    with open("user.txt", "r", encoding="utf-8") as user_input:
        user_count = len(user_input.readlines())

    with open("tasks.txt", "r", encoding="utf-8") as task_input:
        task_count = len(task_input.readlines())

    print("\nUsage statistics:")
    print("\n------------------------------------")
    print(f"Number of users: \t\t {user_count}")
    print(f"Number of tasks: \t\t {task_count}")
    print("------------------------------------\n")


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
    """Clears the screen to refresh the display"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


# ==== Start of program ====

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
    curr_t['due_date'] = datetime.strptime(task_components[3],
                                           DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4],
                                                DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# ====Login Section====

# Read usernames and passwords from user.txt and store values in
# username_password dictionary.

# If no user.txt file exists, write one with a default account.
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
print("If you do not have an account, please ask a registered user "
      "to add you.\n")

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

# ==== MAIN PROGRAM ROUTINE ====

menu = True
while menu:
    # presents the menu to the user and converts input to lower case.
    print("\n\033[1mMain menu:\033[0m\n")
    menu = input('''Select one of the following options below:\n
    r -  Register a user
    a -  Add a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
    ds - Display statistics (admin only)
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

    elif menu == 'ds':
        if curr_user == 'admin':
            clear_screen()
            display_stats()
        else:
            clear_screen()
            print("\n** Sorry, only the Admin user is able to display "
                  "this report. **")

    elif menu == 'e':
        clear_screen()
        print("Thank you for using this task management program.\n")
        exit()

    else:
        clear_screen()
        print("\nYou have entered an invalid option. Please try again.")
