GGPK Viewer
===============================================================================

The GGPK Viewer is as the name suggests an utility to browse the contents of
Path of Exile's content.ggpk.

Features in a nutshell:

* browsing the ggpk content file tree
* searching for files using regular expressions (see :py:mod:`re`)
* extracting of files or directories
* live opening of various file formats, but in particular the proprietary .dat
  file format

.. note::
    Opening the GGPK may take several seconds depending on your disk and cpu
    speed.

Viewing .dat files
-------------------------------------------------------------------------------

The GGPK Viewer includes the ability to view the binary .dat files.

They're parsed in a way that provides extra information about the entries
for viewing purposes and in particular updating PyPoE's .dat specification.

In particular information about pointers is kept intact and parsed into a table
format adjusted , as such the dat viewer can be much slower then the API
counter-part (i.e :class:`DatFile`).

.. warning::
    Opening large .dat files such as GrantedEffectsPerLevel.dat will 'hang'
    the UI until the processing is completed.

As soon a .dat file is opening, filters can be applied to the individual
rows by right-clicking the header columns.

Columns can also be sorted by left-clicking on them.