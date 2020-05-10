This project was meant to be a starting point for automating information systems. Change
these functions as needed. This project is intended to use on Windows machines only at 
this time. 


Getting Python Modules:

Open a PowerShell and copy/paste the following commands
pip install -U behave
pip install -U ipdb
pip install -U selenium
pip install -U requests
pip install -U Appium-Python-Client

-or if you are in a closed environment-

Go through your software change management process

Download the file from here:
https://pypi.org/

Unzip the file, open a Powershell window or Linux terminal, change directory to the
unzipped folder main directory with the setup.py file in it, type the
command "python setup.py install". This should install everything. 

Be sure to look through the setup.py file for all of the dependencies for the modules.


If you are running both Python2 and Python3, and the library deploys to Python2 lib. 
Just cut and paste the new libraries into the Python3 library.

Running behave:

Behave is just and executable. There is nothing magical about it. It's not complicated.
Anyone that tells you otherwise is lying. You can literally copy someone else's project
to anyplace, change working directory to the new project root folder, and execute.
For behave  to run the project, you PowerShell current working directory needs to 
contain the "behave.ini" file. Easiest to just use the root folder "behave" and using 
the "run_behave.py" file to execute.

Set up your "behave.ini" and "user_properties.ini" file with the specific information 
the variables require. For the behave.ini file, please see the behave Documentation:
1.5.2  Configuration Files
https://readthedocs.org/projects/python-behave/downloads/pdf/latest/

The behave.exe reads a specific file structure. Feature file should be put inside the 
"feature" folder. You can have sub folders for feature file and behave will still find
them. Your "environment.py" file is the only Python file that can be located outside
of your "steps" folder. All other project Python files need to be under "steps". Be sure
to put "__init__.py" for every folder that contains Python files.

Example project directory structure:

tests/
tests/environment.py
tests/features/signup.feature
tests/features/login.feature
tests/features/account_details.feature
tests/steps
/tests/steps/website.py
tests/steps/utils.py


Selenium Requirements:
Selenium is supposed to work with three component: Client, Standalone Server jar and Driver exe. At this 
point, you should have the client. The server can be downloaded here:
https://www.selenium.dev/downloads/

Try to stick with the same version client you have. The most popular Selenium drivers can be found here:
https://www.selenium.dev/documentation/en/getting_started_with_webdriver/third_party_drivers_and_plugins/