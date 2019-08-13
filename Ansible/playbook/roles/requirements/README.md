apigw requirements
=========

Checks the HW specs for ram and number of cores, disables unnecessary services. SElinux is also disabled.

Requirements
------------

none

Role Variables
--------------

The variables that can be passed to this role and a brief description about them are as follows:

        # ram in megabytes ~ -200
        min_ram: 1800
        min_cores: 2 
        
The following services are disabled, they are listed under `stop_disable_service_list` default variables. 

        firewalld
        httpd
        sendmail
        postfix
        exim4
        rpcbind
        nfs-common
        dnsmasq             

Dependencies
------------

none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: apigw.requirements }          
         
License
-------


Author Information
------------------
EA: ehab.aboudaya@tecnotree.com


History
-----------------
25.07.2017-EA: inital version  

