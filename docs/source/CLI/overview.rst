Overview
==============================================================================

The command line interface of PyPoE features various utilities split up into
command line scripts.

Currently there are the following scripts:

:command:`pypoe_exporter`
  Exporting functionality for the Path of Exile wiki and .dat files


Invoking a script without any additional parameters will implicitly tell you
about the available sub commands and command line options.
However, it is possible to explicitly open the help by specifying :command:`-h`
or :command:`--help`.

So for example:

:command:`pypoe_exporter -h`


Each of the scripts comes with their own :ref:`CLI/config`. In order to use the
scripts the config variables need to be set first, then the setup needs to be
performed.