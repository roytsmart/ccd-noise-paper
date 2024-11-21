import astropy.units as u
import named_arrays as na
import optika
import ccd_snr

ccd = ccd_snr.ccd()

num_experiment = 1000000
shape_experiment = dict(experiment=num_experiment)

intensity = na.broadcast_to(100 * u.ph, shape_experiment)
direction = na.Cartesian3dVectorArray(0, 0, 1)
normal = na.Cartesian3dVectorArray(0, 0, -1)


def _fano_electron(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    electrons = ccd.electrons_measured(rays, normal).intensity

    result = ccd_snr.fano_factor(electrons, axis="experiment")

    return result


def _fano_photon(wavelength: na.ScalarArray) -> na.ScalarArray:

    rays = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength,
        direction=direction,
    )

    electrons = ccd.electrons_measured(rays, normal).intensity

    qe = ccd.quantum_efficiency(rays, normal)

    photons = electrons / qe

    result = ccd_snr.fano_factor(photons, axis="experiment")

    return result
