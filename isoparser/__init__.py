import iso
import source


def parse(path_or_url, cache_content=False):
    """
    Returns an :class:`ISO` object for the given filesystem path or URL.

    cache_content:
      Whether to store sectors backing file content in the sector cache. If true, this will
      cause memory usage to grow to the size of the ISO as more file content get accessed.
      Even if false (default), an individual Record object will cache its own file content
      for the lifetime of the Record, once accessed.
    """
    if path_or_url.startswith("http"):
        src = source.HTTPSource(path_or_url, cache_content=cache_content)
    else:
        src = source.FileSource(path_or_url, cache_content=cache_content)
    return iso.ISO(src)
