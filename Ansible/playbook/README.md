### Ansible deployment guide for docker

This readme explains the necessary steps to install Docker using ansible. Ansible is a free automation engine that
automates configuration management, cloud provisioning and application deployment.

#### Requirements

* The control machine "local host" and target hosts should have at least python 2.7+
* The control machine should have ansible installed.
* Target hosts should be reachable via ssh.
* The target hosts should be able to connect to the repository network locations.
* 

The deployment can be carried out in steps in ansible terms they are called plays or roles. If a play execution fails 
then it can be re-execute again without starting from the previous role. It is a good idea to limit the target host. 


#### Installing Ansible on RedHat OS family 
This is the minimal install requirment to install ansible and roles dependencies.

    $ sudo yum clean all # good practice start fresh and update
    $ sudo yum update
    $ sudo yum install -y epel-release  # for centos if not already installed
    $ sudo yum install -y python-pip python-netaddr ansible
    
At time of writing this guide ansible version is 2.4 and a simple test produces

    $ ansible --version
    ansible 2.4.2.0
    
    $ ansible all -i 'localhost,' -c local -m ping
    localhost | SUCCESS => {
        "changed": false, 
        "ping": "pong"
    }

#### Configure the inventory files
It is important to setup the inventory with correct corresponding target vm values. There is an example under inventories.

- `inventories/hosts` definition of target hosts including specifying the rancher server and port. 
- `inventories/group_vars/all` general configurations applied to all target hosts.
- `roles/apigw.add_repos_upgrade` if there is/are any custom repo files or other repository. *Note: edit `tasks/main.yml`*

To test the inventory a simple ping test should report back with SUCCESS:

    $ ansible all -m ping
    e02.apigw.local | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }
    e01.apigw.local | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }
    e03.apigw.local | SUCCESS => {
        "changed": false,
        "ping": "pong"
    }

There are other variables for each group and var names are self explanatory, but the two above files are most important to get 
started. 

#### Running the deployment plays

The correct default directory to run the plays should be started from where ansible.cfg or this readme file exists.
  
The plays exists under the playbooks directory and When setting up a new target the order of plays should carried out this way:  

**1**. [prerequisites.yml](./playbooks/prerequisites.yml)

**2**. [configure.yml](./playbooks/configure.yml)

**3**. [docker.yml](./playbooks/docker.yml)

**4**. [finalize.yml](./playbooks/finalize.yml)

**5**. [configure_docker.yml](./playbooks/configure_proxy.yml)


If a play fails then one can fix the problems and rerun the same play. Each play has enough comment to use it and the task
names are also self explanatory. While we can use the ssh_config file to define some paramters the next examples do not
use any ssh_config definitions.  


```bash
$ pwd
/home/tcusr/deployment/ansible
 
$ ansible-playbook -u tecnotree -k -K ./playbooks/prerequisites.yml
```

**Note**: tecnotree is a remote user with sudo preveliages.

It is also possible a single or multiple target host(s) fails, one can run a play on single target or added to the
inventory group.

```bash
$ ansible-playbook -u tecnotree -k -K ./playbooks/prerequisites.yml -e target_hosts=vm1
```

If a play is successful there will be a report "list" of tasks executed and time consumed. On the otherhand if a play fails
there will be an error output and should be read or reported to understand what went wrong.
