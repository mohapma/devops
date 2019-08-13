Role for updating Docker-ce to certain version
=========

This role updates docker-ce to certain version

Requirements
------------

Make sure to edit the `main.yml` file and define the docker-ce version you wish to update to.

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
         - { role: docker_update, force_reboot: no }

License
-------



Author Information
------------------
PVe  pasi.vepsa@tecnotree.com


History
-----------------
09.08.2018: PVe: inital version  

