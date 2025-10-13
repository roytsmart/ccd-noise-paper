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


def _fano_electron(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    electrons = ccd.signal(rays, normal).intensity

    result = ccd_snr.fano_factor(electrons, axis=axis_experiment)

    return result


def _fano_electron_naive(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    qe = ccd.quantum_efficiency(rays, normal)

    eqe = ccd.quantum_efficiency_effective(rays, normal)

    result = 1 / eqe * u.photon * qe

    return result


def _fano_photon(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    electrons = ccd.signal(rays, normal).intensity

    qe = ccd.quantum_efficiency(rays, normal)

    photons = electrons / qe

    result = ccd_snr.fano_factor(photons, axis=axis_experiment)

    return result


def _fano_photon_naive(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    iqy = ccd.quantum_yield_ideal(rays.wavelength)

    absorbance = ccd.absorbance(rays, normal)

    eqe = ccd.quantum_efficiency_effective(rays, normal)

    fano = ccd.fano_factor(rays.wavelength) / iqy / absorbance.average * u.photon

    result = 1 / eqe * u.photon + fano

    return result


def _width_diffusion(wavelength: na.ScalarArray) -> na.ScalarArray:
   return ccd.width_charge_diffusion(
        rays=optika.rays.RayVectorArray(
            wavelength=wavelength,
        ),
        normal=na.Cartesian3dVectorArray(0, 0, -1),
    )
