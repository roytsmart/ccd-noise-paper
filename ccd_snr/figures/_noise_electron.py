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

    rays = ccd_snr.simulations.rays()
    normal = ccd_snr.simulations.normal

    iqy = ccd.quantum_yield_ideal(wavelength)
    absorbance = ccd.absorbance(rays, normal)
    cce = ccd.charge_collection_efficiency(rays, normal)
    qe = ccd.quantum_efficiency(rays, normal)
    eqe = ccd.quantum_efficiency_effective(rays, normal)

    n0 = ccd.cce_backsurface
    a = optika.chemicals.Chemical("Si").absorption(wavelength)
    W = ccd.thickness_implant
    aW = (a * W).to(u.dimensionless_unscaled).value

    f = ccd.fano_factor(wavelength)

    electrons_measured = ccd_snr.simulations.electrons_measured()

    mean_n = iqy
    var_n = f * mean_n
    mean_p = cce
    var_p = 2 * np.exp(-aW) * np.square((n0 - 1) / aW) * (np.sinh(aW) - aW)
    mean_p2 = np.square(mean_p)
    mean_n2 = np.square(mean_n)
    mean_i = mean_n * mean_p
    var_exp = (var_n * var_p) + (var_n * mean_p2) + (var_p * mean_n2)
    exp_var = mean_n * (mean_p - (var_p + mean_p2)) * u.electron / u.photon
    var_i = var_exp + exp_var

    vmr_shot = 1 / absorbance.average * u.photon * qe
    vmr_fano = cce * f * u.photon
    vmr_recombination = var_i / mean_i * u.photon - vmr_fano
    vmr_total = vmr_shot + vmr_recombination + vmr_fano

    fano_mc = ccd_snr.fano_factor(
        a=electrons_measured,
        axis=ccd_snr.simulations.axis_xy,
    )
    fano_eqe = (1 / eqe) * u.photon * qe + vmr_fano

    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.plot(
        wavelength,
        vmr_shot,
        ax=ax,
        label="shot",
    )
    na.plt.plot(
        wavelength,
        vmr_recombination,
        ax=ax,
        label="partial-charge collection",
    )
    na.plt.plot(
        wavelength,
        vmr_fano,
        ax=ax,
        label="Fano",
    )
    na.plt.plot(
        wavelength,
        vmr_total,
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
