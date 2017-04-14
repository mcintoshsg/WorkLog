# Timesheet class - for entering employee time worked on a specifi project task
# class attributes
#
#    employee name - string
#    project working on - string
#    task performed - string
#    time / date started - datetime
#    effort duration - datetime
#    time / dare completed - datetime
#    total hours logged - datetime
#    associated notes - string
#
#    time sheet storage example:
#
#        TimeSheets[{'Employee Name' : Stuart McIntosh, 'Project Name' ; 'ATOM',
#                       'Task Performed' : Developed word order', 'DateTime Started' :
#                            22/11/63 12:30, 'DateTime Completed' : '22/11/63 14:30',
#                        Total Time Taken : 2, Work Notes : 'JHGJHGJHGJH'}]
#
# class methods
#
# add / delete / edit a timesheet
# search method - find by date, name, task, project, time or a regex
# display method - display all the timesheet 1:1
# calucate hours method - number of hours / minutes on a single project, task, date etc...
# total number of minutes / hours / days worked etc...
import collections
import csv
import datetime
import os
import os.path
import random
import re
import sys

from utils import clear_screen
from timesheet_constants import Constants


class TimeSheet:

    # timesheet class - whcih logs and tracks individuals work done
    timesheets = []  # hold all timesheets
    employee_name = ''
    project = ''
    task = ''
    time_started = datetime
    time_completed = datetime
    total_time = ''
    time_str = ''
    notes = ''
    total_minutes = ''

    def __init__(self):
        # open worklog file and load previously saved timesheets
        file_path = 'timesheets.csv'
        if os.path.exists(file_path):
            open_type = 'r'
        else:
            open_type = 'w+'
            Constants.FIRST_USE = True
        with open(file_path, open_type, newline = '') as csvfile:
            timesheet_reader = csv.DictReader(csvfile, delimiter = ',')
            self.timesheets = list(timesheet_reader)
        csvfile.close()

    # displays the various menus
    def display_menu(self, menu_layout, choice_menu):
        while True:
            clear_screen()
            if menu_layout == Constants.TIMESHEET_MENU:
                print(Constants.BANNER)
            print(menu_layout)
            choice = input("Enter an option: ")
            action = choice_menu.get(choice)
            if action:
                action()
            else:
                input("\n{} is not a valid choice, press enter to continue: ".format(choice))

    # main loop for the work logger
    def timesheet_run(self):
        clear_screen()
        self.timesheet_choices = {
            '1': self.add_timesheet,
            '2': self.display_timesheets,
            '3': self.search_timesheets,
            '4': self.modify_delete_timesheet,
            '5': self.quit
            }

        while True:
            if Constants.FIRST_USE:
                start = input('\n\nAs this is the first time, you need to add in your first timesheet! Press enter to continue or q to quit : ')
                if start.upper() == 'Q':
                    sys.exit()
                else:
                    self.add_timesheet()
                    Constants.FIRST_USE = False
            else:
                self.display_menu(Constants.TIMESHEET_MENU, self.timesheet_choices)
                choice = input("Enter an option: ")
                action = timesheet_choices.get(choice)
                if action:
                    action()
                else:
                    input("\n{} is not a valid choice, press enter to continue: ".format(choice))

    def quit(self):
        # before we quit we need to write back all the changes we made to the file
        field_names = self.timesheets[0].keys()
        with open('timesheets.csv', 'w+', newline = '') as csvfile:
            timesheet_writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter= ',')
            timesheet_writer.writeheader()
            for timesheet in self.timesheets:
                timesheet_writer.writerow(timesheet)
        csvfile.close()

        sys.exit()

    # add a new time sheet entry the emplyee name, project, date/time started etc...
    def add_timesheet(self):
        clear_screen()
        worklog = {} # individual work log

        self.employee_name = self.get_employee_name()
        worklog.update({'Employee Name': self.employee_name})
        self.project = self.get_project().upper()
        worklog.update({'Project Name': self.project})
        self.task = self.get_task()
        worklog.update({'Task Completed': self.task})
        self.time_started = self.get_time_started()
        worklog.update({'Time Started': self.time_started.strftime('%d/%m/%y %H:%M')})
        self.time_completed = self.get_time_completed(self.time_started)
        worklog.update({'Time Completed': self.time_completed.strftime('%d/%m/%y %H:%M')})
        self.total_seconds, self.time_str = self.get_total_time()
        worklog.update({'Total Time': self.total_seconds})
        worklog.update({'Total Time Str': self.time_str})
        self.notes = self.get_notes()
        worklog.update({'Notes': self.notes})

        self.timesheets.append(worklog)
        input("\nTimesheet entry complete, press enter to return to main menu : ")

    def display_timesheets(self):
        search_message = 'Displaying all logged timesheets!\n'
        self.display_results(self.timesheets, search_message)


    # list out a subset of the timesheet entries and allow the end user to either
    # modify or delete the timesheet
    # must question the end user to ensure he/she is really wanting to remove
    def modify_delete_timesheet(self):
        clear_screen()
        # display all timesheets one-by-one pausing to allow and action
        for count, x in enumerate(self.timesheets):
            print(Constants.GREEN + '*******************************************\n')
            print(Constants.GREEN + '   Employee Name: {} | Project Name: {} | Task Completed: {}\n'.format(x['Employee Name'],x['Project Name'], x['Task Completed']))
            print(Constants.GREEN + '   Time Started: {} | Time Taken: {}'.format(x['Time Started'], x['Total Time Str']))
            print(Constants.GREEN + '   Notes: {}\n'.format(x['Notes']))
            choice = input(Constants.ENDC + '\n\nPress enter to review next timesheet or M to modify or D to delete : ')
            if choice.upper() == 'M':
                mod_entry = self.modify_timesheet(self.timesheets[count])
                self.timesheets[count] = mod_entry
                break
                # display a list of fields and allow the user to choose which entery he wants to modify
            elif choice.upper() == 'D':
                yes_no = input('Are you sure you want to delete this timesheet? Y/N : ')
                if yes_no.upper().strip() == 'Y':
                    self.timesheets.pop(count)
                else:
                    break
            else:
                continue


    def modify_timesheet(self, ts_entry):
        # list out all the fields that can be changed
        # cannot change duration as this a calculated field
        mod_list = []

        while True:
            try:
                field_name = input('Please enter the field name you would like to change i.e. "'"Employee Name"'" : ').strip()
                if field_name == '':
                    raise Exception('You must enter a field name! Press enter to continue.')
                elif field_name.upper() == 'TIME TAKEN':
                    raise Exception('You cannot modfiy the time taken field.')
                elif field_name.upper() == 'EMPLOYEE NAME':
                    field_entry = self.get_employee_name()
                    ts_entry.update({'Employee Name': field_entry})
                    return ts_entry
                elif field_name.upper() == 'PROJECT NAME':
                    field_entry = self.get_project().upper()
                    ts_entry.update({'Project Name': field_entry})
                    return ts_entry
                elif field_name.upper() == 'TASK COMPLETED':
                    field_entry = self.get_task()
                    ts_entry.update({'Task Completed':field_entry})
                    return ts_entry
                elif field_name.upper() == 'NOTES':
                    field_entry = self.get_notes()
                    ts_entry.update({'Notes':field_entry})
                    return ts_entry
                elif field_name.upper() == 'TIME STARTED':
                    field_entry = self.get_time_started()
                    while True:
                        if field_entry >= datetime.datetime.strptime(ts_entry['Time Completed'], '%d/%m/%y %H:%M'):
                            raise Exception('\nYou cannot start the task after it was completed! : Time Started {} / Time Completed {}'.format(field_entry, ts_entry['Time Completed']))
                        else:
                            ts_entry.update({'Time Started': field_entry.strftime('%d/%m/%y %H:%M')})
                            time_taken = datetime.datetime.strptime(ts_entry['Time Completed'], '%d/%m/%y %H:%M') - datetime.datetime.strptime(ts_entry['Time Started'], '%d/%m/%y %H:%M')

                            time_taken_seconds = time_taken.total_seconds()
                            m, s = divmod(time_taken_seconds, 60)
                            h, m = divmod(m, 60)
                            #d, h = divmod(h, 24)
                            time_str = '{} hours {} minutes'.format(h,m)

                            ts_entry.update({'Total Time' : time_taken_seconds})
                            ts_entry.update({'Total Time Str': time_str})
                            break
                elif field_name.upper() == 'TIME COMPLETED':
                    field_entry = self.get_time_completed(datetime.datetime.strptime(ts_entry['Time Started'], '%d/%m/%y %H:%M'))
                    while True:
                        if field_entry <= datetime.datetime.strptime(ts_entry['Time Started'], '%d/%m/%y %H:%M'):
                            raise Exception('\nYou cannot complete the task before it was started! : Time Completed {} / Time Started {}'.format(field_entry, ts_entry['Time Started']))
                        else:
                            ts_entry.update({'Time Completed': field_entry.strftime('%d/%m/%y %H:%M')})
                            time_taken = datetime.datetime.strptime(ts_entry['Time Completed'], '%d/%m/%y %H:%M') - datetime.datetime.strptime(ts_entry['Time Started'], '%d/%m/%y %H:%M')

                            time_taken_seconds = time_taken.total_seconds()
                            m, s = divmod(time_taken_seconds, 60)
                            h, m = divmod(m, 60)
                            #d, h = divmod(h, 24)
                            time_str = '{} hours {} minutes'.format(h,m)

                            ts_entry.update({'Total Time' : time_taken_seconds})
                            ts_entry.update({'Total Time Str': time_str})
                            break
                mod_list.append(ts_entry)
                self.display_results(mod_list, 'The following Timesheet was sucessfully modified.')
                return ts_entry
            except Exception as error:
                print(error)
            except ValueError:
                print('Invalid entry, try again!')

