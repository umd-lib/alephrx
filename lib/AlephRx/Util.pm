package AlephRx::Util;

=head1 NAME

AlephRx::Util - AlephRx application configuration and utilities.

=head1 DESCRIPTION

This module gathers together application-level configuration information used by
the various scripts of the AlephRx application.

=head2 $AlephRx::Util::FROM

The email address used in the C<From:> header of all notification emails. Per
issue LIBILS-37, this cannot be a reflector address that might show up in the
C<To:> header, since the UMD email system will likely reject that email.

=cut
our $FROM = 'AlephRx <alephrx@umd.edu>';

=head2 $AlepRx::Util::REPLY_TO

The email address used in the C<Reply-To:> header of all notification emails.
While users are instructed not to reply directly to the notification emails,
this is put in place so that just in case they do, the replies will go to a
mailbox or list that is being monitored.

=cut
our $REPLY_TO = 'usmaialeph@umd.edu';

=head2 @AlephRx::Util::FUNCTIONAL_AREAS

List of all functional areas used in the application. Each item is a hashref
with the keys C<name>, C<recipient>, and C<slug>.

The C<name> is both the display name for the area in the UI as well as the value
that is stored in the database.

The C<recipient> is the email address or addresses for the default recipient of
notification emails for reports with a given functional area.

The C<slug> is a short abbreviation for the functional area that is used int he
email subject line.

=cut
our @FUNCTIONAL_AREAS = (
    {
        name => 'Password reset',
        recipient => 'usmaialeph@umd.edu',
        slug => 'PSWD:',
    },
    {
        name => 'Report request',
        recipient => 'usmaialeph@umd.edu',
        slug => 'RQST:',
    },
    {
        name => 'Change request',
        recipient => 'usmaialeph@umd.edu',
        slug => 'CHNG:',
    },
    {
        name => 'Acquisitions',
        recipient => 'usmaicoiseracq@umd.edu',
        slug => 'ACQ:',
    },
    {
        name => 'Cataloging',
        recipient => 'usmaicoicatdbmaint@umd.edu',
        slug => 'CAT:',
    },
    {
        name => 'Circulation',
        recipient => 'usmaicoicircresill@umd.edu',
        slug => 'CIRC:',
    },
    {
        name => 'Item Maintenance',
        recipient => 'usmaicoicircresill@umd.edu,usmaicoicatdbmaint@umd.edu,usmaicoiseracq@umd.edu',
        slug => 'ITM:',
    },
    {
        name => 'Reserves',
        recipient => 'usmaicoicircresill@umd.edu,usmaicoiuserinter@umd.edu',
        clug => 'RES:',
    },
    {
        name => 'ILL',
        recipient => 'ilug@umd.edu,usmaicoicircresill@umd.edu',
        slug => 'ILL:',
    },
    {
        name => 'Serials',
        recipient => 'usmaicoiseracq@umd.edu',
        slug => 'SER:',
    },
    {
        name => 'Technical',
        recipient => 'usmaicoidesktech@umd.edu',
        slug => 'TECH:',
    },
    {
        name => 'Web OPAC',
        recipient => 'usmaicoiuserinter@umd.edu',
        slug => 'OPAC:',
    },
    {
        name => 'OLE Testing',
        recipient => 'usmaialeph@umd.edu',
        slug => 'OLE-TEST:',
    },
    {
        name => 'other',
        recipient => 'usmaialeph@umd.edu',
        slug => 'OTHR:',
    },
);

=head2 %AlephRx::Util::RECIPIENT_FOR

Mapping of functional area C<name> to C<recipient>.

=head2 %AlephRx::Util::SLUG_FOR

Mapping of functional area C<name> to C<slug>.

=cut
# mappings for quick recipient and slug lookups, given the functional area name
our %RECIPIENT_FOR = map { $_->{name} => $_->{recipient} } @FUNCTIONAL_AREAS;
our %SLUG_FOR      = map { $_->{name} => $_->{slug}      } @FUNCTIONAL_AREAS;

# module return
1;
