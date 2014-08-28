Starting a Fresh Development Environment
========================================

Prerequisites
-------------

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](http://www.vagrantup.com/downloads.html)

Instructions
------------

Clone the repository. Copy the *vm/alephrx.conf.template* and
*vm/createdb.sql.template* files to *vm/alephrx.conf* and *vm/createdb.sql*,
respectively, and edit them to fill in the database connection information you
would like to use.

    $ cp vm/alephrx.conf.template vm/alephrx.conf
    $ cp vm/createdb.sql.template vm/createdb.sql
    # Edit using your favorite editor to replace __DB_NAME__, __DB_USER__, and
    # __DB_PASS__ with your chosen values...

Initialize and provision the VM. The first time you do this, vagrant will need
to download and install the CentOS 5.1 box.

By default, the VM will get a private IP address of 192.168.33.10. If you want
to change it, set the environment variable `ALEPHRX_VM_IP` before calling
`vagrant up` or `vagrant reload`.

    $ cd vm
    $ vagrant up
    # To reload the VM using a different private IP address once
    $ ALEPHRX_VM_IP=192.168.17.17 vagrant reload
    # To use a custom IP without having to enter it any time you want to bring
    # up or reload the VM, export the environment variable, either in your shell
    # or in your .bash_profile
    $ export ALEPHRX_VM_IP=192.168.17.17
    $ vagrant reload

SSH into the new vagrant server to complete the setup.

    $ vagrant ssh

Get a quick data dump from the current ITD server so you have some test data in
the database to play with. Replace credentials as appropriate.

    $ ssh <USER>@itd.umd.edu -t /usr/local/mysql/bin/mysqldump -u<USERNAME> -p<PASSWORD> <DBNAME> | mysql -u<USERNAME> -p<PASSWORD> <DBNAME>

Create a *passwd* file in */apps/git/alephrx* using the Apache *htpasswd*
utility. Add users itdstaff, usmai, 3ALL, and maryland.

    $ htpasswd -c /apps/git/alephrx/passwd itdstaff
    # Enter password info...
    # You only need to use the -c switch the first time, to create the password file
    $ htpasswd /apps/git/alephrx/passwd usmai
    # Enter password info...
    # Repeat for the remaining users

Add a line to your workstation's */etc/hosts* file to map the VM's private IP
address to the name *alephrx.local*. For example, if you are using the default
address:

    192.168.33.10  alephrx.local

For testing using the t/testmail script instead of sendmail as the mailer, the
t/mails directory needs to be created publicly writable (mode 777), so that
Apache can write the mail to files there.

On your workstation, in the alephrx working copy:

    $ mkdir -p t/mails
    $ sudo chmod 777 t/mails
