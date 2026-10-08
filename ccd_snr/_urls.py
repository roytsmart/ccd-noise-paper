import importlib.metadata
from ._versions import _is_release

__all__ = [
    "url_docs_optika",
]


def url_docs_optika(version: None | str = None) -> str:
    """
    The URL of the documentation of a version of :mod:`optika`.

    Read the Docs keeps the documentation of every release of :mod:`optika`,
    so linking to the release this article was built with keeps the links
    valid after later releases rename or remove what they point to.
    A development version has no documentation of its own,
    so it gives the latest documentation instead.

    Parameters
    ----------
    version
        The version of :mod:`optika`.
        If :obj:`None` (the default), the installed version is used.
    """
    if version is None:
        version = importlib.metadata.version("optika")

    if _is_release(version):
        slug = f"v{version}"
    else:
        slug = "latest"

    return f"https://optika.readthedocs.io/en/{slug}"
