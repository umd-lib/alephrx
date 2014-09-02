Starting a Fresh Development Environment
========================================

Prerequisites
-------------

- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- [Vagrant](http://www.vagrantup.com/downloads.html)

Instructions
------------

Initialize and provision the VM. The first time you do this, vagrant will need
to download and install the CentOS 5.1 box.

    $ cd vm
    $ vagrant up

By default, the VM will get a private IP address of 192.168.33.10. If you want
to change it, set the environment variable `ALEPHRX_VM_IP` before calling
`vagrant up` or `vagrant reload`.

    # To reload the VM using a different private IP address once
    $ ALEPHRX_VM_IP=192.168.17.17 vagrant reload
    # To use a custom IP without having to enter it any time you want to bring
    # up or reload the VM, export the environment variable, either in your shell
    # or in your .bash_profile
    $ export ALEPHRX_VM_IP=192.168.17.17
    $ vagrant reload

Vagrant creates a database for the application named *alephrx*, with username
*alephrx* and password *alephrx*, and creates the tables required by the
application. It also creates an Apache password file in */apps/git/alephrx* for
HTTP basic authentication with the users *itdstaff*, *usmai*, *3ALL*, and
*maryland*. All of the passwords for these accounts are the same as the
usernames.

The Apache configuration is *copied* into */etc/httpd/conf.d*, so if you wish to
make changes to the running configuration, you should edit the *alephrx.conf*
file found there, and not the one in your working copy.

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

If you want to have some test data to play with, SSH into the new server, and
then get a quick data dump from the current ITD server by calling *mysqldump*
over SSH. Replace credentials on itd.umd.edu as appropriate.

    $ vagrant ssh
    $ ssh <USER>@itd.umd.edu -t /usr/local/mysql/bin/mysqldump --no-create-info -u<USERNAME> -p<PASSWORD> <DBNAME> | mysql -ualephrx -palephrx alephrx

If at any time you need to start over completely, just destroy and recreate the
VM. From your working copy directory:

    $ cd vm
    $ vagrant destroy
    $ vagrant up

Now that you have everything set up, you can go to the following URLs in your
workstation browser to start testing the application:

- Report form: <http://alephrx.local/cgi-bin/ALEPHform.cgi>
- User summary page: <http://alephrx.local/cgi-bin/ALEPH16/ALEPHsum.cgi>
  (username: usmai, password: usmai)
- Staff summary page: <http://alephrx.local/cgi-bin/ALEPH16/ALEPH/ALEPHform2.cgi>
  (username: itdstaff, password: itdstaff)
