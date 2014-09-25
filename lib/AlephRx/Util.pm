package AlephRx::Util;

our $FROM = 'AlephRx <alephrx@umd.edu>';
our $REPLY_TO = 'usmaialeph@umd.edu';

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
        name => 'other',
        recipient => 'usmaialeph@umd.edu',
        slug => 'OTHR:',
    },
);

# mappings for quick recipient and slug lookups, given the functional area name
our %RECIPIENT_FOR = map { $_->{name} => $_->{recipient} } @FUNCTIONAL_AREAS;
our %SLUG_FOR      = map { $_->{name} => $_->{slug}      } @FUNCTIONAL_AREAS;

# module return
1;
