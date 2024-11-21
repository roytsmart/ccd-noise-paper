import astropy.units as u
import named_arrays as na
from ._util import _fano_electron, _fano_photon

__all__ = [
    "wavelength",
    "fano_electron",
    "fano_photon",
]

wavelength = [
    94,
    131,
    171,
    193,
    211,
    304,
    335,
    1600,
    1700,
]

wavelength = na.ScalarArray(wavelength * u.AA, axes="wavelength")

fano_electron = _fano_electron(wavelength)
fano_photon = _fano_photon(wavelength)
