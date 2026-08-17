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

    wavelength = na.geomspace(1.5, 10000, axis="wavelength", num=101) * u.AA
    energy = wavelength.to(u.eV, equivalencies=u.spectral())

    f = ccd.fano_factor(wavelength)

    iqy = ccd.quantum_yield_ideal(wavelength)

    q = ccd_snr.random.discrete_gamma(
        mean=iqy,
        vmr=f,
        shape_random=shape_xy | dict(photon=int(num_photons.to_value(u.ph))),
    )
    q = q * u.photon
    n = q.sum("photon")

    w = 2 / 12 * (u.electron / u.photon) ** 2
    f2 = f + w * (num_photons - 1 * u.ph) / (num_photons * iqy)

    m = ccd_snr.random.discrete_gamma(
        mean=num_photons * iqy,
        vmr=f2 * u.photon,
        shape_random=shape_xy,
    )

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
        ax.set_ylabel(f"variance-to-mean ratio ({ax.get_ylabel()})")
        ax.legend()

    result = aastex.Figure("fanoNoise", position="thb!")

    # result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(aastex.NoEscape(r"""
The VMR of the number of generated photoelectrons as a function of wavelength
given by a Monte Carlo simulation of Equation~\ref{eq:totalElectrons} (individual photons)
and Equation~\ref{eq:approxTotalElectrons} (ensemble approximation). 
"""))

    return result
