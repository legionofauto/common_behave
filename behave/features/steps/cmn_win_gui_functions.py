import pyautogui

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

def take_a_gui_screenshot(context, sc_title):
    """
    Takes the PyAutoGUI screenshot function and expands upon it. Adds a padding to the
    beginning of the screenshot for the purpose of reading the sequence of events. 
    Also, forces all screenshots to point to the scenario log folder. 
    
    This will also prevent the potential of saving over an image if the same function 
    is called twice in a single scenario.
    """
    #takes the count, established in the "before_scenario" sections in the environment.py
    #file.
    context.screenshot_count += 1
    
    #Adds the paadding to the beginning of your screenshot. If you are taking over 1k 
    #screenshots in one scenario, revisit the scope of your test or update this...
    if len(str(context.screenshot_count)) == 1:
        sc_padding = '00'
    elif len(str(context.screenshot_count)) == 2:
        sc_padding = '0'
    else:
        sc_padding = ''
    
    #Adds the padding.
    screenshot_padding = sc_padding + str(context.screenshot_count)
    
    #Uses PyAutoGui's screenshot function to take the picture.
    myScreenshot = pyautogui.screenshot()
    
    #Saves the picture to the scenario log folder.
    myScreenshot.save(context.log_path_scenario + screenshot_padding + '_' + sc_title + r'.png')


def highlight_all_text():
    """
    Used to select all text, or other objects while in a graphical user environment.
    """
    pyautogui.hotkey('ctrl', 'a')


def open_windows_run_menu():
    """
    Opens the Windows Run menu.
    """
    pyautogui.hotkey('win', 'r')


def switch_between_open_programs():
    """
    Switch between open programs.
    """
    pyautogui.hotkey('alt', 'tab')


def switch_between_open_programs_in_order_they_were_opened():
    """
    Switch between programs in order they were opened.
    """
    pyautogui.hotkey('alt', 'esc')


def open_task_manager():
    """
    Opens Windows Task Manager.
    """
    pyautogui.hotkey('ctrl', 'shift', 'esc')


def open_search_file_or_folder():
    """
    Opens search for files and folders.
    """
    pyautogui.hotkey('ctrl', 'f')


def show_the_desktop():
    """
    Display the desktop.
    """
    pyautogui.hotkey('win', 'd')


def close_active_window():
    """
    Quit active application or close current window.
    """
    pyautogui.hotkey('alt', 'f4')


def open_task_viewer():
    """
    Quit active application or close current window.
    """
    pyautogui.hotkey('alt', 'f4')

