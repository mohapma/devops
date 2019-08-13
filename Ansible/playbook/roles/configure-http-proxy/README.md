Configure HTTP proxy for Docker
=========

This role configures http proxy for Docker 

Requirements
------------

HTTP and HTTPS proxy URLs can be added in ../defaults/main.yml

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
         - { role: configure-http-proxy, force_reboot: no }

License
-------



Author Information
------------------
PVe  pasi.vepsa@tecnotree.com


History
-----------------
30.07.2018: PVe: inital version  

