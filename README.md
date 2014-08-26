Aleph Rx
========

This is the code for the Aleph ticket tracking system for USMAI Consortium. This
is the system that is currently running on the itd.umd.edu server with the
following entry points:

- End-users: http://itd.umd.edu/cgi-bin/ALEPHform.cgi
- DSS Staff: http://itd.umd.edu/cgi-bin/ALEPH16/ALEPH/ALEPHform2.cgi

Codebase
--------

- **cgi-bin:** CGI scripts making up the bulk of the application
- **docs:** Documentation
    - [aleph16.mwb](docs/aleph16.mwb): MySQL Workbench diagram of the database
      schema
    - [aleph16.sql](docs/aleph16.sql): The database schema (table definitions)
    - [codefixes.md](docs/codefixes.md): Notes on how to generally improve the
      codebase
    - [database.md](docs/database.md): List of tables and columns in the
      database schema
    - [pageflow.dot](docs/pageflow.dot): Source code for the pageflow.png
      diagram
    - [pageflow.png](docs/pageflow.png): Diagram of the navigation and form
      submission connections between the CGI scripts
    - [scripts.md](docs/scripts.md): List of all the CGI scripts and their
      general functionality
- **htdocs:** Static files used by the application
- **t:** Test scripts and utilities
