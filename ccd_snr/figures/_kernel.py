import matplotlib.pyplot as plt
import aastex
import named_arrays as na
import ccd_snr


def diffusion_kernel() -> aastex.Figure:

    kernel = ccd_snr.diffusion.kernel()

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
            r"""
The charge diffusion kernel at \diffusionWavelength\ convolved with a 
\diffusionPixelSize\ IRIS pixel and integrated over the extent of each
pixel.
"""
        )
    )

    return result
