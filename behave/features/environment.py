from os.path import exists
from os import getcwd, makedirs, rename
from socket import gethostname
from uuid import getnode
import re
from getpass import getuser
from pathlib import Path
from datetime import datetime
from os import name as os_name


"""
The environment.py module may define code to run before and after certain events during 
your testing.

"""

BEHAVE_DEBUG_ON_ERROR = False


def forbidden_character_filter(file_name):
    """
    Cleans all bad reserved from the file or directory you put through it.
    
    DO NOT PUT A DRIRECTORY STRING THROUGH THIS FUNCTION. It will turn your
    directory into one long file and probably kill you test.
    
    See Microsoft's "Naming Files, Paths, and Namespaces":
    https://docs.microsoft.com/en-us/windows/win32/fileio/naming-a-file
    
    The following are reserved characters for Windows:

    < (less than)
    > (greater than)
    : (colon)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)
    
    :param file_name: (str) The file name you want to clean.
    :return: The file name without any reserved characters.
    """
    forbidden_list = ['\<','\>','\:','\"','\/','\\','\|','\?','\*']
    
    #Puts the file name into a new container.
    clean_file_name = file_name
    
    #For every item in the forbidden_list
    for forbidden_char in forbidden_list:
        
        #Replaces the character with a "-".
        clean_file_name.replace(forbidden_char, "-")
    
    return clean_file_name


def setup_debug_on_error(userdata):
    """
    Behave Documentation recommendation. 
    """
    global BEHAVE_DEBUG_ON_ERROR 
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")


def get_time_right_now():
    """
    Returns the date and time. Keeping this as its own function allows the users to
    customize the date/time format on demand. If multiple formats are needed, copy
    and pasted this function, change it to fit each individual need.
    
    See Python 3 docs for more info.
    https://docs.python.org/3/library/datetime.html
    
    format  MM/DD/YY hh:mm:ss 
    """
    now = datetime.now().strftime('%m/%d/%y %I:%M:%S %p')
    return str(now)


def before_all(context):
    """
    This runs before the whole shooting match.
    """
    if os_name == 'posix':
        context.folder_divid = '/'
    else:
        context.folder_divid = '\\'
    #Set the start time of the test run.
    context.run_time_start = str(datetime.now().strftime('%m-%d-%y_%I-%M-%S_%p'))
    context.run_time_start_int = datetime.now()
    
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini".
    context.config.setup_logging()
    
    #Current working directory upon startup
    context.starting_working_directory = getcwd()
    
    #Pulls the log_path value from the behave.ini file.
    context.log_path = context.config.userdata['log_path']
    
    """
    A lot of the work below will be working on fixing any potential issues with log paths that
    may occur. Specific characters or spaces in the wrong area will cause the test to fail 
    before it even starts. 
    """
    
    #If the log path originates in the current working directory.
    if context.log_path.startswith('.'):
        
        context.log_path = context.log_path.replace(".", "")
        context.log_path = str(context.starting_working_directory + context.log_path)
        if not context.log_path.endswith(context.folder_divid):
            context.log_path = context.log_path + context.folder_divid
    
    #Set the hostname of the execution host to the variable.
    context.exe_hostname = str(gethostname())
    
    #Get MAC address source: https://www.geeksforgeeks.org/extracting-mac-address-using-python/?ref=rp
    context.exe_host_ip = str(':'.join(re.findall('..', '%012x' % getnode())))
    
    #Sets the login user of the execution host to the variable.
    context.exe_login_user = str(getuser())
    
    #Creates the log path directory if it does not exist.
    if not exists(context.log_path):
        makedirs(context.log_path)
    
    context.log_path_raw = Path(context.log_path + 'test_run_' + context.run_time_start)
    context.log_path = str(context.log_path_raw)
    
    #Creates the log path directory if it does not exist.
    if not exists(context.log_path):
        makedirs(context.log_path)
    
    
    log_string = 'Test Run Information\n\n'
    log_string = log_string + 'Working Directory:\t{}\n'.format(context.starting_working_directory)
    log_string = log_string + 'Starting Date\\Time:\t{}\n'.format(context.run_time_start_int)
    log_string = log_string + 'Behave User Data:\t{}\n'.format(context.config.userdata)
    
    context.test_run_log = context.log_path + context.folder_divid + 'test_run_info.txt'
    context.scenario_file = open(context.test_run_log,"w+")
    context.scenario_file.write(log_string)
    context.scenario_file.close()


