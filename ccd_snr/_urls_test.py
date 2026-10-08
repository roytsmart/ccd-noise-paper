import importlib.metadata
import pytest
import ccd_snr


@pytest.mark.parametrize(
    argnames="version,url",
    argvalues=[
        ("2.11.1", "https://optika.readthedocs.io/en/v2.11.1"),
        ("3.0.0", "https://optika.readthedocs.io/en/v3.0.0"),
        ("2.11.2.dev14+g7d61a68ed", "https://optika.readthedocs.io/en/latest"),
        ("3.0.0rc1", "https://optika.readthedocs.io/en/latest"),
    ],
)
def test_url_docs_optika(version: str, url: str):
    assert ccd_snr.url_docs_optika(version) == url


def test_url_docs_optika_installed():
    version = importlib.metadata.version("optika")
    assert ccd_snr.url_docs_optika() == ccd_snr.url_docs_optika(version)
