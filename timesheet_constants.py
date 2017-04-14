
class Constants:

    TIMESHEET_MENU = """
    Timesheet Menu

    1. Add New TimeSheet
    2. Display TimeSheets
    3. Search TimeSheets
    4. Modify / Delete a TimeSheet
    5. Quit
    """

    SEARCH_MENU = '''
    Search Timesheet Menu

    1. Find Timesheets by Date
    2. Find Timesheets by Name
    3. Find Timesheets by Duration
    4. Find Timesheets by 'Lookup'
    5. Find Timesheets by 'Pattern'
    6. Return to main menu
    '''

    FIRST_USE = False

    # Ascii constants to add color to text
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLACK='\033[30m'
    RED='\033[31m'
    GREEN='\033[32m'
    ORANGE='\033[33m'
    BLUE='\033[34m'
    PURPLE='\033[35m'
    CYAN='\033[36m'
    LIGHTGREY='\033[37m'
    DARKGREY='\033[90m'
    LIGHTRED='\033[91m'
    LIGHTGREEN='\033[92m'
    YELLOW='\033[93m'
    LIGHTBLUE='\033[94m'
    PINK='\033[95m'
    LIGHTCYAN='\033[96m'

    BANNER = GREEN + """


              ### ### # # ###      ## # # ### ### ###     #    #   ##
               #   #  ### #       #   # # #   #    #      #   # # #
               #   #  ### ##       #  ### ##  ##   #      #   # # # #
               #   #  # # #         # # # #   #    #      #   # # # #
               #  ### # # ###     ##  # # ### ###  #      ###  #   ##

                                  SM IV.XIV.MMXVII
    """ + ENDC
