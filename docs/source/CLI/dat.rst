Dat Exporter
==============================================================================

Setup sub commands are accessible with:

:command:`dat <subcommand>`

Commands
------------------------------------------------------------------------------

dat json
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`dat json <target> [--files FILE [FILE ...]]`

The dat json export is used to export .dat files to json format.

The resulting json will roughly look like this:

.. code-block:: json

    [
        {
            // One of the files you've specified in the --files parameter
            "filename": "FILE",
            // headers in order from the dat specification
            "headers": [
                {
                    // name of the header
                    'name': 'Name',
                    [ ... ] // other fields
                },
                ... // other headers
            ]
            "data": [
                // Each row
                [ ... ],
            ],
        },
        ... // other files
    ]

For details on what the extra fields mean in the headers, please see
the dat specification file:
https://github.com/OmegaK2/PyPoE/blob/dev/PyPoE/_data/dat.specification.ini

dat sql
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`dat sql [--url URL] [--skip-data] [--skip-child-data]`
:command:`[--files FILE [FILE ...]]`

http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine

.. warning::
    Only the MySQL driver is supported