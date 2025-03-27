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

    electrons = ccd.signal(rays, normal).intensity

    result = ccd_snr.fano_factor(electrons, axis="experiment")

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

    result = ccd_snr.fano_factor(photons, axis="experiment")

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

    fano = ccd.fano_noise / iqy / absorbance.average * u.photon

    result = 1 / eqe * u.photon + fano

    return result
