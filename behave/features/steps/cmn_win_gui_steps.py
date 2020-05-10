import pyautogui
from behave import given
from cmn_win_gui_functions import take_a_gui_screenshot, open_windows_run_menu, highlight_all_text
from cmn_cmdline_steps import execute_local_powershell_cmd
from common_functions import get_usr_prop
import time

"""
Do check out PyAutoGui's documentation page here:
https://pyautogui.readthedocs.io/en/latest/index.html

Capturing images for PyAutoGUI to see:
Window - Pressing Windows Key + PrtScn. Save the SC to your 
         C:\\Users\\<your_profle>\\Pictures\\Screenshots folder.
Linux - PrtScn button Save a screenshot of the entire screen to the 'Pictures' directory.
Open the image by right-clicking on it and hitting "Edit".
Resize the image to just enough of the image to be unique for the search item you 
are looking for.
Save the image to the project's image repository as '<image-title>.png'.
The image has to be a ".png" file for it to work.

"""


@given('the Windows Start button is clicked on')
def given_the_windows_start_button_is_clicked_on(context):
    """
    This is an 'iffy' one. Since everyone has their screen settings customized, this will 
    definitely fail. 
    
    What you will have to do is take a screenshot by:
    Window - Pressing Windows Key + PrtScn. Save the SC to your 
             C:\\Users\\<your_profle>\\Pictures\\Screenshots folder.
    Linux - PrtScn Save a screenshot of the entire screen to the 'Pictures' directory.
    (Just find something on your desktop for Linux to pick up)
    Open the image by right-clicking on it and hitting "Edit".
    Resize the image to just the Windows start button, save it to the project's 
    resources\image_repo as 'start.png'. Rerun the test and it should pass.
    """
    start_button = pyautogui.locateCenterOnScreen('.\\resources\\image_repo\\start.png')
    
    #Confirms the image was found. If not found, the scenario is ended.
    assert start_button, 'this didn\'t work! Read the directions for this step before running again.'
    
    #The "locateCenterOnScreen" function moves the cursor to the center of the image, 
    #then clicks.
    pyautogui.click(start_button)
    
    take_a_gui_screenshot(context, 'Windows Start button was clicked on')



@given('the "{user}" user account establishes an RDP connection to "{host}" host cmd')
def given_the_user_account_establishes_an_rdp_connection_to_host_cmd(context, user, host):
    """
    Uses PowerShell to create an Remote Desktop Protocol connection to a specific host.
    Not image based GUI automation but it works faster and more reliably. Just another 
    option for you to use if it falls within the scope of what you are trying to 
    accomplish. 
    
    cmdkey documentation:
    https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey
    
    mstsc documentation:
    https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc
    
    :param user: (str) User account information you want to pull form your 
        user_properties.ini file
    :param host: (str) 
    """
    #The get_usr_prop function returns user property information from your 
    #user_properties.ini file.
    username = get_usr_prop(context, user)
    user_pass = get_usr_prop(context, user + ".password")
    host = str(host)
    
    cmdkey_string = 'cmdkey /add:"{}" /user:"{}" /pass:"{}"; '.format(host, username, user_pass)
    rdp_connection_string = cmdkey_string + 'mstsc /v:{}; '.format(host)
    ps_command = rdp_connection_string + 'cmdkey /delete:{}'.format(host)
    
    output = execute_local_powershell_cmd(context, ps_command)
    
    #Asserts that no error messages are produced.
    assert not output[1], 'An error occurred when executing an RDP connection through the command-line to host "{}"'.format(host)



@given('the "{user}" user account establishes an RDP connection to "{host}" host')
def given_the_user_account_establishes_an_rdp_connection_to_host_gui(context, user, host):
    """
    Uses PowerShell to create an Remote Desktop Protocol connection to a specific host.
    Not image based GUI automation but it works faster and more reliably. Just another 
    option for you to use if it falls within the scope of what you are trying to 
    accomplish. 
    
    cmdkey documentation:
    https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cmdkey
    
    mstsc documentation:
    https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/mstsc
    
    :param user: (str) User account information you want to pull form your 
        user_properties.ini file
    :param host: (str) 
    """
    #The get_usr_prop function returns user property information from your 
    #user_properties.ini file.
    username = get_usr_prop(context, user)
    user_pass = get_usr_prop(context, user + ".password")
    
    #Assures that the hostname is in string format for PyAutoGUI to write.
    host = str(host)
    
    #Self explanatory.
    open_windows_run_menu()
    
    #Snooze button
    time.sleep(0.5)
    
    #Microsoft Terminal Services Client Suggest (aka RDP)
    pyautogui.write('mstsc')
    #Runs the program.
    pyautogui.press('enter')
    
    time.sleep(0.5)
    
    #In some cases, the previous hostname will still be in the "Computer:" entry field.
    #This step makes sure that the field will whip everything currently existing after
    #you start typing the hostname.
    highlight_all_text()
    
    #Enters the hostname into the "Computer:" entry field. 
    pyautogui.write(host)
    
    assert "I will not do any more work on this function. Your RDP configs start to differ from here. You will know the best way to finish."
    