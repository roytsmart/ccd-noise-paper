import matplotlib.axes
import astropy.units as u
import named_arrays as na
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

    rays = ccd_snr.simulations.rays()
    normal = ccd_snr.simulations.normal

    iqy = ccd.quantum_yield_ideal(wavelength)
    absorbance = ccd.absorbance(rays, normal)
    cce = ccd.charge_collection_efficiency(rays, normal)
    qe = ccd.quantum_efficiency(rays, normal)
    eqe = ccd.quantum_efficiency_effective(rays, normal)

    photons_measured = ccd_snr.simulations.photons_measured()

    vsr_shot = 1 / absorbance.average * u.photon
    vsr_recombination = (1 - cce) * u.electron / qe
    f = ccd.fano_noise
    f_a = f + (1 / 6) / iqy.value * iqy.unit
    vsr_fano = f / iqy / absorbance.average * u.photon
    vsr_fano_a = f_a / iqy / absorbance.average * u.photon
    fano_total = vsr_shot + vsr_recombination + vsr_fano_a
    # fano_total = ((iqy.value + f_a - 1) * cce + 1) * u.electron / qe
    fano_mc = ccd_snr.fano_factor(
        a=photons_measured,
        axis=ccd_snr.simulations.axis_xy,
    )
    fano_eqe = (1 / eqe) * u.photon + vsr_fano

    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.plot(
        wavelength,
        vsr_shot,
        ax=ax,
        label="shot",
    )
    na.plt.plot(
        wavelength,
        vsr_recombination,
        ax=ax,
        label="recombination",
    )
    na.plt.plot(
        wavelength,
        vsr_fano_a,
        ax=ax,
        label="Fano",
    )
    na.plt.plot(
        wavelength,
        fano_total,
        ax=ax,
        label="total",
        color="black",
        zorder=5,
    )
    na.plt.plot(
        wavelength,
        fano_mc,
        ax=ax,
        label=r"Monte Carlo",
        zorder=0,
    )
    na.plt.plot(
        wavelength,
        fano_eqe,
        ax=ax,
        label="Stern et al. (1986)",
        color="gray",
    )
    na.plt.plot(
        energy,
        vsr_shot,
        ax=ax2,
        linestyle="None",
    )

    ax.set_xscale("log")
    ax2.set_xscale("log")
    ax2.set_xlabel(f"energy ({energy.unit:latex_inline})", labelpad=8)
    ax.set_ylabel(f"variance-to-signal ratio ({fano_total.unit:latex_inline})")

    ax.text(
        x=0.01,
        y=0.96,
        s="(a)",
        transform=ax.transAxes,
        ha="left",
        va="top",
    )
