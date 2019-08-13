Add Docker and other specific repos
=========

This role add repos  e.g: docker-ce.repo 

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
         - { role: add_docker_repo, force_reboot: no }

License
-------



Author Information
------------------
PVe  pasi.vepsa@tecnotree.com


History
-----------------
10.08.2018: PVe: inital version  

