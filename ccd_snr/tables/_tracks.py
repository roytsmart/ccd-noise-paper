import astropy.units as u
import ccd_snr

__all__ = [
    "num_frames",
    "tracks",
]

_chips = ["FUV1", "FUV2", "SJI"]


def num_frames(chip: str) -> tuple[int, int]:
    """The number of frames searched for tracks on the given CCD, and the number inside the SAA."""
    image = "FUV" if chip.startswith("FUV") else "SJI"
    frames = [f for f in ccd_snr.tracks.frames() if f["image"].startswith(image)]
    return len(frames), sum(f["saa"] == "1" for f in frames)


def tracks() -> str:

    result = r"""\begin{deluxetable*}{lrrrrccccc}
\tablecaption{
\label{table:tracks}
The charge diffusion measured from glancing particle tracks on the three
\IRIS\ \CCDs.
The number of frames is the number of level-1 images searched, with the
number taken inside the \SAA\ in parentheses.
The flat tracks are those which constrain $t_c$ to within 0.15 and show no
Bragg rise along their length.
$t_c$ and $\sigma_\text{max}$ are the medians of the per-track fits, with the
interquartile range in brackets.
$p$ is the probability that two electrons deposited within
$D / 10$ of the back surface are collected in the same column,
$\mathcal{P} = p^2$ is the corresponding probability that they are collected
in the same pixel, and the last column is $\mathcal{P}$ predicted by the
model used in this work for the same tracks.
}
\tablehead{
\colhead{\CCD}
& \colhead{frames}
& \colhead{tracks}
& \colhead{flat}
& \colhead{$t_c$}
& \colhead{$\sigma_\text{max}$ ($\mu$m)}
& \colhead{$p$}
& \colhead{$\mathcal{P}$}
& \colhead{$\mathcal{P}_\text{model}$}
}
\startdata
"""

    for chip in _chips:
        s = ccd_snr.tracks.summary(chip)
        n_frames, n_saa = num_frames(chip)
        tc = s.critical_depth
        sm = s.width_max.to_value(u.um)
        row = [
            chip,
            f"{n_frames} ({n_saa})",
            f"{s.num_tracks}",
            f"{s.num_flat}",
            f"{tc[1]:.2f} [{tc[0]:.2f}, {tc[2]:.2f}]",
            f"{sm[1]:.1f} [{sm[0]:.1f}, {sm[2]:.1f}]",
            f"${s.same_pixel_1d:.3f} \\pm {s.same_pixel_1d_error:.3f}$",
            f"${s.same_pixel:.3f} \\pm {s.same_pixel_error:.3f}$",
            f"{s.same_pixel_paper:.3f}",
        ]
        result += f"{' & '.join(row)} \\\\\n"

    result += "\\enddata\n"
    result += "\\end{deluxetable*}"

    return result
