from selenium.webdriver import Chrome, ChromeOptions, FirefoxProfile, Firefox, Ie
from selenium.webdriver.chrome.options import Options as chromeOptions
from selenium.webdriver.ie.options import Options as ieOptions
from selenium.webdriver.firefox.options import Options as firefoxOptions
from behave import given, then

"""
This is a common Selenium Python file. Use this as a basis for execution. These functions are based
off of Selenium version 3.141.0. 

Selenium-python docs are located here:
https://selenium-python.readthedocs.io/

More Selenium docs here:
https://www.selenium.dev/documentation/en/
"""


@given('an Internet Explorer window is open')
def given_a_internet_explorer_window_is_open(context):
    """
    Opens a Internet Explorer window and establishes the initial Selenium browser configuration. 
    
    'IEDriverServer.exe' executable needs to be in PATH.
    
    By default, Seleniums Internet Explorer options are shown below:
     __init__(executable_path='IEDriverServer.exe', capabilities=None, port=0, timeout=30, host=None, 
     log_level=None, service_log_path=None, options=None, ie_options=None, desired_capabilities=None, 
     log_file=None, keep_alive=False)
    """
    ie_driver_path = context.config.userdata['ie_driver_path']
    
    #For IE, we have to modify Registry values instead of adding options like with Chrome or Firefox.
    
    driver_options = ieOptions() 
    '''
    https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
    
    This will make Selenium WebDriver to wait for the entire page is loaded. When set to normal, 
    Selenium WebDriver waits until the load event fire is returned.
    '''
    driver_options.page_load_strategy = 'normal'
    
    context.driver = Ie(executable_path=ie_driver_path, port=0, options=driver_options, 
                        service_log_path=None)
    
    context.driver.implicitly_wait(15)
    
    context.driver.maximize_window()


@given('a Google Chrome window is open')
def given_a_google_chrome_window_is_open(context):
    """
    Opens a Google Chrome window and establishes the initial Selenium browser configuration. Be careful
    with the version of Chromedriver you get. The version of Chromedriver should be the same version 
    number as the version of Chrome you are running. Chrome is very picky about versions. 
    
    'chromedriver.exe' executable needs to be in PATH.
    
    By default, Seleniums options are shown below:
     __init__(executable_path='chromedriver', port=0, options=None, service_args=None, 
     desired_capabilities=None, service_log_path=None, chrome_options=None, keep_alive=True)
    """
    chrome_driver_path = context.config.userdata['chrome_driver_path']
    print('nothing')
    
    chrome_options = ChromeOptions()
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    driver_options = chromeOptions() 
    '''
    https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
    
    This will make Selenium WebDriver to wait for the entire page is loaded. When set to normal, 
    Selenium WebDriver waits until the load event fire is returned.
    '''
    driver_options.page_load_strategy = 'normal'
    
    context.chromedriver_log = context.log_path_scenario + 'chrome.log'
    
    context.driver = Chrome(executable_path=chrome_driver_path, options=driver_options, 
                            service_log_path=context.chromedriver_log, 
                            chrome_options=chrome_options)
    
    context.driver.implicitly_wait(15)
    
    context.driver.maximize_window()


@given('a Mozilla Firefox window is open')
def given_a_mozilla_firefox_window_is_open(context):
    """
    Opens a Mozilla Firefox window and establishes the initial Selenium browser configuration. 
    
    'geckodriver.exe' executable needs to be in PATH.
    
    By default, Seleniums options are shown below:
      __init__(firefox_profile=None, firefox_binary=None, timeout=30, capabilities=None, 
      proxy=None, executable_path='geckodriver', options=None, service_log_path='geckodriver.log', 
      firefox_options=None, service_args=None, desired_capabilities=None, log_path=None, 
      keep_alive=True)
    """
    firefox_driver_path = context.config.userdata['firefox_driver_path']
    
    firefox_options = FirefoxProfile()
    firefox_options.set_preference("dom.webnotifications.enabled", False)
    firefox_options.set_preference("dom.disable_open_during_load", False)
    firefox_options.accept_untrusted_certs = True
    
    driver_options = firefoxOptions() 
    '''
    https://www.selenium.dev/documentation/en/webdriver/page_loading_strategy/
    
    This will make Selenium WebDriver to wait for the entire page is loaded. When set to normal, 
    Selenium WebDriver waits until the load event fire is returned.
    '''
    driver_options.page_load_strategy = 'normal'
    
    context.driver = Firefox(executable_path=firefox_driver_path, port=0, options=driver_options, 
                            service_log_path=None, firefox_options=firefox_options)
    
    context.driver.implicitly_wait(15)
    
    context.driver.maximize_window()


