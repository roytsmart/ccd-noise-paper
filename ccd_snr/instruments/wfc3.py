import astropy.units as u
import named_arrays as na
from ._util import (
    _fano_electron,
    _fano_electron_naive,
    _fano_photon,
    _fano_photon_naive,
    _width_diffusion,
)

__all__ = [
    "wavelength",
    "fano_electron",
    "fano_photon",
    "width_pixel",
    "width_diffusion",
]

wavelength = [
    208,
    224,
    240,
    256,
    272,
    288,
    304,
    400,
]

wavelength = na.ScalarArray(wavelength * u.nm, axes="wavelength")

fano_electron = _fano_electron(wavelength)
fano_electron_naive = _fano_electron_naive(wavelength)

fano_photon = _fano_photon(wavelength)
fano_photon_naive = _fano_photon_naive(wavelength)

width_pixel = 15 * u.um

width_diffusion = _width_diffusion(wavelength)
