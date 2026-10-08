import pytest
import ccd_snr


@pytest.mark.parametrize(
    argnames="version,doi,version_cited",
    argvalues=[
        ("2.11.1", "10.5281/zenodo.23074622", "v2.11.1"),
        ("2.11.2.dev14+g7d61a68ed", "10.5281/zenodo.23074621", None),
    ],
)
def test_bibtex_optika(version: str, doi: str, version_cited: None | str):
    result = ccd_snr.bibtex_optika(version)
    assert result.startswith("@software{optika,\n")
    assert f"    doi = {{{doi}}},\n" in result
    assert f"    url = {{https://doi.org/{doi}}},\n" in result
    if version_cited is None:
        assert "    version = " not in result
    else:
        assert f"    version = {{{version_cited}}},\n" in result


def test_bibtex_optika_unarchived():
    """optika 2.11.0 was released before its releases were archived."""
    with pytest.raises(ValueError, match="Zenodo"):
        ccd_snr.bibtex_optika("2.11.0")
