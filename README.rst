isoparser
=========

This python library can parse the `ISO 9660`_ disk image format. It can load ISOs from the local
filesystem or via HTTP, and will only read and cache sectors as necessary. You list directory
contents, extract files, and retrieve metadata.

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

.. _`ISO 9660`: http://wiki.osdev.org/ISO_9660
