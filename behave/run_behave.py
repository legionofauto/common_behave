import subprocess


"""
For Windows, find the behave.exe with PowerShell using the following command:
(get-command behave.exe).Path

For Linux, just type "behave" 

Instructions:
Copy and paste the path into the "<behave path>" placeholder, uncomment the line, Right-click on this 
file, move to "Run as", and click on "Python Run". See Behave's Documentation "1.5.1 Command-Line 
Arguments" for mor information on how to run behave from the command-line.

running the argument "behave" will run everything.
running "behave -t selenium_test_chrome" will execute all features, scenarios or example tables marked
with the tag "selenium_test_chrome"
"""


#p = subprocess.Popen([r'C:\<behave path>\Python\Python37\Scripts\behave.exe', '-t', 'selenium_test_ie']).communicate()
#p = subprocess.Popen([r'C:\<behave path>\Scripts\behave.exe', '-t', 'pyautgui_test']).communicate()
#p = subprocess.Popen([r'C:\<behave path>\behave.exe', '-t', 'rest_get_test']).communicate()
#p = subprocess.Popen([r'C:\<behave path>\behave.exe', '-t', 'powershell_feature_test']).communicate()

#Windows version
#p = subprocess.Popen([r'<behave path>', '-t', 'selenium_test_feature']).communicate()

#Linux version
#p = subprocess.Popen([r'behave', '-t', 'selenium_test_feature']).communicate()

#Run everything using the option below
#p = subprocess.Popen([r'behave']).communicate()