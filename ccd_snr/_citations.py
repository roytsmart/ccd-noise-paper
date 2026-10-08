import json
import datetime
import urllib.parse
import urllib.request
import importlib.metadata
from ._versions import _is_release

__all__ = [
    "bibtex_optika",
]

_conceptrecid_optika = 23074621
"""The Zenodo record that every archived release of :mod:`optika` is a version of."""


def _zenodo(path: str, **params: str) -> dict:
    """
    Query the REST API of Zenodo.

    Parameters
    ----------
    path
        The path of the endpoint, relative to ``https://zenodo.org/api/``.
    params
        The parameters of the query.
    """
    url = f"https://zenodo.org/api/{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def bibtex_optika(version: None | str = None) -> str:
    """
    A BibTeX entry, with the key ``optika``, citing a version of :mod:`optika`
    by its archive on Zenodo.

    A release is cited by the DOI of its own archive,
    so the citation names the version this article was built with.
    A development version has no archive of its own,
    so it is cited by the concept DOI, which resolves to the latest release.

    Parameters
    ----------
    version
        The version of :mod:`optika`.
        If :obj:`None` (the default), the installed version is used.
    """
    if version is None:
        version = importlib.metadata.version("optika")

    is_release = _is_release(version)

    if is_release:
        records = _zenodo(
            "records",
            q=f'conceptrecid:{_conceptrecid_optika} AND metadata.version:"v{version}"',
            all_versions="true",
        )["hits"]["hits"]
        if not records:
            raise ValueError(
                f"optika v{version} has not been archived on Zenodo, "
                f"so there is no DOI to cite it by."
            )
        (record,) = records
        doi = record["doi"]
    else:
        record = _zenodo(f"records/{_conceptrecid_optika}/versions/latest")
        doi = record["conceptdoi"]

    metadata = record["metadata"]

    fields = dict(
        author=" and ".join(creator["name"] for creator in metadata["creators"]),
        title=metadata["title"],
        year=datetime.date.fromisoformat(metadata["publication_date"]).year,
        publisher="Zenodo",
    )
    if is_release:
        fields["version"] = metadata["version"]
    fields["doi"] = doi
    fields["url"] = f"https://doi.org/{doi}"

    lines = [f"    {key} = {{{value}}}," for key, value in fields.items()]

    return "\n".join(["@software{optika,", *lines, "}"]) + "\n"
