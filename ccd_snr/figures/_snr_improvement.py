import pathlib
import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.visualization
import aastex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "snr_improvement",
]


def snr_improvement() -> pathlib.Path:

    ccd = ccd_snr.ccd()

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    vmr_total = optika.sensors.vmr_signal(
        wavelength=wavelength,
        absorption=ccd._chemical.absorption(wavelength),
        thickness_implant=ccd.thickness_implant,
        cce_backsurface=ccd.cce_backsurface,
        temperature=ccd.temperature,
    )

    width_diffusion = optika.sensors.charge_diffusion(
        absorption=ccd._chemical.absorption(wavelength),
        thickness_substrate=ccd.thickness_substrate,
        thickness_depletion=ccd.depletion.thickness,
    )
    vmr_iris = optika.sensors.vmr_diffusion(
        vmr_flat=vmr_total,
        mcc=optika.sensors.mean_charge_capture(
            width_diffusion=width_diffusion,
            width_pixel=ccd_snr.instruments.iris.width_pixel,
        ),
    )
    vmr_wfc3 = optika.sensors.vmr_diffusion(
        vmr_flat=vmr_total,
        mcc=optika.sensors.mean_charge_capture(
            width_diffusion=width_diffusion,
            width_pixel=ccd_snr.instruments.wfc3.width_pixel,
        ),
    )

    vmr_stern = ccd_snr.vmr_stern(
        wavelength=wavelength,
        temperature=ccd.temperature,
    )

    ratio_total = np.sqrt(vmr_stern / vmr_total)
    ratio_iris = np.sqrt(vmr_stern / vmr_iris)
    ratio_wfc3 = np.sqrt(vmr_stern / vmr_wfc3)

    with astropy.visualization.quantity_support():
        fig, ax = plt.subplots(
            figsize=(aastex.column_width_inches, 3),
            constrained_layout=True,
        )
        ax2 = ax.twiny()
        ax2.invert_xaxis()
        na.plt.plot(
            wavelength,
            ratio_total,
            ax=ax,
            label="undiffused"
            # label=r"$\sqrt{F(N_e'') / F_{e,\mathrm{Stern}}''}$"
        )
        na.plt.plot(
            wavelength,
            ratio_iris,
            ax=ax,
            label="IRIS",
            # label=r"$\sqrt{F_{e,\mathrm{IRIS}}'' / F_{e,\mathrm{Stern}}''}$"
        )
        na.plt.plot(
            wavelength,
            ratio_wfc3,
            ax=ax,
            label="WFC3",
            # label=r"$\sqrt{F_{e,\mathrm{WFC3}}'' / F_{e,\mathrm{Stern}}''}$"
        )
        na.plt.plot(energy, ratio_total, ax=ax2, color="none")
        ax.set_xscale("log")
        ax2.set_xscale("log")
        ax.set_xlabel(f"wavelength ({ax.get_xlabel()})")
        ax2.set_xlabel(f"energy ({ax2.get_xlabel()})", labelpad=16)
        ax.set_ylabel("SNR improvement")
        ax.legend()

    result = aastex.Figure("SnrImprovement")
    result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
The SNR improvement predicted by our noise model
compared to the \citet{Stern1986} model.
In blue we have plotted the SNR improvement ignoring charge diffusion.
In orange and green we have plotted the SNR improvement,
including charge diffusion,
for a flat-field image observed by IRIS and WFC3.
"""
        )
    )

    return result
