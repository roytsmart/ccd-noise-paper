import astropy.units as u
import named_arrays as na
from ._util import (
    _fano_electron,
    _fano_electron_naive,
    _fano_photon,
    _fano_photon_naive,
)

__all__ = [
    "index_1330",
    "index_1400",
    "wavelength",
    "fano_electron",
    "fano_photon",
    "width_pixel",
]

wavelength = [
    1330,
    1400,
    2796,
    2832,
]

index_1330 = dict(wavelength=wavelength.index(1330))
index_1400 = dict(wavelength=wavelength.index(1400))

wavelength = na.ScalarArray(wavelength * u.AA, axes="wavelength")

fano_electron = _fano_electron(wavelength)
fano_electron_naive = _fano_electron_naive(wavelength)

fano_photon = _fano_photon(wavelength)
fano_photon_naive = _fano_photon_naive(wavelength)

width_pixel = 13 * u.um
