PyPoE
========
Collection of Python Tools for Path of Exile.

Parts:
* Library toolkit for programmers (PyPoE/poe)
* UI based on QT for browsing the game files
* CLI interface for extracting/exporting data (for the wiki, more TBD)

Overview
--------
Alpha:
* Code structure may change at any time
* incomplete in many areas (check files and TODOs)
* and tests still have to be written for a lot of things.

Quick Setup Guide
--------

* Install Python 3.4
* make sure Python 3.4 and python scripts folder is in your %PATH% on windows
* checkout PyPoE with git
* go into the PyPoE folder
* run ```python setup.py develop ```
* For extra ui support,  run ```pip install -e .[ui]```
* For extra development libs, run```pip install -e .[dev]```
