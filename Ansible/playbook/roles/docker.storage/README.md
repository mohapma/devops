apigw docker-storage-setup
=========

Configures the storage for docker  

Requirements
------------

Installation of docker from the repo should be sufficent to install epel-relase or rhel-7-server-extras-rpms.

For docker-ce the repo `https://download.docker.com/linux/centos/docker-ce.repo` must be installed. The role
apigw.add.repos_upgrade performs this installation.   

Role Variables
--------------

The variables that can be passed to this role:

        docker_version: "docker-ce"
        docker_storage_block_device: "/dev/sdb"
        docker_storage_filesystem: "xfs"
        docker_storage_vg_name: "docker-vg"
        docker_storage_lv_name: "docker_storage"
        docker_storage_driver: "devicemapper"            

check the [default vars](./defaults/main.yaml) for comments

The following tables indicates docker version with possible storage selection, CentOS Linux release 7.3.1611 
 kernel 3.10.0-514.26.2.el7.x86_64 

docker_storage_driver | docker | docker-ce
--- | --- | ---
 | | 1.12.6 | 17.06.1-ce
default | loop | overlay
devicemapper | OK | OK
overlay2 | NOT SUPPORTED | OK
       
Dependencies
------------

none

Example Playbook
----------------
The files directory contains different files related to repos, check them and use accordingly. Edit the `tasks/main.yml`

    - hosts: servers
      roles:
         - { role: apigw.docker-ce }          
       
with out changes to defaults the play will install docker-ce , latest version and storage on /dev/sdb with devicemapper
driver.        
         
License
-------


Author Information
------------------
EA  ehab.aboudaya@tecnotree.com


History
-----------------
10.08.2017-EA: inital version  
11.08.2017-EA: updates and fixes    
16.08.2017-EA: added comments   
21.08.2017-EA: fixes and updates