def before_tag(context, tag):
    """
    This runs before a section tagged with the given name.They are invoked for each tag 
    encountered in the order they're found in the feature file. See "Controlling Things 
    With Tags" in the "behave Documentation". The tag passed in is an instance of Tag 
    and because it's a subclass of string you can do simple tests.
    """
    pass
    

def before_feature(context, feature):
    """
    This runs after each feature file is ex-ercised. The feature passed in is an instance of Feature 
    (see behave Doc).
    """
    context.feature_name = feature.name
    context.feature_tags = feature.tags
    context.feature_filename = feature.filename
    
    
    #Set the start time of the feature execution.
    context.feature_start_time = get_time_right_now()
    
    #Clears all forbidden characters from the scenario name
    context.feature_name = forbidden_character_filter(context.feature_name)
    
    context.log_path_feature_raw = Path(context.log_path + context.folder_divid + context.feature_name)
    context.log_path_feature = str(context.log_path_feature_raw)
    
    #Creates the log path directory if it does not exist.
    if not exists(context.log_path_feature):
        makedirs(context.log_path_feature)
 
 
def before_scenario(context, scenario):
    """
    This runs before each scenario is run.
    """
    context.scenario_name = scenario.name
    
    #Repo for passwords. Used to replace passwords that may be caught during runtime.
    context.plaintext_passwords = []
    
    #Set the start time of the scenario execution.
    context.scenario_start_time = get_time_right_now()
    
    #Sets the screenshot count. Prodominately used for Selenium or PyWinAuto (GUI tools).
    context.screenshot_count = 0
    
    #Replaces any whitespace in the end of the string. Whitespace will cause problems later on if left in.
    context.scenario_name = re.sub('\s+$',  '', context.scenario_name)
    
    #Clears all forbidden characters from the scenario name
    context.scenario_name = forbidden_character_filter(context.scenario_name)
    
    #Creates the log path at the scenario level. 
    context.log_path_scenario_raw = Path(context.log_path_feature + context.folder_divid + context.scenario_name)
    context.log_path_scenario = str(context.log_path_scenario_raw)
    
    #Creates the log path directory if it does not exist.
    if not exists(context.log_path_scenario):
        makedirs(context.log_path_scenario)
    
    #Pulls the log_path value from the behave.ini file.
    context.scenario_log_name = context.config.userdata['scenario_log_name']
    
    context.scenario_log = context.log_path_scenario + context.folder_divid + context.scenario_log_name
    
    #Scenario log string.
    log_string = 'Feature Filename:\t{}\n'.format(context.feature_filename)
    log_string = log_string + 'Feature Name:\t\t{}\n'.format(context.feature_name)
    log_string = log_string + 'Scenario Start Time:\t{}\n'.format(context.scenario_start_time)
    log_string = log_string + 'Scenario Name:\t\t{}\n'.format(context.scenario_name)
    log_string = log_string + 'Scenario Tags:\t\t{}\n\n\n'.format(scenario.tags)
    
    #Creates the scenario log and saves the scenario log string to the scenario.log file.
    context.scenario_file = open(context.scenario_log,"w+")
    context.scenario_file.write(log_string)
    context.scenario_file.close()
    
    
def before_step(context, step):
    """
    This runs before every step.
    """
    context.step_name = step.name
    
    #Set the start time of the step execution.
    context.step_start_time = get_time_right_now()
    
    log_string = '================ Step Start ================\n'
    log_string = log_string  + 'Step Title:\t\t{} {}\n'.format(step.keyword, step.name)
    log_string = log_string  + 'Step Starting Time:\t{}\n'.format(context.step_start_time)
    log_string = log_string  + 'Step Feature Line:\t{}\n\n\n'.format(step.line)
    
    context.scenario_file = open(context.scenario_log,"a")
    context.scenario_file.write(log_string)
    context.scenario_file.close()


def after_step(context, step):
    """
    This runs after every step.
    """
    #Set the ending time of the step execution.
    context.step_end_time = get_time_right_now()
    
    log_string = '---------------- Step Ending Info ----------------\n'
    log_string = log_string  + 'Step Title:\t\t{} {}\n'.format(step.keyword, step.name)
    log_string = log_string  + 'Step Ending Time:\t{}\n'.format(context.step_end_time)
    log_string = log_string  + 'Step Duration:\t\t{}\n'.format(step.duration)
    if step.status == 'failed':
        log_string = log_string  + 'Step Status:\t\tFailed\n'
        log_string = log_string  + 'Step Error Message:\t{}\n'.format(step.error_message)
    else:
        log_string = log_string  + 'Step Status:\t\tSuccessful\n'
    log_string = log_string  + '================ Step End ================\n\n'
    
    context.scenario_file = open(context.scenario_log,"a")
    context.scenario_file.write(log_string)
    context.scenario_file.close()
    
    
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location. #@UnresolvedImport
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb 
        ipdb.post_mortem(step.exc_traceback)


