@powershell_feature_test
Feature: Local PowerShell test
  The WinRM and SSH tests will fail as is. You will have to pick a
  host that you can log into. Also, make sure the user_properties.ini
  file is updated with the correct user information for a successful
  run.

  @powershell_local_test
  Scenario: PowerShell local command test
    Given I run powershell command "ls"

  @powershell_winrm_test
  Scenario Outline: PowerShell WinRM test <host>
    Given the "<host>" host is online
      And the "<user>" user account can WinRM to "<host>" host

    @powershell_winrm_facebook_test
    Examples: 
      | user      | host             |
      | oper.user | ww5.acebook.com  |
      | oper.user | www.facebook.com |

    @powershell_winrm_ssh_test
    Examples: 
      | user      | host        |
      | oper.user | www.ssh.com |

  @powershell_ssh_test
  Scenario Outline: 
    Given the "<host>" host is online
      And the "<user>" user account can SSH to "<host>" host

    Examples: 
      | user      | host        |
      | oper.user | www.ssh.com |
