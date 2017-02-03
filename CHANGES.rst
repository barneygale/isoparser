Changelog
=========

v0.3
----

- Added support for Python 3. Many thanks to Daniel Wozniak and Michał Barciś

v0.2
----

- Added fairly comprehensive support for SUSP, and mostly-complete support for
  Rock Ridge. Thanks to Danielle Church for the patch.
- Improved the fetch behavior, by minimizing number of fetches (causing seek
  latency for local files, or excess HTTP header traffic) and minimizing memory
  usage for the ISO object by not caching backing sectors for file content.
  Thanks to Danielle Church for the patch.
- Added ``get_stream()`` method to Record objects, which returns a file-like
  object. Thanks to Danielle Church for the patch.
- Added support for using ``parse()`` as a context manager. Thanks to
  Jean Olivier for the initial patch.
- The ``Record.is_hidden`` and ``Record.is_directory`` flags are now booleans.
  Thanks to Jean Olivier for the patch.
- Fixed issue that prevented ``pip install isoparser`` working. Thanks to
  Jordan Speicher for the patch.

v0.1
----

- Initial release
