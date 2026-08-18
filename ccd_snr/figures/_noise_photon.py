import matplotlib.axes
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "noise_photon",
]


def noise_photon(
    ax: matplotlib.axes.Axes,
) -> None:

    ccd = ccd_snr.ccd()

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    qe = ccd.quantum_efficiency(wavelength)

    kwargs_vmr = dict(
        wavelength=wavelength,
        thickness_implant=ccd.thickness_implant,
        cce_backsurface=ccd.cce_backsurface,
        temperature=ccd.temperature,
        diffusion=False,
    )
    vmr_shot = optika.sensors.vmr_signal(fano=False, pcc=False, **kwargs_vmr) / qe
    vmr_fano = optika.sensors.vmr_signal(shot=False, pcc=False, **kwargs_vmr) / qe
    vmr_pcc = optika.sensors.vmr_signal(shot=False, fano=False, **kwargs_vmr) / qe
    vmr_total = optika.sensors.vmr_signal(**kwargs_vmr) / qe

    kwargs_diffusion = kwargs_vmr | dict(
        thickness_depletion=ccd.depletion.thickness,
        thickness_substrate=ccd.thickness_substrate,
        width_pixel=ccd_snr.instruments.iris.width_pixel,
        diffusion=True,
    )
    vmr_iris = optika.sensors.vmr_signal(**kwargs_diffusion) / qe

    vmr_stern = ccd_snr.vmr_stern(
        wavelength=wavelength,
        temperature=ccd.temperature,
    )
    vmr_stern = vmr_stern / qe

    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.plot(
        wavelength,
        vmr_shot,
        ax=ax,
        label=r"$F_{\gamma,\mathrm{shot}}$",
    )
    na.plt.plot(
        wavelength,
        vmr_pcc,
        ax=ax,
        label=r"$F_{e,\mathrm{PCC}}'' / \mathrm{QE}$",
    )
    na.plt.plot(
        wavelength,
        vmr_fano,
        ax=ax,
        label=r"$F_{e,\mathrm{Fano}}'' / \mathrm{QE}$",
    )
    na.plt.plot(
        wavelength,
        vmr_total,
        ax=ax,
        label=r"$F(N_e'') / \mathrm{QE}$",
        color="black",
        zorder=5,
    )
    na.plt.plot(
        wavelength,
        vmr_stern,
        ax=ax,
        label=r"$F_{e,\mathrm{Stern}}'' / \mathrm{QE}$",
        color="black",
        linestyle="dashed",
    )
    na.plt.plot(
        wavelength,
        vmr_iris,
        ax=ax,
        label=r"$F_{e,\mathrm{blurred}}'' / \mathrm{QE}$",
        color="gray",
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
    ax2.set_xlabel(f"energy ({energy.unit:latex_inline})", labelpad=8)
    ax.set_ylabel(f"variance-to-mean ratio ({vmr_total.unit:latex_inline})")
    ax.legend()
    ax.text(
        x=0.01,
        y=0.96,
        s="(a)",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )
