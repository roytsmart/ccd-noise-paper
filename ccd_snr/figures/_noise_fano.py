import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.visualization
import named_arrays as na
import aastex
import ccd_snr

__all__ = [
    "noise_fano",
]


def noise_fano() -> aastex.Figure:
    """
    A figure plotting the effective Fano factor
    """

    ccd = ccd_snr.ccd()

    num_photons = 10 * u.photon

    axis_xy = ccd_snr.simulations.axis_xy
    shape_xy = ccd_snr.simulations.shape

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    f = ccd.fano_noise

    iqy = ccd.quantum_yield_ideal(wavelength)

    q = na.random.poisson(
        lam=iqy / f,
        shape_random=shape_xy | dict(photon=int(num_photons.to_value(u.ph))),
    ) * f * u.photon

    q_frac, q_int = np.modf(q.value)
    q2 = (q_int + na.random.binomial(1, q_frac)) << q.unit

    n = q2.sum("photon")

    w = 2 / 12 * (u.electron / u.photon) ** 2
    f2 = f + w * (num_photons - 1 * u.ph) / (num_photons * iqy)

    m = na.random.poisson(
        lam=num_photons * iqy / f2,
        shape_random=shape_xy,
    ) * f2
    m_frac, m_int = np.modf(m.value)
    m = (m_int + na.random.binomial(1, m_frac)) << m.unit

    f_eff = ccd_snr.fano_factor(n, axis=axis_xy)
    f2_eff = ccd_snr.fano_factor(m, axis=axis_xy)

    with astropy.visualization.quantity_support():
        fig, ax = plt.subplots(
            figsize=(aastex.column_width_inches, 2.5),
            constrained_layout=True,
        )
        ax2 = ax.twiny()
        ax2.invert_xaxis()
        na.plt.plot(
            wavelength,
            f_eff,
            ax=ax,
            label="individual photons",
        )
        na.plt.plot(
            wavelength,
            f2_eff,
            ax=ax,
            label="ensemble approximation",
        )
        na.plt.plot(
            energy,
            f2_eff,
            ax=ax2,
            linestyle="None",
        )
        ax.set_xscale("log")
        ax2.set_xscale("log")
        ax.set_xlabel(f"wavelength ({ax.get_xlabel()})")
        ax2.set_xlabel(f"energy ({ax2.get_xlabel()})", labelpad=8)
        ax.set_ylabel(f"variance-to-signal ratio ({ax.get_ylabel()})")
        ax.legend()

    result = aastex.Figure("fanoNoise", position="thb!")

    # result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
The VSR of the number of generated photoelectrons as a function of wavelength
given by a Monte Carlo simulation of Equation~\ref{eq:totalElectrons} (individual photons)
and Equation~\ref{eq:approxTotalElectrons} (ensemble approximation). 
"""
        )
    )

    return result
