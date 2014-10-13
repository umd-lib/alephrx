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

What are the most common types of requests? Reports, password resets, and
circulation requests are the top ones.

Tables in Aleph Rx
==================

Active
------

**people**: Identifying information on the person reporting the issue. This
record is created first, and the `id` is used when creating the associated row
in the `report` table.

- **id:** ID number for the Rx. This value is shared with the *report* table,
  and is used in URLs that reference specific Rxes. It is an auto-incrementing
  integer value, and also the primary key for this table.
- **grp:** The functional area. In the user interface, this value is constrained
  by a single-select dropdown.
- **campus:** The campus. In the user interface, this value is constrained by a
  single-select dropdown.
- **phone:** The phone number of the user reporting the issue.
- **name:** The name of the user reporting the issue.
- **email:** The email address of the user reporting the issue.
- **timestamp:** Not used (there is no non-null data in the column on
  production, and no references to this column in the code). The
  `report.timestamp` is used to record the Rx creation time.

**report**: The issue information. Linked to the `person` table through having
the same `id`, not through a foreign key relationship. (Does this application
predate foreign keys in MySQL MyISAM tables?)

- **id:** ID number for the Rx. This value is shared with the *people* table,
  and is used in URLs that reference specific Rxes. It is the primary key for
  this table, but it is not auto-incrementing, as it is always set manually using
  the last inserted row id from the *people* table.
- **date:** The initial submission date of the request.
- **grp:** Not used (there is no non-null data in the column on production, and
  no references to this column in the code). The `people.grp` column is always
  used instead to track the functional area of an Rx.
- **status:** The Rx status.
- **summary:** The brief text summary of the issue. In the UI, this is the
  "Problem Summary" field.
- **text:** The full text of the issue report.
- **supress:** Flag indicating whether this Rx should be hidden from the summary
  views, searches, and reports. Values are "yes" or "no". Typically used to
  indicate that an Rx is being used to test some new feature or fix.
- **cataloger:** The name of the person submitting the Rx, if it is different
  from the person reporting the request. In the UI this is the "Submitted by"
  field.
- **assigned:** Not used (there is no non-null data in this column on
  production, and no references to this column in the code). The `status` column
  is used instead to track who this Rx is assigned to, by having an "Assigned
  (XX)" status for each staff member, where "XX" is that person's initials.
- **timestamp:** Creation timestamp for this Rx. This is not updated after the
  record is created.
- **updated:** Last updated timestamp for this Rx. It is initially set the same
  as *timestamp*, but it is changed when a a reply is created or when the status
  of the Rx is updated.
- **version:** The version of Aleph?

**reply**: Replies to the issue report. The `parent_id` column references the
`id` in the `report` table, although (as with the `people`-`report`
relationship), it is not a formal foreign key.

- **id:** The ID of this reply. This is an auto-incrementing integer value, and
  also the primary key for this table.
- **parent_id:** The ID of the Rx that this is a reply to. Note that this is not
  a formal foreign key relationship to either the *people* or *report* tables.
- **name:** The name of the person submitting the reply/response.
- **date:** The creation date of the reply. This is never changed.
- **text:** The text of the reply message.
- **timestamp:** The timestamp of the last time this reply is updated. This is
  intially *not* set, and is only updated if a staff member edits the reply
  using the ALEPHureply.cgi script.
- **itd:** Flag to indicate whether this is a staff response (submitted through
  the ALEPHurecord.cgi script) or a user reply (submitted through the
  ALEPHxreply.cgi script). Values are "yes" or "no".

Unused/Inactive
---------------

**response**: The only references in the code are commented out, and the table
is empty on the production server. This was most likely a first attempt to
separate responses (i.e. staff comments) form replies (i.e. user comments) that
was ultimately done through having a `reply.itd` column. **RECOMMENDATION:**
Remove this table.

**RXreply**: No references to this table in the code. On the server, it appears
that the RXreply table was migrated to the reply table between 2006-04-29
17:46:24 and 2006-04-30 20:26:07. **RECOMMENDATION:** Remove this table.

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

**kbase**: Knowledge base records. This may or may not be active, since although
there is data in this table on production, the scripts to view the knowledge
base appear to be incomplete.
