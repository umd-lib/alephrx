# use the puppetlabs-mysql module
# this also ensures that the MySQL server package is installed
include mysql::server

# Install Vim, Apache, and Perl modules
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

# LIBILS-38 added a dependency on the URI module
package { 'perl-URI':
    ensure => present,
}

# LIBILS-43 added a dependency on HTML::Entities, which is part of the
# HTML::Parser package
package { 'perl-HTML-Parser':
    ensure => present,
}

# LIBILS-45 added a dependency on Moose and XML::Simple
# perl-Moose is available through the EPEL repository, so install that first
# on RHEL, must use:
#     rpm -i http://mirror.umd.edu/fedora/epel/5/i386/epel-release-5-4.noarch.rpm
package { 'epel-release':
    ensure => present,
}
package { 'perl-Moose':
    ensure  => present,
    require => Package['epel-release'],
}
package { 'perl-XML-Simple':
    ensure => present,
}

# configure the hosts file, so Apache will dispatch to the right vhost
host { 'alephrx.local':
    ip => '127.0.0.1',
}

# create the MySQL database and user
mysql::db { 'alephrx':
    user     => 'alephrx',
    password => 'alephrx',
    host     => 'localhost',
    grant    => ['ALL'],
}
