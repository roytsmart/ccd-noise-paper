import aastex
import ccd_snr

__all__ = [
    "tracks",
]


def tracks() -> aastex.Section:
    result = aastex.Section(
        "Measuring the Charge Diffusion Kernel with Particle Tracks",
        label="appendix:tracks",
    )
    result.append(r"""
The charge diffusion model of Section~\ref{subsec:ChargeDiffusion} rests on a
depletion thickness fit to the \MCC\ measurements of \citet{Stern2004},
which were made on a different sensor operated at a different voltage.
Here we measure the charge diffusion of the \IRIS\ \CCDs\ themselves using the
tracks left by energetic particles.

A charged particle crossing the sensor at glancing incidence deposits charge
along a straight line running from the back surface to the front surface.
Each row (or column) of pixels crossed by the track therefore samples the
charge cloud at a different, known depth, and the spread of the charge across
the track in that row measures the width of the charge diffusion kernel at
that depth.
Charge deposited in the field-free region diffuses in the same way regardless
of how it was liberated, so the tracks measure the same kernel that applies to
photoelectrons.

We searched \numTrackFrames\ level-1 frames from the \IRIS\ \FUV\
spectrograph and the \SJI\ for tracks (Table~\ref{table:tracks}),
favoring frames taken while the spacecraft crossed the \SAA, where the flux of
energetic protons is greatest, and frames in which the slit or the field of
view was at least partly off the solar limb, so that the tracks could be found
against a dark background.
For the \SJI\ frames only the off-limb half of the field of view was used.
The background of each frame was estimated as the trimmed mean of the frames
in the same observing sequence and subtracted, and the read noise was
estimated from the median absolute deviation of the residual.
Pixels more than five times the read noise above the background were labeled,
connected groups of labeled pixels were fit with a straight line,
and we kept the groups spanning at least twelve rows (or columns) with a slope
of less than 0.35 pixels per row, so that each track is nearly aligned with the
pixel grid and its cross-section is sampled once per row.
A seven-pixel-wide cutout centered on the fitted line was extracted for each
track, keeping the slices with more than 240 electrons,
which yielded \numTracks\ tracks.

For each track we modeled the charge in every slice as spread uniformly along
the fitted centerline and diffused as a Gaussian with standard deviation
\begin{equation} \label{eq:trackWidth}
    \sigma(t) = \sigma_\text{max} \sqrt{1 - t / t_c}, \quad t < t_c,
\end{equation}
and zero otherwise,
where $t = z / D$ is the fractional depth of the slice below the back surface,
$t_c = z_f / D$ is the fractional thickness of the field-free region,
and $\sigma_\text{max}$ is the width of the charge cloud at the back surface.
This is Equation~\ref{eq:chargeDiffusion} rewritten in terms of the fractional
depth, since we observe the length of the track in slices rather than the
thickness of the sensor in microns.
A track that enters the back surface and exits the front surface spans the
full thickness of the sensor, so the fractional depth of slice $i$ of an
$N$-slice track is $t = (i + 1/2) / N$, up to the orientation of the track,
which we fit along with $t_c$ and $\sigma_\text{max}$ by exhaustive search on
a grid of 21 values in each of $t_c \in [0, 1]$ and
$\sigma_\text{max} \in [0, 10]$ $\mu$m.
At each grid point the offset and tilt of the centerline are adjusted to
minimize a robust misfit, $\sum \ln(1 + r^2 / 2)$, where $r$ is the residual
of the fraction of each slice's charge in each pixel in units of the read
noise.

The useful tracks are those which cross the full thickness of the sensor at
nearly constant energy loss.
We therefore kept only the tracks for which the fit constrains $t_c$ to within
0.15 and improves on a model with no diffusion by at least ten units of misfit,
and for which the median charge per slice in the last third of the track is
within 50\% of that in the first third,
since a rise in the deposited charge along the track (a Bragg peak) indicates
that the particle stopped inside the sensor and did not cross its full
thickness.
We call these the flat tracks;
\numFlatTracks\ tracks pass these cuts, \numFlatTracksSji\ of them on the \SJI\
\CCD.
""")
    result.append(ccd_snr.figures.tracks())
    result.append(ccd_snr.tables.tracks())
    result.append(r"""
Figure~\ref{fig:tracks} shows one of the flat tracks along with the
probability that two electrons deposited in the same slice are collected in
the same column, $\sum_j f_j^2$ where $f_j$ is the fraction of the slice's
charge in column $j$, averaged over the flat tracks on each \CCD\ in bins of
fractional depth.
The bias from the read noise, $\sum_j \epsilon_j^2$ where $\epsilon_j$ is the
read noise in units of the charge in the slice, has been subtracted.
This quantity requires no model of the shape of the kernel,
and its value near the back surface is the one-dimensional analogue of
Equation~\ref{eq:probabilitySamePixel}, the quantity which enters our noise
model through Equation~\ref{eq:diffusedVmr}.
Since the kernel is separable, the probability that two electrons are
collected in the same pixel is the square of the probability that they are
collected in the same column.
Table~\ref{table:tracks} lists the medians of the fitted parameters and the
same-column and same-pixel probabilities for the slices within $D / 10$ of the
back surface, alongside the same-pixel probability predicted by our model
evaluated along the same tracks.

On the \SJI\ \CCD, the sensor on which \citet{Wulser2018} measured the
photon-transfer curves that we compare to in
Section~\ref{sec:ResultsandDiscussion},
the probability that two electrons liberated at the back surface are collected
in the same pixel is $\sjiSamePixel \pm \sjiSamePixelError$,
in agreement with the \sjiSamePixelModel\ predicted by
Equation~\ref{eq:chargeDiffusion} with $z_d = \depletionThickness$.
The FUV2 \CCD\ is indistinguishable from the \SJI\ \CCD,
while the FUV1 \CCD\ appears to spread its charge over fewer pixels.
The depletion thickness depends on the resistivity of the wafer and on the
applied bias, both of which can differ between devices,
but the FUV1 \CCD\ is not the sensor to which we compare our model.

Two features of Figure~\ref{fig:tracks} deserve comment.
First, the shallowest bin averages over depths from the back surface to
$D / 10$, so the comparison in Table~\ref{table:tracks} is between averages
over that bin rather than at the surface itself,
and the model is averaged in the same way.
Second, the fitted $t_c$, with a median of \sjiCriticalDepth\ on the \SJI\
\CCD, is somewhat larger than the \modelCriticalDepth\ of our model,
and beyond $t_c$ the measured same-column probability settles below the value
expected for a track with no diffusion at all (the dashed line in
Figure~\ref{fig:tracks}).
Both indicate that the charge undergoes some additional spreading, of order a
micron, while drifting across the depletion region, which our model neglects.
The ultraviolet photons of interest here are absorbed within a fraction of a
micron of the back surface, where the diffusion is dominated by the field-free
region, and the back-surface probabilities in Table~\ref{table:tracks} are
measured directly rather than extrapolated from the fit,
so this does not affect our results.

The cutouts of every track, the fits, and the list of frames searched are
distributed with the source code of this article, along with the code to
reproduce the fits.
""")
    return result
