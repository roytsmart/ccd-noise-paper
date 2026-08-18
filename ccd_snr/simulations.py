import functools
import astropy.units as u
import named_arrays as na
import ccd_snr

__all__ = [
    "axis_x",
    "axis_y",
    "axis_xy",
    "num_x",
    "num_y",
    "shape",
    "photons_expected",
    "electrons_measured",
]

axis_x = "detector_x"
"""The logical axis representing the horizontal dimension of the sensor."""

axis_y = "detector_y"
"""The logical axis representing the vertical dimension of the sensor."""

axis_xy = (axis_x, axis_y)
"""The logical axes representing the horizontal and vertical dimensions of the sensor."""

num_x = 128
"""The number of pixels in the horizontal dimension."""

num_y = 128
"""The number of pixels in the vertical dimension."""

shape = {axis_x: num_x, axis_y: num_y}
"""The shape of the pixel grid."""

photons_expected = 100 * u.photon
"""The expected number of photons measured by each pixel in the sensor."""


@functools.cache
def electrons_measured() -> na.ScalarArray:
    """
    The number of electrons measured by each pixel in the simulation.
    """
    ccd = ccd_snr.ccd()

    return ccd.signal(
        photons=na.broadcast_to(photons_expected, shape),
        wavelength=ccd_snr.wavelength(),
        width_pixel=ccd_snr.instruments.iris.width_pixel,
        axis_xy=axis_xy,
        wrap=True,
    )
