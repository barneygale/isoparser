import iso
import source


def parse(path_or_url):
    """
    Returns an :class:`ISO` object for the given filesystem path or URL.
    """
    if path_or_url.startswith("http"):
        src = source.HTTPSource(path_or_url)
    else:
        src = source.FileSource(path_or_url)
    return iso.ISO(src)