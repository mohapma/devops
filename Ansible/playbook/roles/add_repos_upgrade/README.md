apigw add repos and upgrade
=========

This role add repos in different format or installs a common repo e.g: epel_relase 

Requirements
------------

repo files can be added in the files directory, make sure to edit the `main.yml` file and edit as necessary.

Role Variables
--------------

The variables that can be passed to this role and a brief description about them are as follows:

        # repos to be installed for CentOS distro
        CentOS:
          - epel-release
        
        # repos to be installed for RHEL distros
        RedHat:
          - rhel-7-server-extras-rpms
        
        # if there is a kernel diff upgrade the reboots is done, this forces reboot in any case if is yes   
        force_reboot: no
        
Dependencies
------------

none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: apigw.add_repos_upgrade, force_reboot: no }

License
-------



Author Information
------------------
EA  ehab.aboudaya@tecnotree.com


History
-----------------
05.08.2017: EA: inital version  

