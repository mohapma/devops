apigw sysctl hosts
=========

Configures kernel and system parameters to the recommened settings. Adds hostnames and ip to the /etc/hosts file. 

Requirements
------------

none

Role Variables
--------------

The variables that can be passed to this role and a brief description about them are as follows:

        external_hosts_list: []
        # example
        #  - { ip: "194.42.63.195", alias: "registry.tecnotree.com proxy-registry.tecnotree.com" }
        
The following services are disabled, they are listed under `stop_disable_service_list` default variables. 

        firewalld
        httpd
        sendmail
        postfix
        exim4
        rpcbind
        nfs-common
        dnsmasq             

the host name is set according to the `inventory_hostname` and must be an IP address.

Dependencies
------------

none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: apigw.sysctl_hosts }
         
         
License
-------


Author Information
------------------
EA: ehab.aboudaya@tecnotree.com


History
-----------------
20.07.2017-EA: inital version  

