Package update
=========

This role updates packages, yum update excluding docker-ce 

Requirements
------------


Role Variables
--------------

        
Dependencies
------------

none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: update_packages, force_reboot: no }

License
-------



Author Information
------------------
PVe  pasi.vepsa@tecnotree.com


History
-----------------
09.08.2018: EA: inital version  

