import matplotlib.pyplot as plt
import named_arrays as na
import optika
import aastex
import ccd_snr

__all__ = [
    "absorbance_and_cce",
]


def absorbance_and_cce() -> aastex.Figure:

    wavelength = ccd_snr.wavelength()
    energy = ccd_snr.energy()

    ccd = ccd_snr.ccd()

    rays = optika.rays.RayVectorArray(
        wavelength=wavelength,
        direction=na.Cartesian3dVectorArray(0, 0, 1),
    )
    normal = na.Cartesian3dVectorArray(0, 0, -1)

    absorbance = ccd.absorbance(rays, normal).average
    cce = ccd.charge_collection_efficiency(rays, normal)

    fig, ax = plt.subplots(
        figsize=(aastex.column_width_inches, 2.5),
        constrained_layout=True,
    )
    ax2 = ax.twiny()
    ax2.invert_xaxis()
    na.plt.plot(
        wavelength,
        absorbance,
        ax=ax,
        label=r"$A(\lambda)$",
        zorder=10,
    )
    na.plt.plot(
        wavelength,
        cce,
        ax=ax,
        label=r"$\mathrm{CCE}(\lambda)$",
    )
    na.plt.plot(
        energy,
        cce,
        ax=ax2,
        linestyle="None",
    )
    ax.set_xscale("log")
    ax2.set_xscale("log")
    ax.set_xlabel(f"wavelength ({wavelength.unit:latex_inline})")
    ax2.set_xlabel(f"energy ({energy.unit:latex_inline})", labelpad=8)
    ax.set_ylabel("efficiency")
    ax.legend()

    result = aastex.Figure("absorbanceAndCCE")
    result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
The fraction of incident light absorbed by the light-sensitive silicon layer 
and the \CCE\ as a function of wavelength for the \citet{Heymes2020} model.
"""
        )
    )

    return result
