import re

__all__ = []


def _is_release(version: str) -> bool:
    """
    Whether a version of :mod:`optika` is a release,
    which has documentation and an archive of its own,
    rather than a development version, which has neither.

    Parameters
    ----------
    version
        The version of :mod:`optika`.
    """
    return re.fullmatch(r"\d+\.\d+\.\d+", version) is not None
