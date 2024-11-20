import astropy.units as u
import pylatex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "fano_factor",
]


def fano_factor() -> pylatex.Table:

    ccd = ccd_snr.ccd()

    num_experiment = 1000000
    shape_experiment = dict(experiment=num_experiment)

    wavelength_aia = [
        94,
        131,
        171,
        193,
        211,
        304,
        335,
        1600,
        1700,
    ] * u.AA
    wavelength_aia = na.ScalarArray(wavelength_aia, axes="wavelength")

    wavelength_iris = [
        1330,
        1400,
        2796,
        2832,
    ] * u.AA
    wavelength_iris = na.ScalarArray(wavelength_iris, axes="wavelength")

    wavelength_muse = [
        108,
        171,
        284,
    ] * u.AA
    wavelength_muse = na.ScalarArray(wavelength_muse, axes="wavelength")

    intensity = na.broadcast_to(100 * u.ph, shape_experiment)
    direction = na.Cartesian3dVectorArray(0, 0, 1)
    normal = na.Cartesian3dVectorArray(0, 0, -1)

    rays_aia = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength_aia,
        direction=direction,
    )
    rays_iris = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength_iris,
        direction=direction,
    )
    rays_muse = optika.rays.RayVectorArray(
        intensity=intensity,
        wavelength=wavelength_muse,
        direction=direction,
    )

    electrons_aia = ccd.electrons_measured(rays_aia, normal).intensity
    electrons_iris = ccd.electrons_measured(rays_iris, normal).intensity
    electrons_muse = ccd.electrons_measured(rays_muse, normal).intensity

    qe_aia = ccd.quantum_efficiency(rays_aia, normal)
    qe_iris = ccd.quantum_efficiency(rays_iris, normal)
    qe_muse = ccd.quantum_efficiency(rays_muse, normal)

    photons_aia = electrons_aia / qe_aia
    photons_iris = electrons_iris / qe_iris
    photons_muse = electrons_muse / qe_muse

    fano_electrons_aia = ccd_snr.fano_factor(electrons_aia, axis="experiment")
    fano_electrons_iris = ccd_snr.fano_factor(electrons_iris, axis="experiment")
    fano_electrons_muse = ccd_snr.fano_factor(electrons_muse, axis="experiment")

    fano_photons_aia = ccd_snr.fano_factor(photons_aia, axis="experiment")
    fano_photons_iris = ccd_snr.fano_factor(photons_iris, axis="experiment")
    fano_photons_muse = ccd_snr.fano_factor(photons_muse, axis="experiment")

    result = pylatex.Table()
    result.escape = False

    caption = pylatex.NoEscape(
        r"""
The ratio of the variance to the mean predicted by our model for prominent
wavelengths in selected solar observatories 
in both incident photon and measured electron units."""
    )
    result.add_caption(caption)
    result.append(pylatex.Label("table:instrumentVSR"))

    with result.create(pylatex.Tabular("lr|rr")) as tabular:
        tabular.escape = False
        row = [
            "Instrument",
            f"$\lambda$ ({u.AA:latex_inline})",
            f"VSR ({fano_photons_aia.unit:latex_inline})",
            f"VSR ({fano_electrons_aia.unit:latex_inline})",
        ]
        tabular.add_row(row)
        tabular.add_hline()
        tabular.add_hline()
        for i, index in enumerate(fano_photons_aia.ndindex()):
            if i == 0:
                instrument = r"\AIA"
            else:
                instrument = ""
            row = [
                instrument,
                f"{wavelength_aia[index].ndarray.to_value(u.AA):.0f}",
                f"{fano_photons_aia[index].ndarray.real.to_value(u.ph):.2f}",
                f"{fano_electrons_aia[index].ndarray.to_value(u.electron):.2f}",
            ]
            tabular.add_row(row)

        tabular.add_hline()

        for i, index in enumerate(fano_photons_iris.ndindex()):
            if i == 0:
                instrument = r"\IRIS"
            else:
                instrument = ""
            row = [
                instrument,
                f"{wavelength_iris[index].ndarray.to_value(u.AA):.0f}",
                f"{fano_photons_iris[index].ndarray.real.to_value(u.ph):.2f}",
                f"{fano_electrons_iris[index].ndarray.to_value(u.electron):.2f}",
            ]
            tabular.add_row(row)

        tabular.add_hline()

        for i, index in enumerate(fano_photons_muse.ndindex()):
            if i == 0:
                instrument = r"MUSE"
            else:
                instrument = ""
            row = [
                instrument,
                f"{wavelength_muse[index].ndarray.to_value(u.AA):.0f}",
                f"{fano_photons_muse[index].ndarray.real.to_value(u.ph):.2f}",
                f"{fano_electrons_muse[index].ndarray.to_value(u.electron):.2f}",
            ]
            tabular.add_row(row)

    return result
