import astropy.units as u
import named_arrays as na

__all__ = [
    "wavelength",
    "energy",
]


def wavelength() -> na.ScalarArray:
    """
    The wavelength grid used throughout this article.
    """
    return na.geomspace(1.5, 10000, axis="wavelength", num=1001) * u.AA


def energy() -> na.ScalarArray:
    w = wavelength()
    return w.to(u.eV, equivalencies=u.spectral())
