# Install Vim, Apache, and MySQL; the MySQL package also installs the Perl DBI
# and DBD::MySQL Perl modules as dependencies.

package { 'vim-common':
    ensure => present,
}
package { 'vim-enhanced':
    ensure => present,
}
package { 'vim-minimal':
    ensure => present,
}
package { 'httpd':
    ensure => present,
}
package { 'mysql-server':
    ensure => present,
}
package { 'mysql':
    ensure => present,
}
