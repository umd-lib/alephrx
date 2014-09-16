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

# LIBILS-38 added a dependency on the URI module
package { 'perl-URI':
    ensure => present,
}

# LIBILS-43 added a dependency on HTML::Entities, which is part of the
# HTML::Parser package
package { 'perl-HTML-Parser':
    ensure => present,
}

# LIBILS-45 added a dependency on XML::Simple
package { 'perl-XML-Simple':
    ensure => present,
}
