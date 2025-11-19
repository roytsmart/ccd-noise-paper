import numpy as np
import matplotlib.axes
import astropy.units as u
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "noise_electron",
]


def noise_electron(
    ax: matplotlib.axes.Axes,
) -> None:

    ccd = ccd_snr.ccd()

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    kwargs_vmr = dict(
        wavelength=wavelength,
        absorption=ccd._chemical.absorption(wavelength),
        thickness_implant=ccd.thickness_implant,
        cce_backsurface=ccd.cce_backsurface,
        temperature=ccd.temperature,
    )
    vmr_shot = optika.sensors.vmr_signal(fano=False, pcc=False, **kwargs_vmr)
    vmr_fano = optika.sensors.vmr_signal(shot=False, pcc=False, **kwargs_vmr)
    vmr_pcc = optika.sensors.vmr_signal(shot=False, fano=False, **kwargs_vmr)
    vmr_total = optika.sensors.vmr_signal(**kwargs_vmr)

    width_diffusion = optika.sensors.charge_diffusion(
        absorption=ccd._chemical.absorption(wavelength),
        thickness_substrate=ccd.thickness_substrate,
        thickness_depletion=ccd.depletion.thickness,
    )

    mcc_iris = optika.sensors.mean_charge_capture(
        width_diffusion=width_diffusion,
        width_pixel=ccd_snr.instruments.iris.width_pixel,
    )

    vmr_iris = optika.sensors.vmr_diffusion(
        vmr_flat=vmr_total,
        mcc=mcc_iris,
    )

    electrons_measured = ccd_snr.simulations.electrons_measured()

    vmr_mc = electrons_measured.vmr(ccd_snr.simulations.axis_xy)

    vmr_stern = ccd_snr.vmr_stern(
        wavelength=wavelength,
        temperature=ccd.temperature,
    )

    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.plot(
        wavelength,
        vmr_shot,
        ax=ax,
        label=r"$F_{e,\mathrm{shot}}''$",
    )
    na.plt.plot(
        wavelength,
        vmr_pcc,
        ax=ax,
        label=r"$F_{e,\mathrm{PCC}}''$",
    )
    na.plt.plot(
        wavelength,
        vmr_fano,
        ax=ax,
        label=r"$F_{e,\mathrm{Fano}}''$",
    )
    na.plt.plot(
        wavelength,
        vmr_total,
        ax=ax,
        label="$F(N_e'')$",
        color="black",
        zorder=5,
    )
    na.plt.plot(
        wavelength,
        vmr_stern,
        ax=ax,
        label=r"$F_{e,\mathrm{Stern}}''$",
        color="black",
        linestyle="dashed",
    )
    na.plt.plot(
        wavelength,
        vmr_iris,
        ax=ax,
        label=r"$F_{e,\mathrm{blurred}}''$",
        color="gray",
    )
    na.plt.plot(
        wavelength,
        vmr_mc,
        ax=ax,
        label=r"Monte Carlo",
        zorder=0,
    )
    na.plt.plot(
        energy,
        vmr_shot,
        ax=ax2,
        linestyle="None",
    )

    ax.set_xscale("log")
    ax2.set_xscale("log")
    ax.set_yscale("log")
    ax2.set_yscale("log")
    ax.set_xlabel(f"wavelength ({wavelength.unit:latex_inline})")
    ax2.set_xticklabels([])
    ax.set_ylabel(f"variance-to-mean ratio ({vmr_total.unit:latex_inline})")
    ax.legend(loc="upper right")
    ax.set_ylim(bottom=0.01)

    ax.text(
        x=0.01,
        y=0.98,
        s="(b)",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )
