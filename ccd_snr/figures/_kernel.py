import matplotlib.pyplot as plt
import aastex
import astropy.units as u
import named_arrays as na
import optika
import ccd_snr


def diffusion_kernel() -> aastex.Figure:

    ccd = ccd_snr.ccd()

    wavelength = 1400 * u.AA

    width_pixel = 15 * u.um

    kernel = ccd_snr.diffusion_kernel(
        width_diffusion=ccd.width_charge_diffusion(
            rays=optika.rays.RayVectorArray(
                wavelength=wavelength,
            ),
            normal=na.Cartesian3dVectorArray(0, 0, -1),
        ),
        width_pixel=width_pixel,
    )

    mappable = plt.cm.ScalarMappable(
        norm=plt.Normalize(0, 1),
        cmap="viridis",
    )

    fig, ax = plt.subplots(
        figsize=(2, 2),
        constrained_layout=True,
    )
    na.plt.pcolormesh(
        kernel.inputs.x,
        kernel.inputs.y,
        C=kernel.outputs,
        cmap=mappable.cmap,
        norm=mappable.norm,
        facecolors="None",
        edgecolors="black",
    )
    na.plt.text(
        x=kernel.inputs.x,
        y=kernel.inputs.y,
        s=kernel.outputs.to_string_array(),
        color="black",
        ha="center",
        va="center",
    )
    ax.set_xlabel("detector $x$ (pix)")
    ax.set_ylabel("detector $y$ (pix)")
    ax.set_aspect("equal")
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    # fig.colorbar(mappable, ax=ax)

    result = aastex.Figure("chargeDiffusionKernel")
    result.append(aastex.NoEscape(r"\centering"))
    # result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            rf"""
The charge diffusion kernel at {wavelength:latex_inline} convolved with a 
{width_pixel:latex_inline} pixel.
"""
        )
    )

    return result
