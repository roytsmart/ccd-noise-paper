import numpy as np
import astropy.units as u
import named_arrays as na
import optika
import ccd_snr

ccd = ccd_snr.ccd()

num_experiment = 1000000
num_x = 1000
num_y = 1000
axis_experiment = ("detector_x", "detector_y")
shape_experiment = dict(detector_x=num_x, detector_y=num_y)

intensity = na.broadcast_to(100 * u.ph, shape_experiment)
direction = na.Cartesian3dVectorArray(0, 0, 1)
normal = na.Cartesian3dVectorArray(0, 0, -1)


def _vmr_electron(
    wavelength: na.ScalarArray,
    width_pixel: u.Quantity,
) -> na.ScalarArray:

    result = optika.sensors.vmr_signal(
        wavelength=wavelength,
        absorption=ccd._chemical.absorption(wavelength),
        thickness_implant=ccd.thickness_implant,
        cce_backsurface=ccd.cce_backsurface,
        temperature=ccd.temperature,
    )

    mcc = optika.sensors.mean_charge_capture(
        width_diffusion=_width_diffusion(wavelength),
        width_pixel=width_pixel,
    )

    result = optika.sensors.vmr_diffusion(
        vmr_flat=result,
        mcc=mcc,
    )

    return result


def _vmr_photon(
    wavelength: na.ScalarArray,
    width_pixel: u.Quantity,
) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    qe = ccd.quantum_efficiency(rays, normal)

    vmr_electron = _vmr_electron(wavelength, width_pixel)

    result = vmr_electron / qe

    return result


def _snr_improvement(
    wavelength: na.ScalarArray,
    width_pixel: u.Quantity,
) -> na.ScalarArray:

    vmr_electron = _vmr_electron(wavelength, width_pixel)

    vmr_stern = ccd_snr.vmr_stern(wavelength, ccd.temperature)

    result = np.sqrt(vmr_stern / vmr_electron)

    return result


def _width_diffusion(wavelength: na.ScalarArray) -> na.ScalarArray:
    return ccd.width_charge_diffusion(
        rays=optika.rays.RayVectorArray(
            wavelength=wavelength,
        ),
        normal=na.Cartesian3dVectorArray(0, 0, -1),
    )
