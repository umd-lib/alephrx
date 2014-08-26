Starting a Fresh Development Environment
========================================

Clone the repository. Copy the *vm/alephrx.conf.template* and
*vm/createdb.sql.template* files to *vm/alephrx.conf* and *vm/createdb.sql*,
respectively, and edit them to fill in the database connection information you
would like to use.

    $ cp vm/alephrx.conf.template vm/alephrx.conf
    $ cp vm/createdb.sql.template vm/createdb.sql
    # Edit using your favorite editor to replace __DB_NAME__, __DB_USER__, and
    # __DB_PASS__ with your chosen values...

Initialize and provision the VM.

    $ cd vm
    $ vagrant up

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

Add a line to your workstation's */etc/hosts* file to map the VM's IP address to
the name *alephrx.local*. For example:

    192.168.33.10  alephrx.local

For testing using the t/testmail script instead of sendmail as the mailer, the
t/mails directory needs to be created publicly writable (mode 777), so that
Apache can write the mail to files there.

On your workstation, in the alephrx working copy:

    $ mkdir -p t/mails
    $ sudo chmod 777 t/mails

TODO
----

Ensure that httpd and mysqld start up every time the server reboots.

Make the private IP address and the development hostname configurable.
