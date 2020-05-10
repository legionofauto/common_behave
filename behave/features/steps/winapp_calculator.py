from appium.webdriver import Remote
from behave import given

"""
Find the app name with PowerShell using the following command:
get-StartApps | Where-Object {$_.Name -like '*Calculator*'}

Have not gotten this to work yet. On the to-do list.
"""


@given('Windows Calculator is open')
def open_task_manager(context):
    desired_caps = {}
    desired_caps['app'] = 'Microsoft.WindowsCalculator_8wekyb3d8bbwe!App'
    desired_caps['platformName'] = 'Windows'
    desired_caps['deviceName'] = 'WindowsPC'
    context.calculator = Remote('http://127.0.0.1:4723/', desired_caps)
