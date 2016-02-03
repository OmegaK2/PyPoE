Contributing
===============================================================================

Everyone is generally welcome to contribute to the project.

There are basically 3 ways to do so:

* Feature requests & :doc:`reporting issues <report_issue>`
* Sending pull requests
* Becoming a dev

Pull requests
-------------------------------------------------------------------------------

You're welcome to send a pull request on github for features or changes you
think that should be in PyPoE.

Please keep a few things in mind:

* the code in the request should be well behaved and a proper fix or addition
* the change should be under the MIT license
* if it's an entirely new feature, it may debatable whether it is has a place
  in PyPoE
* the submitted code should:
  * be well behaved and a proper fix or addition
  * be PEP8 compatible (minus the line-length)
  * include changes in the respective tests or new tests
  * validate against existing tests (if tests were changed, validate against
    those)
* backwards incompatible changes are more suited for the dev branch

So for example:

* Likely to be accepted

  * general improvements to existing code of UI, CLI or API
  * new, well-behaved features that extend the existing functional
  * support for missing file formats
  * updated dat.specification.ini
  * additional tests

* Likely to be rejected

  * changes unrelated to the goal of the project
  * refusal of making the change itself available under MIT license
  * changes with poor coding style

Become a dev
-------------------------------------------------------------------------------

If you want to become an active developer and meet the requirements please
contact me. I'll manually unlock people for access to the repo.

.. note::

    If you just want to contribute a few changes, there is no need to become a
    dev and you can send pull requests instead.

    If you just want your own repo, just fork the project on github.

**Requirements**

* You should

  * have a good amount of experience with developing in Python 3
  * be willing to actively contribute, i.e. making changes on your own, working
    on the TODOs
  * be fluent in English (written); no you don't have to be a perfect speaker,
    but you're English should be good enough to have no issues with
    communication
  * be available in the IRC channel
* I'll want to see some pieces of code you've written; a good history of
  pull requests will suffice, otherwise:

  * another open source project you've been involved in,
  * some private things you've written but are willing to let me have a look at

It would be extra helpful, if you:

* have experience with C/C++ and writing embedded python libraries with C/API
* have a lot of experience with Path of Exile [for the api]
* are experienced with using Mediawiki [for exporter]
* speak other languages fluently or natively [for translating the project]
* are adept with reverse engineering [to help with api]
