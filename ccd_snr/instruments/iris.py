import astropy.units as u
import named_arrays as na
from ._util import (
    _vmr_electron,
    _vmr_photon,
    _snr_improvement,
    _width_diffusion,
)

__all__ = [
    "index_1330",
    "index_1400",
    "wavelength",
    "width_pixel",
    "vmr_electron",
    "vmr_photon",
    "snr_improvement",
    "width_diffusion",
]

wavelength = [
    1330,
    1400,
    2796,
    2832,
]

width_pixel = 13 * u.um

index_1330 = dict(wavelength=wavelength.index(1330))
index_1400 = dict(wavelength=wavelength.index(1400))

wavelength = na.ScalarArray(wavelength * u.AA, axes="wavelength")

vmr_electron = _vmr_electron(wavelength, width_pixel)
vmr_photon = _vmr_photon(wavelength, width_pixel)

snr_improvement = _snr_improvement(wavelength, width_pixel)

width_diffusion = _width_diffusion(wavelength)
