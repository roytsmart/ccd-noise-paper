import astropy.units as u
import ccd_snr

__all__ = [
    "vmr_predicted",
]


def vmr_predicted() -> str:

    wavelength_aia = ccd_snr.instruments.aia.wavelength
    wavelength_iris = ccd_snr.instruments.iris.wavelength
    wavelength_muse = ccd_snr.instruments.muse.wavelength
    wavelength_wfc3 = ccd_snr.instruments.wfc3.wavelength

    vmr_electrons_aia = ccd_snr.instruments.aia.vmr_electron
    vmr_electrons_iris = ccd_snr.instruments.iris.vmr_electron
    vmr_electrons_muse = ccd_snr.instruments.muse.vmr_electron
    vmr_electrons_wfc3 = ccd_snr.instruments.wfc3.vmr_electron

    vmr_photons_aia = ccd_snr.instruments.aia.vmr_photon
    vmr_photons_iris = ccd_snr.instruments.iris.vmr_photon
    vmr_photons_muse = ccd_snr.instruments.muse.vmr_photon
    vmr_photons_wfc3 = ccd_snr.instruments.wfc3.vmr_photon

    improvement_aia = ccd_snr.instruments.aia.snr_improvement
    improvement_iris = ccd_snr.instruments.iris.snr_improvement
    improvement_muse = ccd_snr.instruments.muse.snr_improvement
    improvement_wfc3 = ccd_snr.instruments.wfc3.snr_improvement

    diffusion_aia = ccd_snr.instruments.aia.width_diffusion
    diffusion_iris = ccd_snr.instruments.iris.width_diffusion
    diffusion_muse = ccd_snr.instruments.muse.width_diffusion
    diffusion_wfc3 = ccd_snr.instruments.wfc3.width_diffusion

    result = r"""
\begin{deluxetable*}{lrrrrr}
\tablecaption{
\label{table:instrumentVMR}
The VMR predicted by our model (including charge diffusion)
for prominent wavelengths in selected UV observatories,
in both incident photon and measured electron units.
Also included
is the SNR improvement ratio between our model and the traditional noise model
as well as the standard deviation of the charge diffusion kernel. 
}
"""

    result += rf"""\tablehead{{
\colhead{{Instrument}}
& \colhead{{wavelength ({u.AA:latex_inline})}}
& \colhead{{VMR ({vmr_photons_aia.unit:latex_inline})}}
& \colhead{{VMR ({vmr_electrons_aia.unit:latex_inline})}}
& \colhead{{SNR improvement}}
& \colhead{{diffusion width({u.um:latex_inline})}}
}}
"""
    result += "\\startdata\n"

    for i, index in enumerate(vmr_photons_aia.ndindex()):
        if i == 0:
            instrument = r"\AIA"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_aia[index].ndarray.to_value(u.AA):.0f}",
            f"{vmr_photons_aia[index].ndarray.real.to_value(u.ph):.2f}",
            f"{vmr_electrons_aia[index].ndarray.to_value(u.electron):.2f}",
            f"{improvement_aia[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
            f"{diffusion_aia[index].ndarray.to_value(u.um):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

    for i, index in enumerate(vmr_photons_iris.ndindex()):
        if i == 0:
            instrument = r"\IRIS"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_iris[index].ndarray.to_value(u.AA):.0f}",
            f"{vmr_photons_iris[index].ndarray.real.to_value(u.ph):.2f}",
            f"{vmr_electrons_iris[index].ndarray.to_value(u.electron):.2f}",
            f"{improvement_iris[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
            f"{diffusion_iris[index].ndarray.to_value(u.um):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

    for i, index in enumerate(vmr_photons_muse.ndindex()):
        if i == 0:
            instrument = r"MUSE"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_muse[index].ndarray.to_value(u.AA):.0f}",
            f"{vmr_photons_muse[index].ndarray.real.to_value(u.ph):.2f}",
            f"{vmr_electrons_muse[index].ndarray.to_value(u.electron):.2f}",
            f"{improvement_muse[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
            f"{diffusion_muse[index].ndarray.to_value(u.um):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\tableline\n"

    for i, index in enumerate(vmr_photons_wfc3.ndindex()):
        if i == 0:
            instrument = r"WFC3"
        else:
            instrument = ""
        row = [
            instrument,
            f"{wavelength_wfc3[index].ndarray.to_value(u.AA):.0f}",
            f"{vmr_photons_wfc3[index].ndarray.real.to_value(u.ph):.2f}",
            f"{vmr_electrons_wfc3[index].ndarray.to_value(u.electron):.2f}",
            f"{improvement_wfc3[index].ndarray.to_value(u.dimensionless_unscaled):.2f}",
            f"{diffusion_wfc3[index].ndarray.to_value(u.um):.2f}",
        ]
        result += f"{'&'.join(row)} \\\\\n"

    result += "\\enddata\n"
    result += "\\end{deluxetable*}"

    return result
