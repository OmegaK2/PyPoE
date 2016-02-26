Config
==============================================================================

Config sub commands are accessible with:

:command:`config <subcommand>`

The config will be located in the user folder.

Linux: ~/.PyPoE

Windows: %APPDATA%/PyPoE/

Commands
------------------------------------------------------------------------------

.. _cli-config-get:

config get
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`config get <variable>` is used to get a config variable.

:command:`config get -h` provides a list of available variables.
Alternatively it is also possible to use the :ref:`cli-config-print_all` command.

.. _cli-config-set:

config set
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`config set <variable> <value>` is used to get a config variable.

:command:`config set -h` provides a list of available variables.
Alternatively it is also possible to use the :ref:`cli-config-print_all`
command.

.. _cli-config-print_all:

config print_all
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:command:`config print_all` is used to print a list of the currently
registered config variables and their values.
It will also show missing values.

For example:

.. code-block:: none

    09:11:46 Current stored config variables:
    09:11:46 distributor: DISTRIBUTOR.ALL
    09:11:46 version: VERSION.STABLE

    09:11:46 Missing config variables (require config set):
    09:11:46 out_dir
    09:11:46 temp_dir

If you see an output similar to above, it is required to set the variables shown
in the output with :ref:`cli-config-set`.

For example:

:command:`config set out_dir C:/Out`

:command:`config set temp_dir C:/Temp`

PyPoE Exporter config variables
------------------------------------------------------------------------------

distributor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The distributor to use when scanning for a GGPK file.

A list of valid distributors is located at
:py:class:`PyPoE.poe.constants.DISTRIBUTOR`

The variable accepts both numeric and literal values, however it is recommended
to use the literal value.

version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The version to use when scanning for a GGPK file.

A list of valid versions is located at
:py:class:`PyPoE.poe.constants.VERSION`

The variable accepts both numeric and literal values, however it is recommended
to use the literal value.

temp_dir
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The directory to extract temporary files to. This exists in order to speed
up the commandline for certain actions.

A change to this variable will require :ref:`setup-perform`.

.. warning::
    The selected directory should have enough space to hold the files. Above
    500MB of free space is recommended.

out_dir
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default directory output files are written to.