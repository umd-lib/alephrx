Database
========

Server version is MySQL 3.23.38 on production. CentOS development VM is running
MySQL 5.0.95.

Terminology and Problem Domain Notes
====================================

A common status flow is: Assigned (STAFF) -> User input needed -> Assigned
(STAFF). This is managed by using the *PURPLE* filter on the staff summary view,
which highlights "user input needed" reports that have a user reply on them.

System distinguishes between a *response*, which is created by a staff member,
and a *reply*, which is created by an end user.

The functional area is used to determine which listservs or reflectors to send
emails to.

Questions
---------

    1. What does "suppressed" do to a report?
    2. What are the most common types of requests? Reports, password resets, and
       circulation requests are the top ones.

Tables in Aleph Rx
==================

Active
------

**people**: Identifying information on the person reporting the issue. This
record is created first, and the `id` is used when creating the associated row
in the `report` table.

**report**: The issue information. Linked to the `person` table through having
the same `id`, not through a foreign key relationship. (Does this application
predate foreign keys in MySQL MyISAM tables?)

**reply**: Replies to the issue report. The `parent_id` column references the
`id` in the `report` table, although (as with the `people`-`report`
relationship), it is not a formal foreign key.

**kbase**: ???

Unused/Inactive
---------------

**response**: The only references in the code are commented out, and the table
is empty on the server.

**RXreply**: No references to this table in the code. On the server, it appears
that the RXreply table was migrated to the reply table between 2006-04-29
17:46:24 and 2006-04-30 20:26:07.

    mysql> select count(*) from RXreply;
    +----------+
    | count(*) |
    +----------+
    |     5170 |
    +----------+
    1 row in set (0.00 sec)
    
    mysql> select count(*) from reply;
    +----------+
    | count(*) |
    +----------+
    |    30887 |
    +----------+
    1 row in set (0.00 sec)
    
    mysql> select max(date) from RXreply;
    +---------------------+
    | max(date)           |
    +---------------------+
    | 2006-04-29 17:46:24 |
    +---------------------+
    1 row in set (0.02 sec)
    
    mysql> select count(*) from reply where date > '2006-04-29 17:46:24';
    +----------+
    | count(*) |
    +----------+
    |    25717 |
    +----------+
    1 row in set (0.06 sec)
    
    mysql> select min(date) from reply where date > '2006-04-29 17:46:24';
    +---------------------+
    | min(date)           |
    +---------------------+
    | 2006-04-30 20:26:07 |
    +---------------------+
    1 row in set (0.10 sec)

Unknown Status
--------------

**t**: It does not appear to be referenced in the code anywhere, but it is
non-empty on the server
