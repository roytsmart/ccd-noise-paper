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
    num_photons = 100
    num_experiments = 1000

    _wavelength = [
        ((5.89875 + 5.88765) / 2 * u.keV).to(u.AA, equivalencies=u.spectral()),
        93 * u.AA,
        1400 * u.AA,
    ]

    wavelength = na.stack(
        arrays=_wavelength,
        axis="wavelength",
    )
    energy = wavelength.to(u.eV, equivalencies=u.spectral())

    ccd = ccd_snr.ccd()

    rays = optika.rays.RayVectorArray(
        intensity=na.broadcast_to(
            array=num_photons * u.photon,
            shape=dict(experiment=num_experiments)
        ).astype(int),
        wavelength=wavelength,
        direction=na.Cartesian3dVectorArray(0, 0, 1),
    )
    normal = na.Cartesian3dVectorArray(0, 0, -1)

    signal = ccd.electrons_measured(rays, normal).intensity

    shape = signal.shape | dict(photon=num_photons)
    iqy = ccd.quantum_yield_ideal(wavelength)
    thickness_implant = ccd.thickness_implant
    cce_backsurface = ccd.cce_backsurface
    fano_factor = ccd.fano_noise
    si = optika.chemicals.Chemical("Si")
    k = np.imag(si.n(wavelength))
    d = wavelength / (4 * np.pi * k)
    p = na.random.uniform(
        low=0,
        high=1,
        shape_random=shape,
    )
    z = -d * np.log(1 - p)
    q = optika.sensors._materials._materials._discrete_gamma(
        mean=iqy,
        vmr=fano_factor,
        shape_random=shape,
    ) * u.photon
    differential_cce = np.where(
        condition=z < thickness_implant,
        x=cce_backsurface + (1 - cce_backsurface) * z / thickness_implant,
        y=1,
    )
    qy = na.random.binomial(
        n=q.astype(int),
        p=differential_cce.value,
    )
    signal_exact = qy.sum("photon")

    hist = na.histogram(
        a=signal + na.random.uniform(-.5, .5, shape_random=rays.intensity.shape) * u.electron,
        bins=dict(bin=51),
        axis="experiment",
        density=True,
    )
    hist_exact = na.histogram(
        a=signal_exact + na.random.uniform(-.5, .5, shape_random=rays.intensity.shape) * u.electron,
        bins=dict(bin=51),
        axis="experiment",
        density=True,
    )

    wavelength_str = wavelength.to_string_array("%d").astype(object)
    energy_str = energy.to_string_array("%d").astype(object)
    title = wavelength_str + " (" + energy_str + ")"

    with astropy.visualization.quantity_support():
        fig, ax = na.plt.subplots(
            ncols=3,
            axis_cols="wavelength",
            figsize=(aastex.text_width_inches, 2.5),
            constrained_layout=True,
        )
        na.plt.stairs(
            hist_exact.inputs,
            hist_exact.outputs,
            axis="bin",
            ax=ax,
            label="individual\nphotons"
        )
        na.plt.stairs(
            hist.inputs,
            hist.outputs,
            axis="bin",
            ax=ax,
            label="ensemble\napproximation"
        )
        na.plt.set_title(
            label=title,
            ax=ax,
        )
        ax[dict(wavelength=0)].ndarray.legend()
        ax[dict(wavelength=0)].ndarray.set_ylabel("probability density")

    result = aastex.FigureStar("energySpectrum")
    result.add_fig(fig, width=None)
    result.add_caption(
        aastex.NoEscape(
            rf"""
The probability distribution of the number of measured electrons calculated using
a Monte-Carlo simulation of
Equation~\ref{{eq:measuredElectrons}} (individual photons)
and Equation~\ref{{eq:approxMeasuredElectrons}} (ensemble approximation)
with {num_experiments} samples and {num_photons} absorbed photons for each wavelength."""
        )
    )

    return result
