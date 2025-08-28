import matplotlib.pyplot as plt
import aastex
import named_arrays as na
import ccd_snr


def diffusion_kernel() -> aastex.Figure:

    wavelength = ccd_snr.instruments.iris.wavelength
    wavelength = wavelength[ccd_snr.instruments.iris.index_1400].ndarray

    width_pixel = ccd_snr.instruments.iris.width_pixel

    kernel = ccd_snr.diffusion.kernel(
        wavelength=wavelength,
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

    result = aastex.Figure("chargeDiffusionKernel", position="htb!")
    result.append(aastex.NoEscape(r"\centering"))
    # result.append(aastex.NoEscape(r"\vspace{5pt}"))
    result.add_fig(fig, width=None)

    result.add_caption(
        aastex.NoEscape(
            f"""
The charge diffusion kernel at {wavelength:latex_inline} convolved with a 
{width_pixel:latex_inline} IRIS pixel and integrated over the extent of each
pixel.
"""
        )
    )

    return result
