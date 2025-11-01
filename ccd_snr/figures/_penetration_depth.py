import pathlib
import matplotlib.pyplot as plt
import astropy.units as u
import astropy.visualization
import aastex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "penetration_depth",
]


def penetration_depth() -> pathlib.Path:

    ccd = ccd_snr.ccd()

    wavelength = ccd_snr.wavelength()

    energy = ccd_snr.energy()

    depth = 1 / optika.chemicals.Chemical("Si").absorption(wavelength)

    depth = depth.to(u.nm)

    with astropy.visualization.quantity_support():
        fig, ax = plt.subplots(
            figsize=(aastex.column_width_inches, 3),
            constrained_layout=True,
        )
        ax2 = ax.twiny()
        ax2.invert_xaxis()
        na.plt.plot(wavelength, depth, ax=ax, color="tab:blue")
        na.plt.plot(energy, depth, ax=ax2, color="tab:blue")
        ax.axhline(ccd.thickness_implant, linestyle="--", color="black")
        ax.text(
            x=0.1,
            y=ccd.thickness_implant / 10,
            s="PCC region",
            transform=ax.get_yaxis_transform(),
        )
        ax.set_xscale("log")
        ax2.set_xscale("log")
        ax.set_yscale("log")
        ax2.set_yscale("log")
        ax.set_xlabel(f"wavelength ({ax.get_xlabel()})");
        ax2.set_xlabel(f"energy ({ax2.get_xlabel()})", labelpad=16)
        ax.set_ylabel(f"penetration depth ({depth.unit:latex_inline})")

    result = aastex.Figure("penetrationDepth")
    result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
The penetration depth in silicon as a function of wavelength plotted against
the depth of the PCC region.
"""
        )
    )

    return result
