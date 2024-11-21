import astropy.units as u
import pylatex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "fano_factor",
]


def fano_factor() -> pylatex.Table:

    wavelength_aia = ccd_snr.instruments.aia.wavelength
    wavelength_iris = ccd_snr.instruments.iris.wavelength
    wavelength_muse = ccd_snr.instruments.muse.wavelength

    fano_electrons_aia = ccd_snr.instruments.aia.fano_electron
    fano_electrons_iris = ccd_snr.instruments.iris.fano_electron
    fano_electrons_muse = ccd_snr.instruments.muse.fano_electron

    fano_photons_aia = ccd_snr.instruments.aia.fano_photon
    fano_photons_iris = ccd_snr.instruments.iris.fano_photon
    fano_photons_muse = ccd_snr.instruments.muse.fano_photon

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
