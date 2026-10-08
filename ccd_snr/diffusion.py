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

    return ccd.diffusion.kernel_average(
        absorption=optika.chemicals.Chemical("Si").absorption(wavelength),
        thickness_substrate=ccd.thickness_substrate,
        width_pixel=width_pixel,
        axis_x=ccd_snr.simulations.axis_x,
        axis_y=ccd_snr.simulations.axis_y,
        num=3,
    )
