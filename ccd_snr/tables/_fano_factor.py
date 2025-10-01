import numpy as np
import astropy.units as u
import ccd_snr

__all__ = [
    "fano_factor",
]


def fano_factor() -> str:

    wavelength_aia = ccd_snr.instruments.aia.wavelength
    wavelength_iris = ccd_snr.instruments.iris.wavelength
    wavelength_muse = ccd_snr.instruments.muse.wavelength
    wavelength_wfc3 = ccd_snr.instruments.wfc3.wavelength

    fano_electrons_aia = ccd_snr.instruments.aia.fano_electron
    fano_electrons_iris = ccd_snr.instruments.iris.fano_electron
    fano_electrons_muse = ccd_snr.instruments.muse.fano_electron
    fano_electrons_wfc3 = ccd_snr.instruments.wfc3.fano_electron

    fano_photons_aia = ccd_snr.instruments.aia.fano_photon
    fano_photons_iris = ccd_snr.instruments.iris.fano_photon
    fano_photons_muse = ccd_snr.instruments.muse.fano_photon
    fano_photons_wfc3 = ccd_snr.instruments.wfc3.fano_photon

    fano_photons_aia_naive = ccd_snr.instruments.aia.fano_photon_naive
    fano_photons_iris_naive = ccd_snr.instruments.iris.fano_photon_naive
    fano_photons_muse_naive = ccd_snr.instruments.muse.fano_photon_naive
    fano_photons_wfc3_naive = ccd_snr.instruments.wfc3.fano_photon_naive

    improvement_aia = np.sqrt(fano_photons_aia_naive / fano_photons_aia)
    improvement_iris = np.sqrt(fano_photons_iris_naive / fano_photons_iris)
    improvement_muse = np.sqrt(fano_photons_muse_naive / fano_photons_muse)
    improvement_wfc3 = np.sqrt(fano_photons_wfc3_naive / fano_photons_wfc3)

    result = r"""\begin{deluxetable}{lrrrr}
\tablecaption{
\label{table:instrumentVMR}
The ratio of the variance to the mean predicted by our model for prominent
wavelengths in selected solar observatories 
in both incident photon and measured electron units.
In the right column,
we've also included the ratio between the \citet{Stern1986} noise model
and our noise model to demonstrate the improvement in VMR predicted by our model. 
}
"""

    result += rf"""\tablehead{{
\colhead{{Instrument}}
& \colhead{{$\lambda$ ({u.AA:latex_inline})}}
& \colhead{{VMR ({fano_photons_aia.unit:latex_inline})}}
& \colhead{{VMR ({fano_electrons_aia.unit:latex_inline})}}
& \colhead{{improvement}}
}}
"""
    result += "\\startdata\n"

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
            f"{improvement_aia[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

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
            f"{improvement_iris[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

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
            f"{improvement_muse[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

    for i, index in enumerate(fano_photons_wfc3.ndindex()):
        if i == 0:
            instrument = r"WFC3"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_wfc3[index].ndarray.to_value(u.AA):.0f}",
            f"{fano_photons_wfc3[index].ndarray.real.to_value(u.ph):.2f}",
            f"{fano_electrons_wfc3[index].ndarray.to_value(u.electron):.2f}",
            f"{improvement_wfc3[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\enddata\n"
    result += "\\end{deluxetable}"

    return result
