Installing PyPoE
==============================================================================

Prerequisites
------------------------------------------------------------------------------

Python 3.5+
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The current version of PyPoE requires Python 3.5 and higher. It is recommended
to use the latest python version.

The python commandline, the scripts from the script installation directory as
well as pip should be accessible after this step from the command line of
your Operating System.

**Windows**

* Navigate to https://www.python.org/downloads/ and download the latest version
  of Python
* Install and follow the instructions on the installer
* Make sure the python executable and the python scripts folder are located
  within your %PATH% environment variable

.. note::

    If Python is not in your %PATH% it can be manually added in your system
    control panel (System -> Advanced -> Envrionment Variables -> System
    Variables)

**Linux**

Generally python is included with most distributions and can be accessed as
python3.
It may be possible that your distribution uses an old package, in that case
you may need to upgrade python or install from a custom upstream repo if it
isn't available.

Commands for some distributions:

* Ubuntu/Debian: apt-get install python3 python3-pip

Git
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
After this step the git commandline should be accessible.

**Windows**

* Navigate to https://git-scm.com/ and download the latest version of git
* Make sure git is added to the %PATH% envrionment variable

**Linux**

* Ubuntu/Debian: apt-get install git

Qt4 (UI only, Linux only)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Windows**

This step can be skipped on windows as QT is available in binary form from pip.

**Linux**

See http://pyside.readthedocs.org/en/latest/building/linux.html for details.

It's possible that for some reason some sphinx dependencies fail to install
causing the compiling of pyside to fail.
In that case you can try running:

* :command:`pip install docutils jinja2 babel imagesize alabaster pygments`


Downloading & Installing PyPoE
------------------------------------------------------------------------------

.. warning::
    The installation instructions are currently aimed at the deveopment build
    as there is no stable release of PyPoE yet

.. warning::
    On some **Linux** distributions the commands python and pip may link to
    either version 2 or 3 of python.
    It is recommended to check which version the distribution uses; on some
    distributions you can explicitly use python3 and pip3 instead of python and
    pip respectively.

Navigating to a installation folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* Open a command line of your choice
* Navigate to a folder you wish to have PyPoE installed from
* Run: :command:`git clone https://github.com/OmegaK2/PyPoE.git`
* Navigate into the checked folder to the level where **setup.py** resides

Invoking PIP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To use the development install which allows editable you can specify **-e** on
the commandline.

By default, PyPoE only installs the dependencies for the core (PyPoE.poe).
However, there are additional packages available:

+-----------+-----------------------------------------------------------------+
|Package    |Description                                                      |
+-----------+-----------------------------------------------------------------+
|cli        |Basic CLI support                                                |
+-----------+-----------------------------------------------------------------+
|cli-full   |Meta-Package for all CLI packages                                |
+-----------+-----------------------------------------------------------------+
|dev        |Support for development utilities (documentation & testing)      |
+-----------+-----------------------------------------------------------------+
|ui         |Support for the graphical user interface                         |
+-----------+-----------------------------------------------------------------+
|ui-extra   |Support for rendering DDS via OpenGL                             |
+-----------+-----------------------------------------------------------------+
|ui-full    |Meta-Package for all UI packages                                 |
+-----------+-----------------------------------------------------------------+
|full       |Meta-Package for all packages (recommended)                      |
+-----------+-----------------------------------------------------------------+

The minimum installation would be:

:command:`pip install -e .`

To install specific packages add them separated by a comma in brackets:

:command:`pip install -e .[ui,ui-extra]`

For the full installation use:

:command:`pip install -e .[full]`