def after_scenario(context, scenario):
    """
    These run after each scenario is run.
    """
    
    #Set the ending time of the scenario execution.
    context.scenario_end_time = get_time_right_now()
    
    #If Selenium was used in the scenario
    if 'driver' in context:
        #Closes all open windows.
        context.driver.quit()
    
    #Masks all passwords used during the scenario in the scenario log file.
    if context.plaintext_passwords:
        for password in context.plaintext_passwords:
            #Opens the scenario log in read mode.
            f = open(context.scenario_log, 'r')
            #Stores all information in the "text" variable.
            text = f.read()
            #Closes the file.
            f.close()
            
            #What the password will be replaced with.
            rp = r'***Password Removed***'
            #Replaces the password.
            masked_passwd_text = text.replace(password, rp)
            
            #Saves the masked_passwd_text to the chromedriver log file.
            f = open(context.scenario_log, 'w')
            f.write(masked_passwd_text)
            f.close()
    
    
    #If Google Chrome was used, the chromedriver.log file will be checked and 
    #cleared for passwords used during the scenario.
    if 'chromedriver_log' in context:
        
        #For each password in the plaintext_passwords list.
        for password in context.plaintext_passwords:
            #Opens the chromedriver log in read mode.
            f = open(context.chromedriver_log, 'r')
            #Stores all information in the "text" variable.
            text = f.read()
            #Closes the file.
            f.close()
            
            #The password pattern to look for.
            pattern = r'"text": "{}",'.format(password)
            #What the password will be replaced with.
            rp = '"text": "***Password Removed***",'
            #Replaces the password.
            masked_passwd_text = text.replace(pattern, rp)
            
            #Separates every character in the password into a list.
            wordlist = list(password)
            
            #Establishes the second pattern.
            pattern2 = ''
            
            #for every character in wordlist.
            for i in wordlist:
                #If the character is last in the list.
                if i == wordlist[-1]:
                    #Places the last character in this string.
                    pattern2 = '{}"{}"'.format(pattern2, i)
                else:
                    #Places every other character in this string.
                    pattern2 = '{}"{}",,'.format(pattern2, i)
            
            #The second password pattern to look for.
            pattern2 = '"value": [ {} ]'.format(pattern2)
            #What the password will be replaced with.
            rp2 = '"value": [ "***Password Removed***" ]'
            #Masks the second set of password info.
            masked_passwd_text = masked_passwd_text.replace(pattern2, rp2)
            
            #Saves the masked_passwd_text to the chromedriver log file.
            f = open(context.chromedriver_log, 'w')
            f.write(masked_passwd_text)
            f.close()
    
    #If the scenario fails, the scenario folder will change to '_FAILED' at the end.
    if scenario.status == 'failed':
        scenario_fail_path = str(context.log_path_scenario_raw) + '_FAILED'
        rename(context.log_path_scenario, scenario_fail_path)
        context.log_path_scenario = scenario_fail_path


def after_feature(context, feature):
    """
    This runs after each feature file is ex-ercised. The feature passed in is an instance of Feature 
    (see behave Doc).
    """
    #Set the ending time of the feature execution.
    context.feature_end_time = get_time_right_now()
    
    #If the feature fails, the feature folder will change to '_FAILED' at the end.
    if feature.status == 'failed':
        if '_FAILED' not in context.log_path_feature:
            feature_fail_path = str(context.log_path_feature_raw) + '_FAILED'
            rename(context.log_path_feature, feature_fail_path)


def after_tag(context, tag):
    """
    This runs after a section tagged with the given name.They are invoked for each tag 
    encountered in the order they're found in the feature file. See "Controlling Things 
    With Tags" in the "behave Documentation". The tag passed in is an instance of Tag 
    and because it's a subclass of string you can do simple tests.
    """
    pass
    

def after_all(context):
    """
    This runs after the whole shooting match.
    """
    #Set the ending time of the test run.
    context.run_time_end = get_time_right_now()
    run_time_duration = datetime.now() - context.run_time_start_int
    
    log_string = 'Test Run Duration:\t{}\n'.format(run_time_duration)
    log_string = log_string + 'Ending Date\\Time:\t{}\n'.format(datetime.now())
    
    context.scenario_file = open(context.test_run_log,"a")
    context.scenario_file.write(log_string)

