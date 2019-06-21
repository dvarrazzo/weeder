Remove unneeded historical files
================================

You may have backups.

Every day, your precious stuff is saved in a safe place.

But you may have too much of that...

This script will select for you what files to drop, based on a retention policy
such that as files get older you can keep less of them. The default policy
will keep all the files in the last two weeks, a file every week for the last
three months, a file every month for the last year, a file every year forever.

The script takes in input the existing files on command line and by default
will print on stdout the files to delete. You can use a chain of commands such
as::

    ls | xargs weeder | xargs rm

to run in a cron job every day to keep your backup directories light.


Our glorious help
-----------------

Running ``weeder -h`` you might be told::

    usage: weeder [-h] [-p AGE:DIST [AGE:DIST ...]] [-f REGEX] [-r YYYY-MM-DD]
                  [--print-keepers | --print-goners] [-q | -v]
                  [FILE [FILE ...]]

    positional arguments:
      FILE                  the files to weed

    optional arguments:
      -h, --help            show this help message and exit
      -p AGE:DIST [AGE:DIST ...], --policy AGE:DIST [AGE:DIST ...]
                            state that, of every file older than AGE days, we want
                            to keep at least one every DIST days
                            [default: 14:7 84:28 364:364]
      -f REGEX, --format REGEX
                            the pattern to extract a date from a file name
                            [default: (\d{4})-(\d{2})-(\d{2})]
      -r YYYY-MM-DD, --refdate YYYY-MM-DD
                            reference date to establish retention [default: today]
      --print-keepers       print the files to keep
      --print-goners        print the files to delete [default]
      -q, --quiet           talk less
      -v, --verbose         talk more

but who knows, really.


Running tests
-------------

You can run::

    python3 setup.py test