@then('the current window URL is "{url}"')
def then_the_current_window_url_is_text(context, url):
    """
    Gets the Uniform Resource Locator (URL) of the current page. If the URL outlined in the "url" 
    value does not match the current url, the scenario is failed.
    
    :param url: (str) Uniform Resource Locator.
    """
    assert url == context.driver.current_url, "The url '{}' does not match the current window's url {}".format(url, context.driver.current_url)


@given('the user navigates to "{url}"')
def given_the_user_navigates_to_url(context, url):
    """
    Loads a web page in the current browser session.
    
    :param url: (str) Uniform Resource Locator.
    """
    context.driver.get(url)
    take_full_page_screenshot(context, 'something stupid')


@then('the page title is "{page_title}"')
def then_the_page_title_is_text(context, page_title):
    """
    Compares the current page title with the title outlined in the step. If the information does
    not match, the scenario is failed.
    
    :param page_title: (str) The title of the page that the user want to see.
    """
    assert page_title == context.driver.title, "The url '{}' does not match the current window's url {}".format(page_title, context.driver.title)


@then('the web browser is closed')
def then_the_web_browser_is_closed(context):
    """
    Shouldn't really be used much at all since "context.driver.quit()" is place in the after_scenario function in the
    environment.py file. 
    """
    context.driver.quit()


def get_current_window_size(context):
    """
    Returns, through context, the height and width of the browser.
    """
    size = context.driver.get_window_size()
    context.width1 = size.get("width")
    context.height1 = size.get("height")


def set_current_window_size(context, width, height):
    """
    Allows the user to resize the browser.
    
    :param width: (int) The width of the window you want resize it to.
    :param height: (int) The height of the window you want resize it to.
    """
    context.driver.set_window_size(width, height)


def minimize_the_current_window(context):
    """
    Minimizes the current active window.
    """
    context.driver.minimize_window()


def take_full_page_screenshot(context, sc_title):
    """
    Takes a screenshot of the entire web page. Selenium only saves screenshots as ".png" files. Can copy and
    modify this for other GUI automation that require screenshots.
    
    :param sc_title: (str) What you want to name the screenshot.
    """
    context.screenshot_count += 1
    
    sc_padding = ''
    if len(str(context.screenshot_count)) == 1:
        sc_padding = '00'
    elif len(str(context.screenshot_count)) == 2:
        sc_padding = '0'
    else:
        sc_padding = ''
    
    screenshot_padding = sc_padding + str(context.screenshot_count)
    
    element = context.driver.find_element_by_tag_name('body')
    
    #Creates a file with the name you specify in the "sc_title" section.
    context.scenario_file = open(context.log_path_scenario + screenshot_padding + '_' + sc_title + ".png", "wb")
    context.scenario_file.write(element.screenshot_as_png)
    context.scenario_file.close()
    

def scroll_to_element(context, element):
    """
    A JavaScript W3C Document Object Model (DOM) is a platform and language-neutral interface 
    that allows programs and scripts to dynamically access and update the content, structure, 
    and style of a document.
    
    The scrollIntoView() method scrolls the specified element into the visible area of the 
    browser window. Predominantly used for screenshots. or clicking on web elements that were 
    originally off screen.
    
    With the HTML DOM, JavaScript can access and change all the elements of an HTML document.
    """
    context.driver.execute_script('return arguments[0].scrollIntoView();', element)
    
    
    
    
    
    
    
    
    
    
    
    
    