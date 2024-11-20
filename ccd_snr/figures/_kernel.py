import matplotlib.pyplot as plt
import aastex
import astropy.units as u
import named_arrays as na
import optika
import ccd_snr


def diffusion_kernel() -> aastex.Figure:

    ccd = ccd_snr.ccd()

    wavelength = 1400 * u.AA

    kernel = ccd_snr.diffusion_kernel(
        width_diffusion=ccd.width_charge_diffusion(
            rays=optika.rays.RayVectorArray(
                wavelength=wavelength,
            ),
            normal=na.Cartesian3dVectorArray(0, 0, -1),
        ),
        width_pixel=15 * u.um,
    )

    mappable = plt.cm.ScalarMappable(
        norm=plt.Normalize(0, 1),
        cmap="viridis",
    )

    fig, ax = plt.subplots(
        figsize=(aastex.column_width_inches, aastex.column_width_inches),
        constrained_layout=True,
    )
    na.plt.pcolormesh(
        kernel.inputs.x,
        kernel.inputs.y,
        C=kernel.outputs,
        cmap=mappable.cmap,
        norm=mappable.norm,
    )
    ax.set_xlabel(f"detector $x$ (pix)")
    ax.set_ylabel(f"detector $y$ (pix)")
    fig.colorbar(mappable, ax=ax)

    result = aastex.Figure("chargeDiffusionKernel")
    result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            r"""
The charge diffusion kernel convolved with a pixel.
"""
        )
    )

    return result
