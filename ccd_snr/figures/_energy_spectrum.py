import astropy.units as u
import astropy.visualization
import numpy as np
import aastex
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "energy_spectrum",
]


def energy_spectrum() -> aastex.FigureStar:

    num_photons = na.ScalarArray(
        ndarray=([1, 10, 100] * u.photon).astype(int),
        axes="intensity",
    )

    num_experiments = 1000000
    shape_experiments = dict(experiment=num_experiments)

    _wavelength = [
        93 * u.AA,
        977 * u.AA,
        1394 * u.AA,
    ]

    wavelength = na.stack(
        arrays=_wavelength,
        axis="wavelength",
    )
    energy = wavelength.to(u.eV, equivalencies=u.spectral())

    ccd = ccd_snr.ccd()

    rays = optika.rays.RayVectorArray(
        intensity=num_photons,
        wavelength=wavelength,
        direction=na.Cartesian3dVectorArray(0, 0, 1),
    )
    normal = na.Cartesian3dVectorArray(0, 0, -1)

    signal = optika.sensors.signal(
        photons_expected=rays.intensity,
        wavelength=wavelength,
        absorbance=1,
        thickness_implant=ccd.thickness_implant,
        cce_backsurface=ccd.cce_backsurface,
        temperature=ccd.temperature,
        shape_random=shape_experiments,
    )

    dither0 = na.random.uniform(-0.5, 0.5, shape_random=signal.shape)
    dither1 = na.random.uniform(-0.5, 0.5, shape_random=signal.shape)

    dither0 = dither0 * u.electron
    dither1 = dither1 * u.electron

    iqy = ccd.quantum_yield_ideal(wavelength)
    f = ccd.fano_factor(wavelength)
    cce = ccd.charge_collection_efficiency(rays, normal)
    mu = iqy * na.random.poisson(rays.intensity * cce, shape_random=signal.shape)
    signal_stern86 = na.random.normal(
        loc=mu,
        scale=np.sqrt(mu * f * u.photon),
    )
    signal_stern86 = (signal_stern86 + 0.5 * u.electron).astype(int)

    vmin = np.percentile(signal, 00.01, "experiment").astype(int) - 0.5 * u.electron
    vmax = np.percentile(signal, 99.99, "experiment").astype(int) - 0.5 * u.electron

    kwargs_hist = dict(
        bins=dict(bin=201),
        axis="experiment",
        density=True,
        min=vmin,
        max=vmax,
    )

    hist = na.histogram(
        a=signal + dither0,
        **kwargs_hist,
    )
    hist_stern1986 = na.histogram(
        a=signal_stern86 + dither1,
        **kwargs_hist,
    )

    wavelength_str = wavelength.to_string_array("%d").astype(object)
    energy_str = energy.to_string_array("%d").astype(object)
    title = wavelength_str + " (" + energy_str + ")"

    with astropy.visualization.quantity_support():
        fig, ax = na.plt.subplots(
            ncols=signal.shape["wavelength"],
            nrows=signal.shape["intensity"],
            axis_cols="wavelength",
            axis_rows="intensity",
            figsize=(aastex.text_width_inches, aastex.text_width_inches - 2),
            constrained_layout=True,
        )
        na.plt.stairs(
            hist.inputs,
            hist.outputs,
            axis="bin",
            ax=ax,
            label="$N_e''$",
            zorder=10,
        )
        na.plt.stairs(
            hist_stern1986.inputs,
            hist_stern1986.outputs,
            axis="bin",
            ax=ax,
            label="Stern et al. (1986)",
        )

        ax[dict(wavelength=0, intensity=0)].ndarray.legend()
        xlabel = ax.ndarray.flat[0].get_xlabel()
        na.plt.set_xlabel(
            xlabel="",
            ax=ax,
        )
        na.plt.set_xlabel(
            xlabel=f"signal ({xlabel})",
            ax=ax[dict(intensity=0)],
        )
        na.plt.set_ylabel(
            ylabel="probability density",
            ax=ax[dict(wavelength=0)],
        )
        num_photons_str = num_photons.to_string_array(format_value="%d").astype(object)
        na.plt.text(
            x=1.05,
            y=0.5,
            s=r"$\langle$" + num_photons_str + r"$\rangle$",
            ax=ax[dict(wavelength=~0)],
            transform=na.plt.transAxes(ax[dict(wavelength=~0)]),
            ha="left",
            va="center",
        )
        na.plt.text(
            x=0.5,
            y=1.05,
            s=title,
            ax=ax[dict(intensity=~0)],
            transform=na.plt.transAxes(ax[dict(intensity=~0)]),
            ha="center",
            va="bottom",
        )

    result = aastex.FigureStar("energySpectrum")
    result.add_fig(fig, width=None)
    result.add_caption(
        aastex.NoEscape(
            rf"""
The probability distribution of the number of measured electrons for a given
wavelength and expected number of \textit{{absorbed}} photons calculated using
{num_experiments} samples of Equation~\ref{{eq:measuredElectrons}} and the 
\cite{{Stern1986}} noise model."""
        )
    )

    return result