# the following method displays a menu of search functions to choose from
    def search_timesheets(self):
        self.search_choices = {
            '1': self.find_by_date,
            '2': self.find_by_name,
            '3': self.find_by_duration,
            '4': self.find_by_lookup,
            '5': self.find_by_pattern,
            '6': self.timesheet_run,
            '7': self.quit
            }

        while True:
            self.display_menu(Constants.SEARCH_MENU, self.search_choices)
            choice = input("Enter an option: ")
            action = search_choices.get(choice)
            if action:
                action()
            else:
                input("\n{} is not a valid choice, press enter to continue: ".format(choice))

    # method to get the employee name - uses a regex to test that the user has
    # entered both a first name a space and a last name
    def get_employee_name(self):
        clear_screen()
        while True:
            try:
                employee_name = input('\nPlease enter your full name i.e. Stuart McIntosh : ')
                if employee_name == '' or employee_name.isnumeric():
                    raise Exception('Invalid entry, you must enter a name i.e. Stuart McIntosh:')
                else:
                    match = re.match(r'[-\w ]+\s[\w]+', employee_name)
                    if match:
                        return employee_name
            except Exception as error:
                print(error)
            except ValueError:
                print('Invalid entry, try again!')

    # method that displays a list of previously stored projects with dupliates
    # removed. It also allows the user to enter a new project
    def get_project(self):
        project_dict = {}
        project_dict = collections.OrderedDict(project_dict)
        temp_list = []
        ctr = 0

        clear_screen()

        # Fill out a temp dict with a list of current project - remove duplicates
        for x in self.timesheets:
            if x['Project Name'] not in temp_list:
                project_dict.update({str(ctr + 1) : x['Project Name']})
                temp_list.append(x['Project Name'])
                ctr += 1
        # Add an option to the list to get a new project name
        project_dict.update({'A' : 'Add New Project'})

        # print a menu to choose from
        print("Project List \n")
        for k, v in project_dict.items():
            print('{} {}'.format(k, v))

        # Get a valid input from the user - either a Project ID or add a new project
        while True:
            try:
                project_id = input('\nPlease enter a Project ID from list or A to add a new Project : ')
                if project_id == '':
                    raise Exception('Invalid entry, you must select a valid Project ID or A to add a new Project : ')
                elif project_id.isalpha():
                    if project_id.upper().strip() != 'A':
                        raise Exception('Invalid entry, you must select a valid Project ID or A to add a new Project :')
                    else:
                        project = input("Enter a new project name : ")
                        if project == '':
                            raise Exception('Invalid entry, the Project must have a name : ')
                        else:
                            return project
                elif int(project_id) > ctr or int(project_id) == 0:
                    raise Exception('You must select a Project ID in the range of 1 to {} : '.format(ctr))
                else:
                    project = project_dict.get(project_id)
                    return project
            except Exception as error:
                print(error)
            except ValueError:
                print('Invalid entry, try again!')

    # method to enter the task performed on the project
    # a task cannot be more than 30 characters long
    def get_task(self):
        while True:
            try:
                task = input('Enter task performed. Task entires cannot be more than 30 characters long : ')
                if task == '':
                    raise Exception('You must enter a task!')
                elif len(task) > 30:
                    raise Exception('A task cannot be more than 30 characters long!')
                else:
                    return task
            except Exception as error:
                print(error)
            except ValueError:
                print('Invalid entry, try again!')

    # uses a system call to get notes data
    def get_notes(self):
        print("Enter your task notes - press Ctrl+d when finished\n")
        data = sys.stdin.read().strip()
        if data:
            return data

    # method to get the date and time the employee started the task
    def get_time_started(self):
        while True:
            try:
                date_input = input('Please enter date and time you started working, please use - dd/mm/yy hh:mm : ')
                time_started = datetime.datetime.strptime(date_input, '%d/%m/%y %H:%M')
                if time_started >= datetime.datetime.now():
                    raise Exception('\nThe start date cannot be in the future!\n')
                else:
                    return time_started
            except Exception as error:
                print(error)
            except ValueError:
                print("\nInvalid entry. The date entered must use the format dd/mm/yy hh:mm\n")

    # method to get the date and time the user completed the task
    def get_time_completed(self, time_started):
        while True:
            try:
                date_input = input('Please enter the date and time you completed, please use - dd/mm/yy hh:mm : ')
                time_completed = datetime.datetime.strptime(date_input, '%d/%m/%y %H:%M')
                if time_completed <= time_started or time_completed >= datetime.datetime.now():
                    raise Exception('\nThe completed date cannot be before the start date or after the current date and time!\n')
                else:
                    return time_completed
            except Exception as error:
                print(error)
            except ValueError:
                print("\nInvalid entry. The date entered must use the format dd/mm/yy hh:mm\n")

    # method that returns the total time taken on the task in minutes
    def get_total_time(self):
        time_taken = self.time_completed - self.time_started
        time_taken_minutes = time_taken.total_seconds() // 60
        time_taken_seconds = time_taken.total_seconds()

        m, s = divmod(time_taken_seconds, 60)
        h, m = divmod(m, 60)
        #d, h = divmod(h, 24)
        time_str = '{} hours {} minutes'.format(h,m)

        return time_taken_seconds, time_str

    def find_by_date(self):
        date_dict = {}
        date_dict = collections.OrderedDict(date_dict)
        temp_list = []
        date_list = []
        ctr = 0

        clear_screen()

        # Fill out a temp dict with a list of current start dates - remove duplicates
        for x in self.timesheets:
            if x['Time Started'] not in date_list:
                date_dict.update({str(ctr + 1) : x['Time Started']})
                date_list.append(x['Time Started'])
                ctr += 1
        # print a menu to choose from
        print('Task Date List \n')
        for k, v in date_dict.items():
            print('{} {}'.format(k, v))

        # Get a valid input from the user
        while True:
            try:
                date_id = input('\nPlease choose a date_id from the list to search entries : ')
                if date_id == '':
                    raise Exception('Invalid entry, you must select a valid date_id : ')
                elif not date_id.isnumeric():
                    raise Exception('Invalid entry, you must select a valid date_id : ')
                else:
                    search_date = date_dict.get(date_id)
                    for x in self.timesheets:
                        if x['Time Started'] == search_date:
                            temp_list.append(x)
                    search_message = 'The following task(s) started on {} :\n'.format(search_date)
                    self.display_results(temp_list, search_message)
                    break
            except Exception as error:
                print(error)
            except ValueError:
                print("Invalid entry. Try again!")


    def find_by_name(self):
        clear_screen()
        name_dict = {}
        name_dict = collections.OrderedDict(name_dict)
        name_list = []
        temp_list = []
        emp_name = ''
        first_last_name = ''
        # Get a valid input from the user
        # Fill out a temp dict with a list of current start dates - remove duplicates
        for num, x in enumerate(self.timesheets):
            if x['Employee Name'] not in name_list:
                name_dict.update({str(num + 1): x['Employee Name']})
                name_list.append(x['Employee Name'])

        # print a menu to choose from
        print('Employee List \n')
        for k, v in name_dict.items():
            print('{} {}'.format(k, v))


        while True:
            try:
                name_string = input('\nPlease enter an employee name or select a number from the employee list : ')
                if name_string == '':
                    raise Exception('Invalid entry, you must enter a name to search for!')
                    # we need to run through all the timesheets and check of the string given
                    # is in tasks or notes - if found, store that result and
                    # then pass the result to be displayed
                elif name_string.isnumeric():
                    if int(name_string) > (num + 1) or int(name_string) == 0:
                        raise Exception('You must select a Employee ID in the range of 1 to {} : '.format(num + 1))
                    else:
                        emp_name = name_dict.get(name_string)
                else:
                    emp_name = name_string
                    first_last_name = name_string.split()
                for x in self.timesheets:
                    if emp_name.upper() == x['Employee Name'].upper():
                        temp_list.append(x)
                search_message = ('The following timesheets have been logged by {} !\n'.format(emp_name.upper()))
                self.display_results(temp_list, search_message)
                break
            except Exception as error:
                print(error)
            except ValueError:
                print("Invalid entry. Try again!")


    # the following method gives a user the ability to see a timesheet or timesheets
    # by entering the number of minutes a task took...
    # if the search find 0 exact minute matches it will offer the user to see the
    # the entries that took between a range of minutes i.e. 100 - 500 minutes
    def find_by_duration(self):
        temp_list = []
        while True:
            try:
                num_minutes = input('\n Please enter the exact number, or a range of minutes for a task performed - e.g 100 or 100 - 300 : ')
                if num_minutes == '' or num_minutes.isalpha():
                    raise Exception('Invalid entry, you must enter a number :')
                elif re.match(r'\d+\s?-\s?\d+', num_minutes):
                    # we have a match on the range on minutes
                    # split the string on '-' and strip away any spaces
                    minute_range = num_minutes.split('-')
                    for x in self.timesheets:
                        if float(x['Total Time']) // 60 >= int(minute_range[0]) and float(x['Total Time']) // 60 <= int(minute_range[1]):
                            temp_list.append(x)
                    search_message = 'The following timesheets met your search criteria!'
                    self.display_results(temp_list, search_message)
                    break
                else:
                    # check the timesheet list for entries with exact match
                    # need to change add round(total_time.days / 1440 + total_time.seconds / 60))
                    for x in self.timesheets:
                        if int(num_minutes) == float(x['Total Time']) // 60:
                            temp_list.append(x)
                    search_message = 'The following timesheets met your search criteria!\n'
                    self.display_results(temp_list, search_message)
                    break
            except Exception as error:
                print(error)
            except ValueError:
                print("Invalid entry. Try again!")

    # the following method takes a string from the end user and serches in both task
    # and notes entries for an abosulte match - will print out multiple timesheets if
    # the string is found more than once
    def find_by_lookup(self):
        clear_screen()
        temp_list = []
        # Get a valid input from the user
        while True:
            try:
                search_string = input('Please enter a string you would like to search for i.e. "'"Completed database cleanup"'" : ')
                if search_string == '':
                    raise Exception('Invalid entry, you must enter a string to search for!')
                else:
                    # we need to run through all the timesheets and check of the string given
                    # is in tasks or notes - if found, store that result and
                    # then pass the result to be displayed
                    for x in self.timesheets:
                        if search_string.upper() in x['Task Completed'].upper() or search_string.upper() in x['Notes'].upper():
                            temp_list.append(x)
                    search_message = 'The following timesheets met your search criteria!\n'
                    self.display_results(temp_list, search_message)
                    break
            except Exception as error:
                print(error)
            except ValueError:
                print("Invalid entry. Try again!")

    # this method allows the user to enter a regex expression to search for patterns
    # eithe in task or notes
    def find_by_pattern(self):
        clear_screen()
        temp_list = []
        # Get a valid input from the user
        while True:
            try:
                search_pattern = input('Please enter a regular expression "'"\w\d+"'" : ')
                if search_pattern == '':
                    raise Exception('\nInvalid entry, you must enter a regular expression!\n')
                else:
                    for x in self.timesheets:
                        if re.search(search_pattern, x['Task Completed']) or re.search(search_pattern, x['Notes']):
                            temp_list.append(x)
                    search_message = 'The following timesheets met your search criteria!\n'
                    self.display_results(temp_list, search_message)
                    break
            except Exception as error:
                print(error)
            except ValueError:
                print("Invalid entry. Try again!")

    # method prints out timesheets based on criteria from user
    def display_results(self, search_criteria, search_message):
        clear_screen()
        print(search_message + '\n')
        for x in search_criteria:
            print(Constants.GREEN + '*******************************************\n')
            print(Constants.GREEN + '   Employee Name: {} | Project Name: {} | Task Completed: {} \n'.format(x['Employee Name'],x['Project Name'], x['Task Completed']))
            print(Constants.GREEN + '   Time Started: {} | Time Taken: {}'.format(x['Time Started'], x['Total Time Str']))
            print(Constants.GREEN + '   Notes: {}\n'.format(x['Notes']))
        input(Constants.ENDC + '\n\nPress Enter to continue : ')

TimeSheet().timesheet_run()
