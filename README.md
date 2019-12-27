PyPoE
========
Collection of Python Tools for [Path of Exile](https://www.pathofexile.com/).

More detailed docs: [http://omegak2.net/poe/PyPoE/](http://omegak2.net/poe/PyPoE/)

The docs are occasionally updated until I get a build bot up - however docs can also be manually built with sphinx.

[![Build Status](https://travis-ci.org/OmegaK2/PyPoE.svg?branch=dev)](https://travis-ci.org/OmegaK2/PyPoE)

Common problems & advisory
--------
* Install **Python 3.7** for maximum compatibility:
  * UI: PySide currently only supports versions 3.5, 3.6, 3.7 and 3.8
* On windows 10 machines there seems to a be bug in the python install that prevents arguments being passed to the command line interface; you can identify this issue if you get a "help" listing if you supplied more then 1 argument. See [this on stack overflow](https://stackoverflow.com/questions/2640971/windows-is-not-passing-command-line-arguments-to-python-programs-executed-from-t) for possible solutions


Overview
--------
Parts:
* Library toolkit for programmers (PyPoE/poe)
* UI based on QT for browsing the game files
* CLI interface for extracting/exporting data (for the wiki, more TBD)

Resources
-------
* IRC Channel: [freenode.net/#PyPoE](http://webchat.freenode.net/?channels=#PyPoE)
* Discord: No offical channel, but I can be contacted in #tool-dev in the PoE Discord

Imporant Notes
--------
Alpha Stage:
* Code structure and in particular the API may change at any time
* incomplete in many areas (check files and TODOs)
* and tests still have to be written for a lot of things.
* many functions and classes are not yet fully documentated

Dev branch:
* broken code may be committed occasionally to the dev branch

Quick Setup Guide
--------
These instructions are for the current development version of PyPoE.

* Install Python 3.7 & git
* make sure Python 3.7 and python scripts folder is in your %PATH% on windows
* checkout PyPoE with git
* go into the PyPoE folder
* Minimum install: ```pip3 install -e . ```
* Full install: ```pip3 install -e .[full]```

Usage
--------
* UI: ```pypoe_ui```
* CLI: ```pypoe_exporter``` (follow the instructions)
* API: check the individual files in PyPoE/poe/ or the docs [http://omegak2.net/poe/PyPoE/](http://omegak2.net/poe/PyPoE/)

Credits
--------
* [Grinding Gear Games](http://www.grindinggear.com/) - they created many of the file formats and [Path of Exile](https://www.pathofexile.com/) obviously, so do not reuse their files anywhere without their permission and support them if you are able :)
* [Chriskang](http://pathofexile.gamepedia.com/User:Chriskang) and the original [VisualGGPK2](http://pathofexile.gamepedia.com/User:Chriskang/VisualGGPK2)
* [chuanhsing](https://www.reddit.com/user/chuanhsing) ([poedb](http://poedb.tw/us/index.php)) for helping with meaning of certain specification values and retrieving monster stats

Credits - Libraries
-------
* [pyside2](https://wiki.qt.io/Category:LanguageBindings::PySide) ([pypi](https://pypi.org/project/PySide2/))
* [configobj](http://www.voidspace.org.uk/python/configobj.html) ([pypi](https://pypi.python.org/pypi/configobj))
* colorama ([pypi](https://pypi.python.org/pypi/colorama))
* sphinx ([pypi](https://pypi.python.org/pypi/sphinx))
* pytest ([pypi](https://pypi.python.org/pypi/pytest))
* PyOpenGL ([pypi](https://pypi.python.org/pypi/PyOpenGL))
* sqlalchemey ([pypi](https://pypi.python.org/pypi/SQLAlchemy))
* pymysql ([pypi](https://pypi.python.org/pypi/PyMySQL))
* tqdm ([pypi](https://pypi.python.org/pypi/tqdm))
* graphviz ([pypi](https://pypi.python.org/pypi/graphviz))
