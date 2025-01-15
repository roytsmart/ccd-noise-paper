import matplotlib.pyplot as plt
import astropy.units as u
import named_arrays as na
import aastex
import ccd_snr

__all__ = [
    "noise_electron",
]


def noise_electron() -> aastex.FigureStar:

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

    electrons_measured = ccd_snr.simulations.electrons_measured()

    vsr_shot = 1 / absorbance.average * u.photon * qe
    vsr_recombination = (1 - cce) * u.electron
    f = ccd.fano_noise
    f_a = f + (1 / 6) / iqy.value * iqy.unit
    vsr_fano = f / iqy / absorbance.average * u.photon * qe
    vsr_fano_a = f_a / iqy / absorbance.average * u.photon * qe
    vsr_total = vsr_shot + vsr_recombination + vsr_fano_a

    fano_mc = ccd_snr.fano_factor(
        a=electrons_measured,
        axis=ccd_snr.simulations.axis_xy,
    )
    fano_eqe = (1 / eqe) * u.photon * qe + vsr_fano

    fig, ax = plt.subplots(
        figsize=(aastex.text_width_inches, 3.5),
        constrained_layout=True,
    )
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
        vsr_total,
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
    ax.set_yscale("log")
    ax2.set_yscale("log")
    ax.set_xlabel(f"wavelength ({wavelength.unit:latex_inline})")
    ax2.set_xlabel(f"energy ({energy.unit:latex_inline})", labelpad=8)
    ax.set_ylabel(f"variance-to-signal ratio ({vsr_total.unit:latex_inline})")

    result = aastex.FigureStar("electronNoise")
    result.add_fig(fig, width=None)
    result.add_caption(
        aastex.NoEscape(
            r"""
The total and component-wise VSR for electrons measured by the sensor.
This plot is useful when calibrating an instrument since it demonstrates the
noise to expect from the sensor for a given number of electrons measured.
Plotted for comparison (gray) is the VSR of the \citet{Stern1986} noise
model.
Line colors have the same meaning as Figure \ref{fig:photonNoise}.
"""
        )
    )

    return result
