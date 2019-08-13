apigw reboot
=========

Checks if the host requires a reboot based on the last update and reboots the host.     

Requirements
------------

none

Role Variables
--------------

none
        
Dependencies
------------
none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: apigw.reboot}          

License
-------


Author Information
------------------
EA  ehab.aboudaya@tecnotree.com


History
-----------------
05.08.2017-EA: inital version  

