isoparser
=========

This python library can parse the `ISO 9660`_ disk image format including
`Rock Ridge`_ extensions. It can load ISOs from the local filesystem or via
HTTP, and will only read and cache sectors as necessary. You list directory
contents, extract files, and retrieve metadata.

UNMAINTAINED
------------

This package is unmaintained. The author now maintains the pathlab_ package,
which includes support for ISO 9660 and Rock Ridge. The pycdlib_ package
may also be of interest if you need Joliet / UDF support.

Installation
------------

.. code-block:: console

    $ pip install isoparser

Usage
-----

.. code-block:: python

    import isoparser

    iso = isoparser.parse("http://www.microsoft.com/linux.iso")

    print iso.record("boot", "grub").children
    print iso.record("boot", "grub", "grub.cfg").content

.. _`ISO 9660`: https://en.wikipedia.org/wiki/ISO_9660
.. _`Rock Ridge`: https://en.wikipedia.org/wiki/Rock_Ridge
.. _`pathlab`: https://github.com/barneygale/pathlab
.. _`pycdlib`: https://github.com/clalancette/pycdlib
