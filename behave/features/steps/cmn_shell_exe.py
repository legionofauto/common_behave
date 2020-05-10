import subprocess
from common_functions import scenario_logger

"""
For Windows executions:
Get your Powershell executable path by opening Powershell and running this command:
(get-command powershell.exe).Path
Just do a word search for Plink. 

This is for executing on Windows machines only at this moment. Linux is on the to-do list but will have
to wait. 
"""


def powershell_creds_string(username, password):
    """
    All passwords will be converted to a secure string, then passed through a PowerShell credential object.
    Standard operating procedure from Microsoft. 
    
    Passwords will be converted to a secure string using the method found on Microsoft's site here:
    https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/convertto-securestring?view=powershell-7
    
    How to create the credential management string was pulled straight from Microsoft's site here:
    https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/get-credential?view=powershell-7
    
    :param username: (str) Login account title.
    :param user_pass: (str) Login account password.
    """
    #Just making sure you are passing a string.
    username = str(username)
    password = str(password)
    
    #Saves your password as a secure string.
    secure_string = r'$secpwd = ConvertTo-SecureString "{}" -AsPlainText -Force; '.format(password)
    
    #Saves your user credentials 
    cred_string = secure_string + r'$cred = New-Object System.Management.Automation.PSCredential ({}, $Secure_String_Pwd); '.format(username)
    
    return cred_string


def powershell_invoke_command(cmd, hostname, port=None):
    """
    By putting the "Invoke Command" into it's own function, it allows the user a centralized way to manage what
    they want inside the connection string. There are extra parameters that can be added with options but this
    is it's most basic form. 
    
    Uses PowerShell's Module Microsoft.PowerShell.Core "Invoke-Command" to send a single command 
    to a remote machine using WinRM. See Microsoft's documentation here:
    https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/invoke-command?view=powershell-7
    
    :param cmd: (str) The command you want to execute against the remote Windows machine.
    :param hostname: (str) The hostname or IP address of the remote Windows machine.
    :param port: (int) The port number you want to use to access the remote Windows machine.
    """
    #Just making sure you are passing a string.
    cmd = str(cmd)
    hostname = str(hostname)
    
    if port is not None:
        #Absolutely making sure this is a string
        port = str(port)
        
        #When using curly brackets in a string, not intending "format" to be used, you have to comment them out by using
        #a second curly bracket and not a backslash. 
        invoke_command = 'Invoke-Command -ComputerName {} -Port {} -Credential $cred -ScriptBlock {{ {} }}'.format(hostname, port, cmd)
    else:
        invoke_command = 'Invoke-Command -ComputerName {} -Credential $cred -ScriptBlock {{ {} }}'.format(hostname, cmd)
    
    return invoke_command
    

