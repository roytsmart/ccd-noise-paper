import numpy as np
import astropy.units as u
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "kernel",
]


def kernel(
    wavelength: u.Quantity | na.AbstractScalar,
    width_pixel: u.Quantity | na.AbstractScalar,
):

    ccd = ccd_snr.ccd()

    return optika.sensors.kernel_diffusion(
        width_diffusion=ccd.width_charge_diffusion(
            rays=optika.rays.RayVectorArray(
                wavelength=wavelength,
            ),
            normal=na.Cartesian3dVectorArray(0, 0, -1),
        ),
        width_pixel=width_pixel,
        axis_x=ccd_snr.simulations.axis_x,
        axis_y=ccd_snr.simulations.axis_y,
    )
