from cmn_shell_exe import execute_local_powershell_cmd, execute_powershell_winrm_cmd, execute_plink_cmd
from common_functions import get_usr_prop
from behave import given


@given('I run powershell command "{ps_command}"')
def given_i_run_powershell_command_cmd(context, ps_command):
    """
    Executes PowerShell with the given command. Used just for initial testing purpose.
    Mess around with it all you want. 
    """
    stdout, stderr = execute_local_powershell_cmd(context, ps_command)
    
    #No errors
    assert not stderr, "you messed up."
    
    #Prints your output.
    print(stdout)


@given('the "{host}" host is online')
def given_the_host_is_online(context, host):
    """
    Verifies IP-level connectivity to the target host machine. If the host is online, 
    the scenario can proceed. 
    
    Ping information found here:
    https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/ping
    
    :param host: (str) The hostname or ip address of the machine you want
        status from.
    """
    host = str(host)
    cmd = r'ping /n 1 {}'.format(host)
    stdout, stderr = execute_local_powershell_cmd(context, cmd)
    
    #Checks for errors first.
    assert not stderr, 'An error occurred when executing the ping command for host {}'.format(host)
    
    #Checks if the host was found in DNS.
    assert 'could not find host' not in stdout, 'No host found for "{}" in domain!'.format(host)
    
    #If the packet loss is anything other than 0%, the scenario is failed.
    assert 'Lost = 0 (0% loss)' in stdout, 'No packets were returned for host "{}"'.format(host)


@given('the "{user}" user account can WinRM to "{host}" host')
def given_the_authorized_user_account_can_winrm_to_specified_host(context, user, host):
    """
    Since the execute_powershell_winrm_cmd is a singleton and does not create a persistent 
    connection to the host, this step will assure the user that you can connect.
    
    :param user: (str) User account information you want to pull form your 
        user_properties.ini file.
    :param host: (str) The hostname or ip address of the machine you wish 
        to log into.
    """
    #The get_usr_prop function returns user property information from your 
    #user_properties.ini file.
    username = get_usr_prop(context, user)
    user_pass = get_usr_prop(context, user + ".password")
    
    stdout, stderr = execute_powershell_winrm_cmd(context, 'echo hello', host, username, user_pass)
    
    assert not stderr, "An error occurred."
    assert 'hello' in stdout, "'hello' was not found in standard out."
    
    print(stdout)


@given('the "{user}" user account can SSH to "{host}" host')
def given_the_authorized_user_account_can_ssh_to_specified_host(context, user, host):
    """
    Sends a single command to the target host machine via SecureShell. Does not create a persistent
    connection to the host. Python is horrible about this. I have a Java class that does create
    a persistent connection but will implement that later. 
    
    :param user: (str) User account information you want to pull form your 
        user_properties.ini file.
    :param host: (str) The hostname or ip address of the machine you wish 
        to log into.
    """
    username = get_usr_prop(context, user)
    user_pass = get_usr_prop(context, user + ".password")
    
    stdout, stderr = execute_plink_cmd(context, 'echo hello', host, username, user_pass)
    assert not stderr, "An error occurred."
    assert 'hello' in stdout, "'hello' was not found in standard out."
    
    print('You successfully logged into the server via SSH')

