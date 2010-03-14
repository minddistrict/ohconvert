ohconvert
=========

Overview
--------

ohconvert integrates ohcount_ into Hudson_.

This script invokes ohcount, parses its output and converts it into a
sloccount.sc file in the format defined by sloccount_. This format is understood
by the existing SLOCCountPlugin_ plugin for Hudson.

Prerequisites
-------------

You need to have ohcount_ 3.0.0 or later installed and it needs to be directly
executable from the path. You can check by calling ``ohcount --help``. ohcount
can be built manually or is available from some system package management tools.
For example it's available as ``ohcount`` in the latest macports_.

The script needs at least Python 2.5 to run. It's not compatible with any
Python 3.x version at this point.

Usage
-----

You can call the script via::

  python2.5 ohconvert.py <folder>

It will output an intermediate ``ohcount.sc`` and the final ``sloccount.sc``
file in the current directory.


.. _ohcount: http://ohcount.sourceforge.net/
.. _Hudson: http://hudson-ci.org/
.. _sloccount: http://www.dwheeler.com/sloccount/
.. _SLOCCountPlugin: http://wiki.hudson-ci.org/display/HUDSON/SLOCCount+Plugin
.. _macports: http://www.macports.org/
