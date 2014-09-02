Summary View Screens
====================

End Users
---------

Script: [cgi-bin/ALEPH16/ALEPHsum.cgi](../cgi-bin/ALEPH16/ALEPHsum.cgi)

### Filters ###

|Button Label|POST variable name|Filter meaning|
|------------|------------------|--------------|
|Acquisitions|ACQ|Functional area is "Acquisitions"|
|Circulation|CIRC|Functional area is "Circulation"|
|Cataloging|CAT|Functional area is "Cataloging"|
|Item Maintenance|ITM|Functional area is "Item Maintenance"|
|Reserves|RES|Functional area is "Reserves"|
|ILL|ILL|Functional area is "ILL"|
|Serials|SRQ|Functional area is "Serials"|
|Web OPAC|PAC|Functional area is "Web OPAC"|
|Technical|TECH|Functional area is "Technical"|
|New|NEW|Status is "new"|
|Pending|PEND|Status is "pending"|
|Active|ACTIVE|Status is any of the following: "change request", "new", "pending", "assigned", "user input needed", or "sent to functional group"|
|Change Request|CHANGE|Functional area is "Change request"|
|Closed|CLOSED|Status is "closed"|
|Report Requests|REPORT|Functional area is "Report Request"|
|All Summaries|ALL|All reports (no filter)|

Note that the *Active* filter does not check whether the report has any of the
individual assigned statuses (e.g., "assigned (HB)"), so if a report is assigned
to a staff member, that report does not appear on the end users summary view of
active reports.

Staff
-----

Script: [cgi-bin/ALEPH16/ALEPHsum.cgi](../cgi-bin/ALEPH16/ALEPHsum.cgi)

### Filters ###

|Button Label|POST variable name|Filter meaning|
|------------|------------------|--------------|
|Acquisitions:|ACQ|Functional area is "Acquisitions"|
|Circulation:|CIRC|Functional area is "Circulation"|
|Cataloging:|CAT|Functional area is "Cataloging"|
|Item Maintenance:|ITM|Functional area is "Item Maintenance"|
|Reserves:|RES|Functional area is "Reserves"|
|ILL:|ILL|Functional area is "ILL"|
|Serials:|SRQ|Functional area is "Serials"|
|Web OPAC:|PAC|Functional area is "Web OPAC"|
|Technical:|TECH|Functional area is "Technical"|
|All Assigned:|ASSN|Status begins with "assigned"|
|Assigned (HB):|ASSNHB|Status is "assigned (HB)"|
|Assigned (HH):|ASSNHH|Status is "assigned (HH)"|
|Assigned (DW):|ASSNDW|Status is "assigned (DW)"|
|Assigned (YQ):|ASSNYQ|Status is "assigned (YQ)"|
|Assigned (MH):|ASSNMH|Status is "assigned (MH)"|
|Assigned (LS):|ASSNLS|Status is "assigned (LS)"|
|Assigned (US):|ASSNUS|Status is "assigned (US)"|
|New:|NEW|Status is "new"|
|Pending:|PEND|Status is "pending"|
|PURPLE:|PURPLE|Status is "user input needed"|
|Change Request:|CHANGE|Functional area is "Change request"|
|RECENT:|PRE|*Does nothing; this is likely a bug, since a user would expect a "RECENT" filter to filter by date*|
|Deferred:|DEFR|Status is "deferred"|
|Report Request:|REPORT|Functional area is "Report Request"|
|All Summaries:|ALL|All reports (no filter)|
|Not Closed:|NOTCLOSED|Status is not "closed"|
