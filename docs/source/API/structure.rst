Project Structure
==============================================================================

The project is organized in various folders

+-------------+---------------------------------------------------------------+
|Directory    |Description                                                    |
+-------------+---------------------------------------------------------------+
|/            |The root project folder. Only the very core files such as the  |
|             |setup file or the LICENSE file should reside here.             |
+-------------+---------------------------------------------------------------+
|/docs/       |The root folder for the documentation.                         |
|             |It contains scripts and build files as well as the source      |
|             |subdirectory                                                   |
+-------------+---------------------------------------------------------------+
|/docs/source |Source documentation files and description that are not        |
|             |contained in the python source files themselves.               |
|             |Also contains templates and some generated files.              |
+-------------+---------------------------------------------------------------+
|/scripts     |Collection of scripts intended to be invoked from the command  |
|             |line.                                                          |
|             |Unlike the other items, the scripts do not ahere to the same   |
|             |quality standards                                              |
+-------------+---------------------------------------------------------------+
|/tests/      |Tests for py.test                                              |
+-------------+---------------------------------------------------------------+
|/PyPoE/      |Root python folder                                             |
+-------------+---------------------------------------------------------------+
|/PyPoE/_data/|Shared data used by the other files.                           |
+-------------+---------------------------------------------------------------+