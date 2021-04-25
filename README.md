**Development is currently discontinued**

PyPoE
========

Collection of Python Tools for [Path of Exile](https://www.pathofexile.com/).

More detailed docs: [http://omegak2.net/poe/PyPoE/](http://omegak2.net/poe/PyPoE/)

The docs are occasionally updated until I get a build bot up - however docs can also be manually built with Sphinx.

[![Build Status](https://travis-ci.org/OmegaK2/PyPoE.svg?branch=dev)](https://travis-ci.org/OmegaK2/PyPoE)

Common Problems & Advisory
--------
* Install **Python 3.7** for maximum compatibility:
* To support bundle decompression check out https://github.com/zao/ooz, compile it and place libooz.dll in the python directory
* **UI will be reworked for bundle support and is not functional at the moment**
* On Windows 10 machines there seems to a be bug in the Python installation that prevents arguments being passed to the command line interface; you can identify this issue if you get a "help" listing if you supplied more then 1 argument. See [this on stack overflow](https://stackoverflow.com/questions/2640971/windows-is-not-passing-command-line-arguments-to-python-programs-executed-from-t) for possible solutions


Overview
--------
Parts:
* Library toolkit for programmers (PyPoE/poe)
* UI based on Qt for browsing the game files
* CLI interface for extracting/exporting data (for the wiki, more TBD)

Resources
-------
* IRC Channel: [freenode.net/#PyPoE](http://webchat.freenode.net/?channels=#PyPoE)
* Discord: No official channel, but I can be contacted in #3rd-party-tool-dev in the /r/PathOfExile Discord

Important Notes
--------
Alpha Stage:
* Code structure and in particular the API may change at any time
* Incomplete in many areas (check files and TODOs)
* Tests still have to be written for a lot of things.
* Many functions and classes are not yet fully documented

Dev branch:
* Broken code may be committed occasionally to the dev branch

Quick Setup Guide
--------
These instructions are for the current development version of PyPoE.

* Install Python 3.7 & git
* On Windows, make sure Python 3.7 and Python "Scripts" folder are in %PATH%
* Checkout PyPoE with git
* Go into the PyPoE folder
* Minimum install: ```pip3 install -e . ```
* Full install: ```pip3 install -e .[full]```
* Download and compile https://github.com/zao/ooz with cmake
* Place the resulting libooz.dll in the python folder

Usage
--------
* UI: ```pypoe_ui```
* CLI: ```pypoe_exporter``` (follow the instructions)
* API: check the individual files in PyPoE/poe/ or the docs [http://omegak2.net/poe/PyPoE/](http://omegak2.net/poe/PyPoE/)

Credits - People
--------
* [Grinding Gear Games](http://www.grindinggear.com/) - they created many of the file formats and [Path of Exile](https://www.pathofexile.com/) obviously, so do not reuse their files anywhere without their permission and support them if you are able to :)
* [Chriskang](http://pathofexile.gamepedia.com/User:Chriskang) and the original [VisualGGPK2](http://pathofexile.gamepedia.com/User:Chriskang/VisualGGPK2)
* [chuanhsing](https://www.reddit.com/u/chuanhsing) ([poedb](http://poedb.tw/us/index.php)) for helping with meaning of certain specification values and retrieving monster stats

Credits - Libraries
-------
* [pyside2](https://wiki.qt.io/Qt_for_Python) ([pypi](https://pypi.org/project/PySide2/))
* [configobj](http://www.voidspace.org.uk/python/configobj.html) ([pypi](https://pypi.org/project/configobj/))
* colorama ([pypi](https://pypi.org/project/colorama/))
* sphinx ([pypi](https://pypi.org/project/sphinx/))
* pytest ([pypi](https://pypi.org/project/pytest/))
* PyOpenGL ([pypi](https://pypi.org/project/PyOpenGL/))
* tqdm ([pypi](https://pypi.org/project/tqdm/))
* graphviz ([pypi](https://pypi.org/project/graphviz/))
* mwclient ([pypi](https://pypi.org/project/mwclient/))
* mwclientparserfromhell ([pypi](https://pypi.org/project/mwparserfromhell/))
* rapidfuzz ([pypi](https://pypi.org/project/rapidfuzz/))
