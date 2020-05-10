from base64 import b64encode
from configparser import RawConfigParser, ConfigParser
from datetime import timezone, date, datetime
from os import getenv
from pathlib import Path
from csv import DictReader


"""
Please check out this site for tips on Python secure coding standards:

-Python officially recommends to follow the high-level docstring conventions.:
    https://www.python.org/dev/peps/pep-0257/

-string formatting operations:
    https://www.python.org/dev/peps/pep-3101/

-python coding style guidelines which strongly recommend naming conventions, 
 comments, formatting and lot more:
    https://www.python.org/dev/peps/pep-0008/

Can take concepts from OWASP as well. 
http://www.pythonsecurity.org/

Bandit is a tool designed to find common security issues in Python code. To do this, 
Bandit processes each file, builds an AST from it, and runs appropriate plugins 
against the AST nodes. Once Bandit has finished scanning all the files, it generates 
a report.
https://bandit.readthedocs.io/en/latest/

Use "#@UnresolvedImport" on imports that will not resolve when using Eclipse IDE.
"""

################ Helper Functions ################


def get_time_right_now():
    """
    Returns the date and time.
    """
    now = datetime.now().strftime('%m/%d/%y %H:%M:%S %p')
    return now


def get_military_time():
    """
    The Military Date Time Group (DTG) format is used in everything from operations 
    orders to airlifts, and it is essential for every service member to know how to 
    put together a Date Time Group (DTG) format correctly.
    
    the Date Time Group is traditionally formatted as DDHHMM(Z)MONYY
    -DD: Day of the month (e.g. January 6th=06)
    -HHMM: Time in 24 hr format +military time zone (e.g. 6:30pm in =1830).
    -Z: Military identifier- see below for a complete list
    -MON: 3 digit month code, (e.g. January= JAN)
    -YY: 2 Digit year, (e.g. 2012= 12)
    """
    mil_time = date.astimezone(timezone.utc).strftime('%d %H%M') + 'z ' + date.astimezone(timezone.utc).strftime('%b %y')
    return mil_time


def set_key_prop(key, value):
    """
    """
    value=b64encode(value).decode()
    key_file='C:\\path\\to\\secure\\folder\\crypto_key.key'
    config = RawConfigParser()
    config.read(key_file)
    config['KEY'][key] = value
    with open(key_file, 'w') as configfile:    # save the config update.
        config.write(configfile)


def get_usr_prop(context, key):
    """
    Gets the value of the value for the key used in your user_properties.ini file.
    """
    #path the the key file.
    user_properties = 'user_properties.ini'
    config = ConfigParser()
    config.read(user_properties)
    value=config['USERS'][key]
    if 'password' in value:
        context.plaintext_passwords.append(value)
    return value


def get_java_home():
    """"""
    java_home = None
    if getenv('JAVA_HOME'):
        java_home = getenv('JAVA_HOME')
    else:
        #You might have to manually define this part.
        try:
            #This looks for the x64 path to your default Java files.
            java_dir_path = list(Path('C:/java').glob('*x64'))
            if java_dir_path:
                java_home = str(java_dir_path[0])
        except:
            #This looks for the x64 path to your default Java files.
            java_dir_path = list(Path('C:/java').glob('*x32'))
            if java_dir_path:
                java_home = str(java_dir_path[0])
    
    return java_home
            
        
def mask_passwords(context, string_input):
    """
    
    """
    clean_string = string_input
    for passwd in context.plaintext_passwords:
        clean_string = clean_string.replace(passwd, r'*** password replaced ***')
    return clean_string
    

def parse_csv(csv_file, column_name):
    """
    returns a dictionary of values in the column you are looking for.
    
    :params csv_file: (str) Path to the csv file you wish to parse. 
    :params column_name: (str) Name of the column you are looking at.
    :return: A dictionary of items from the column specified in the csv file.
    """
    column_dict = {}
    with open(csv_file) as f:
        column_item = DictReader(f)
        for _, item in enumerate(column_item):
            column_dict[item[column_name]] = item
    
    return column_dict


def scenario_logger(context, logging_string):
    """
    Makes logging simple and fast.
    """
    logging_string = str(logging_string)
    
    #Masks all passwords used during the scenario in the scenario log file.
    if context.plaintext_passwords:
        for password in context.plaintext_passwords:
            
            #What the password will be replaced with.
            rp = r'***Password Removed***'
            #Replaces the password.
            logging_string = logging_string.replace(password, rp)
    
    context.scenario_file = open(context.scenario_log,"a")
    context.scenario_file.write(logging_string)
    context.scenario_file.close()
    
    
    
    
    