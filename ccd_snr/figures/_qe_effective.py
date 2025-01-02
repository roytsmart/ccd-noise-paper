import matplotlib.pyplot as plt
import named_arrays as na
import optika
import aastex
import ccd_snr

__all__ = [
    "qe_effective",
]


def qe_effective() -> aastex.Figure:
    """
    A figure reproducing Figure 12 of Stern (1994).
    """

    result = aastex.FigureStar("eqe", position="htb!")

    ccd = ccd_snr.ccd()
    ccd_aia = ccd_snr.ccd_aia()

    eqe_measured = ccd.quantum_efficiency_measured
    eqe_measured_aia = ccd_aia.quantum_efficiency_measured

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    rays = optika.rays.RayVectorArray(
        wavelength=wavelength,
        direction=na.Cartesian3dVectorArray(0, 0, 1),
    )
    normal = na.Cartesian3dVectorArray(0, 0, -1)

    eqe = ccd.quantum_efficiency_effective(rays, normal)
    eqe_aia = ccd_aia.quantum_efficiency_effective(rays, normal)

    sz_scatter = 10
    fig, ax = plt.subplots(
        figsize=(aastex.text_width_inches, 4),
        constrained_layout=True,
    )
    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.scatter(
        eqe_measured.inputs,
        eqe_measured.outputs,
        ax=ax,
        label="Heymes et al. (2020)",
        s=sz_scatter,
    )
    na.plt.plot(
        wavelength,
        eqe,
        ax=ax,
        label=r"_Heymes et al. (2020) fit",
    )
    na.plt.plot(
        energy,
        eqe,
        ax=ax2,
        linestyle="None",
    )
    na.plt.scatter(
        eqe_measured_aia.inputs,
        eqe_measured_aia.outputs,
        ax=ax,
        label=r"Boerner et al. (2012)",
        s=sz_scatter,
    )
    na.plt.plot(
        wavelength,
        eqe_aia,
        ax=ax,
        label=r"_Boerner et al. (2012) fit",
    )

    ax.set_xscale("log")
    ax2.set_xscale("log")
    ax.set_xlabel(f"wavelength ({wavelength.unit:latex_inline})")
    ax2.set_xlabel(f"energy ({energy.unit:latex_inline})", labelpad=8)
    ax.set_ylabel("effective quantum efficiency")
    ax.legend()

    ax_inset = ax.inset_axes(
        bounds=[0.14, 0.09, 0.3, 0.32],
        xlim=(900, 3000),
        ylim=(0.07, 0.18),
    )
    na.plt.scatter(
        eqe_measured.inputs,
        eqe_measured.outputs,
        ax=ax_inset,
        s=sz_scatter,
    )
    na.plt.plot(
        wavelength,
        eqe,
        ax=ax_inset,
    )
    na.plt.scatter(
        eqe_measured_aia.inputs,
        eqe_measured_aia.outputs,
        ax=ax_inset,
        s=sz_scatter,
    )
    na.plt.plot(
        wavelength,
        eqe_aia,
        ax=ax_inset,
    )
    ax.indicate_inset_zoom(ax_inset, edgecolor="black")

    result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
A comparison of $\text{EQE}(\lambda)$ measured by \citet{Boerner2012} and \citet{Heymes2020},
along with the best-fit models described in Table \ref{table:models} plotted
as lines with the same color as the data.
The inset zooms into the ultraviolet to better visualize the difference between
the measurement and model in this range.
"""
        )
    )

    return result
