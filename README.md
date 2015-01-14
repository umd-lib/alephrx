Aleph Rx
========

This is the code for the Aleph ticket tracking system for USMAI Consortium. This
is the system that is currently running on the itd.umd.edu server with the
following entry points:

- End-users: http://usmai.umd.edu/alephrx/cgi-bin/ALEPHform.cgi
- DSS Staff: http://usmai.umd.edu/alephrx/cgi-bin/ALEPH16/ALEPH/ALEPHform2.cgi

Codebase
--------

- **[cgi-bin](cgi-bin):** CGI scripts making up the bulk of the application
- **[docs](docs):** Documentation
- **[htdocs](htdocs):** Static files used by the application
- **[lib](lib):** Custom Perl modules used by the application
- **[t](t):** Test scripts and utilities
- **[vm](vm):** Vagrantfile and related scripts to create and provision a development
  VM environment

Development Environment
-----------------------

To set up a fresh development environment, clone this repository and then follow
the instructions in [vm/README.md](vm/README.md).
