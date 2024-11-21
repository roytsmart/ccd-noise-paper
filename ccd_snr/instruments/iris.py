import astropy.units as u
import named_arrays as na
from ._util import _fano_electron, _fano_photon

__all__ = [
    "index_1330",
    "wavelength",
    "fano_electron",
    "fano_photon",
]

wavelength = [
    1330,
    1400,
    2796,
    2832,
]

index_1330 = dict(wavelength=wavelength.index(1330))

wavelength = na.ScalarArray(wavelength * u.AA, axes="wavelength")

fano_electron = _fano_electron(wavelength)
fano_photon = _fano_photon(wavelength)