def execute_local_powershell_cmd(context, cmd, timeout=30, prompt='y\n', jump_user=None, jump_host=None, 
                                 jump_pass=None, jump_port=None):
    """
    Executes a single command. Python doesn't allow for a persistent connection so you have to chain 
    everything into one command.
    
    :param cmd: (str) The command to be ran against the Windows machine.
    :param timeout: (int) Number of seconds you establish before the command times out.
    :param prompt: (str) If you enter a command that requires a response, use this.
    :param jump_host: (str) The jump hostname of the remote machine.
    :param jump_user: (str) Login account title for the jump host.
    :param jump_pass: (str) Login account password for the jump host.
    :param jump_port: (int) The port number you want to use to access the jump host machine.
    """
    #Pulls the PowerShell.exe path from the 'powershell_exe' key in your behave.ini file.
    ps_exe = context.config.userdata['powershell_exe']
    assert ps_exe is not None, 'No PowerShell path found in your behave.ini file!'
    
    if jump_host is not None:
        #Jump host information.
        creds = powershell_creds_string(str(jump_user), str(jump_pass))
        invoke_cmd = powershell_invoke_command(str(cmd), str(jump_host), str(jump_port))
        
        script_block = creds + invoke_cmd
    else:
        script_block = cmd
        
    '''
    The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, 
    and obtain their return codes. The underlying process creation and management in this module is 
    handled by the Popen class.
    
    Class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, 
    preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=None, 
    startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, 
    encoding=None, errors=None, text=None)
    
    args should be a sequence of program arguments or else a single string. By default, the program to 
    execute (PowerShell, Plink, or bin/bash) is the first item in args if args is a sequence.
    '''
    proc = subprocess.Popen([ps_exe, script_block], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    
    try:
        '''
        Communicate interacts with the process and send data to stdin. Read data from stdout and stderr, 
        until end-of-file is reached. Wait for process to terminate.
        
        :returns: A tuple (stdout_data, stderr_data).
        '''
        p = proc.communicate(prompt, timeout=timeout)
        
        #If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised. 
        #Catching this exception and retrying communication will not lose any output.
    except subprocess.TimeoutExpired as e:
        proc.kill()
        scenario_logger(context, e)
        raise subprocess.TimeoutExpired('Timeout error on command "{}"'.format(cmd))
    
    #Logging data for the function.
    logging_info = '\n\n---------------- Local PowerShell Command Execution Info ----------------\n'
    if jump_host is not None:
        logging_info = logging_info  + 'Jump Host Username:\t\t{}\n'.format(str(jump_user))
        logging_info = logging_info  + 'Jump Host Name:\t\t{}\n'.format(str(jump_host))
        if jump_port is not None:
            logging_info = logging_info  + 'Jump Host Port:\t\t{}\n'.format(str(jump_port))
    logging_info = logging_info  + 'PowerShell Command:\n{}\n\n'.format(str(cmd))
    #This is the stdout position in the output tuple.
    if not p[0]:
        logging_info = logging_info  + 'No Standard Output\n\n'
    else:
        logging_info = logging_info  + 'Standard Output:\n{}\nEnd of Standard Output\n\n'.format(str(p[0]))
    
    #This is the stderr position in the output tuple.
    if not p[1]:
        logging_info = logging_info  + 'No Standard Error\n\n'
    else:
        logging_info = logging_info  + 'Standard Error:\n{}\nEnd of Standard Error\n\n'.format(str(p[1]))
    logging_info = logging_info  + '---------------- End Local PowerShell Command Execution ----------------\n\n'
    
    #Logs all PowerShell information passed. 
    scenario_logger(context, logging_info)
    
    return p


def execute_powershell_winrm_cmd(context, cmd, hostname, username, user_pass, prompt='y\n', timeout=30,
                                 port=None, jump_host=None, jump_user=None, jump_pass=None, jump_port=None):
    """
    Executes a single command through a WinRM connection. Python doesn't allow for a persistent connection
    so you have to chain everything into one command.
    
    
    :param cmd: (str) The command to be ran against the target Windows machine.
    :param hostname: (str) domain name or IP address assigned to a target machine.
    :param username: (str) Login account title.
    :param user_pass: (str) Login account password.
    :param prompt: (str) If you enter a command that requires a response, use this.
    :param timeout: (int) Number of seconds you establish before the command times out.
    :param port: (int) The port number you want to use to access the remote machine.
    :param jump_host: (str) The jump hostname of the remote machine.
    :param jump_user: (str) Login account title for the jump host.
    :param jump_pass: (str) Login account password for the jump host.
    :param jump_port: (int) The port number you want to use to access the jump host machine.
    :return: A tuple of the standard output and standard error in string format.
    """
    #Pulls the PowerShell.exe path from the 'powershell_exe' key in your behave.ini file.
    ps_exe = context.config.userdata['powershell_exe']
    assert ps_exe is not None, 'No PowerShell path found in your behave.ini file!'
    
    if jump_host is not None:
        
        #The final host execution command string
        creds = powershell_creds_string(username, user_pass)
        invoke_cmd = powershell_invoke_command(cmd, hostname, port)
        
        script_block = creds + invoke_cmd
        
        #Takes the original invoke_command and puts it inside the jump host invoke_command.
        jump_creds = powershell_creds_string(jump_user, jump_pass)
        jump_invoke_cmd = powershell_invoke_command(script_block, jump_host, jump_port)
        
        script_block = jump_creds + jump_invoke_cmd
    else:
        creds = powershell_creds_string(username, user_pass)
        invoke_cmd = powershell_invoke_command(cmd, hostname, port)
        
        script_block = creds + invoke_cmd
        
    #Runs yoru command.
    proc = subprocess.Popen([ps_exe, script_block], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    try:
        p = proc.communicate(prompt, timeout=timeout)
        
        #If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised. 
        #Catching this exception and retrying communication will not lose any output.
    except subprocess.TimeoutExpired as e:
        proc.kill()
        scenario_logger(context, e)
        raise subprocess.TimeoutExpired('Timeout error on command "{}"'.format(cmd))
    
    #Showing off a different way of doing this.
    stdout = p[0]
    stderr = p[1]
    
    #Logging data for the function.
    logging_info = '\n\n---------------- Remote PowerShell Command Execution Info ----------------\n'
    logging_info = logging_info  + 'Login Username:\t\t{}\n'.format(username)
    logging_info = logging_info  + 'Login Host:\t\t{}\n'.format(hostname)
    if jump_host is not None:
        logging_info = logging_info  + 'Jump Host Username:\t{}\n'.format(jump_user)
        logging_info = logging_info  + 'Jump Hostname:\t\t{}\n'.format(jump_host)
        if jump_port is not None:
            logging_info = logging_info  + 'Jump Host Port:\t\t{}\n'.format(jump_port)
    logging_info = logging_info  + 'PowerShell Command:\t{}\n\n'.format(cmd)
    if not stdout:
        logging_info = logging_info  + 'No Standard Output\n\n'
    else:
        logging_info = logging_info  + 'Standard Output:\n{}\nEnd of Standard Output\n\n'.format(stdout)
    
    if not stderr:
        logging_info = logging_info  + 'No Standard Error\n\n'
    else:
        logging_info = logging_info  + 'Standard Error:\n{}\nEnd of Standard Error\n\n'.format(stderr)
    logging_info = logging_info  + '---------------- End Remote PowerShell Command Execution ----------------\n\n'
    
    #Logs all PowerShell information passed. 
    scenario_logger(context, logging_info)
    
    return stdout, stderr


def execute_plink_cmd(context, cmd, hostname, username, user_pass, port=22, prompt='y\n', timeout=30,
                      conn_type='ssh', plink_opt='-x', jump_host=None, jump_user=None, jump_pass=None, 
                      jump_port=None, initial_login=False):
    """
    Plink is a command line application. This means that you cannot just double-click on its icon to 
    run it and instead you have to bring up a console window. In Windows 95, 98, and ME, this is called 
    an 'MS-DOS Prompt', and in Windows NT, 2000, and XP, it is called a 'Command Prompt'.
    
    The jump host I'm expecting is going to be Linux based. The connection from the jump host to the
    target host will be using SSH.
    
    This function sends a single command to a host via SecureShell
    
    plink data for this function was collected here:
    https://www.ssh.com/ssh/putty/putty-manuals/0.68/Chapter7.html
    
    
    :param cmd: (str) The command to be ran against the target machine.
    :param hostname: (str) domain name or IP address assigned to a target machine.
    :param username: (str) Login account title.
    :param user_pass: (str) Login account password.
    :param port: (int) The port number you want to use to access the remote machine.
    :param prompt: (str) If you enter a command that requires a response, use this.
    :param timeout: (int) Number of seconds you establish before the command times out.
    :param conn_type: (str) Can use ssh, telnet, rlogin, serial
    :param plink_opt: (str) The Plink options you want to use with your connection.
    :param jump_host: (str) The jump hostname of the remote machine.
    :param jump_user: (str) Login account title for the jump host.
    :param jump_pass: (str) Login account password for the jump host.
    :param jump_port: (int) The port number you want to use to access the jump host machine.
    :param initial_login: (bool)
    :return: A tuple of the standard output and standard error in string format.
    """
    #Pulls the PowerShell.exe path from the 'powershell_exe' key in your behave.ini file.
    ps_exe = context.config.userdata['powershell_exe']
    assert ps_exe is not None, 'No PowerShell path found in your behave.ini file!'
    #Pulls the plink.exe path from the 'plink_exe' key in your behave.ini file.
    plink_exe = context.config.userdata['plink_exe']
    assert plink_exe is not None, 'No Plink path found in your behave.ini file!'
    
    if initial_login:
        echo_y = 'echo y | '
    else:
        echo_y = ''
    
    
    if jump_host is not None:
        
        #Makes sure the jump_port variable is populated. 
        if jump_port is None:
            jump_port = '22'
        
        #Uses native Linux ssh command to remote to the final destination.
        script_block = 'ssh {} -P {} -pw {} {}@{} {}{}'.format(plink_opt, str(port), user_pass, username, hostname, echo_y, cmd)
        
        #Jump host uses the initial script_block in the command entry section. 
        script_block = '{} -{} {} -P {} -pw {} {}@{} {}{}'.format(plink_exe, conn_type, plink_opt, str(jump_port), jump_pass, jump_user, jump_host, echo_y, script_block)
        
    else:
        
        script_block = '{} -{} {} -P {} -pw {} {}@{} {}{}'.format(plink_exe, conn_type, plink_opt, str(port), user_pass, username, hostname, echo_y, cmd)
        
    
    #Run the command.
    proc = subprocess.Popen([ps_exe, script_block], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    try:
        #Another way of executing stdout and stderr.
        stdout, stderr = proc.communicate(prompt, timeout=timeout)
        
        #If the process does not terminate after timeout seconds, a TimeoutExpired exception will be raised. 
        #Catching this exception and retrying communication will not lose any output.
    except subprocess.TimeoutExpired as e:
        proc.kill()
        scenario_logger(context, e)
        raise subprocess.TimeoutExpired('Timeout error on command "{}"'.format(cmd))
    
    #Logging data for the function.
    logging_info = '\n\n---------------- Plink Command Execution Info ----------------\n'
    logging_info = logging_info  + 'Login Username:\t\t{}\n'.format(username)
    logging_info = logging_info  + 'Login Host:\t\t{}\n'.format(hostname)
    if jump_host is not None:
        logging_info = logging_info  + 'Jump Host Username:\t{}\n'.format(jump_user)
        logging_info = logging_info  + 'Jump Hostname:\t\t{}\n'.format(jump_host)
        logging_info = logging_info  + 'Jump Host Port:\t\t{}\n'.format(str(jump_port))
    logging_info = logging_info  + 'Login Port:\t\t{}\n'.format(str(port))
    logging_info = logging_info  + 'Connection Type:\t{}\n'.format(conn_type)
    logging_info = logging_info  + 'Options used:\t\t{}\n'.format(plink_opt)
    logging_info = logging_info  + 'Shell Command:\t\t{}\n\n'.format(cmd)
    if not stdout:
        logging_info = logging_info  + 'No Standard Output\n\n'
    else:
        logging_info = logging_info  + 'Standard Output:\n{}\nEnd of Standard Output\n\n'.format(stdout)
    
    if not stderr:
        logging_info = logging_info  + 'No Standard Error\n\n'
    else:
        logging_info = logging_info  + 'Standard Error:\n{}\nEnd of Standard Error\n\n'.format(stderr)
    logging_info = logging_info  + '---------------- End Plink Command Execution ----------------\n\n'
    
    #Logs all Plink information passed. 
    scenario_logger(context, logging_info)
    
    return stdout, stderr

