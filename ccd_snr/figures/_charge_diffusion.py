import matplotlib.pyplot as plt
import aastex
import astropy.visualization
import named_arrays as na
import optika
import ccd_snr

__all__ = [
    "charge_diffusion",
]


def charge_diffusion() -> aastex.Figure:

    ccd = ccd_snr.ccd()
    # ccd_aia = ccd_snr.ccd_aia()

    measured = optika.sensors.diffusion.mcc_stern2004("thick")

    wavelength_measured = measured.inputs

    mcc_measured = measured.outputs

    wavelength_fit = ccd_snr.wavelength()
    energy_fit = ccd_snr.energy()

    mcc_fit = ccd.diffusion.mean_charge_capture(
        absorption=optika.chemicals.Chemical("Si").absorption(wavelength_fit),
        thickness_substrate=measured.thickness_substrate,
        width_pixel=measured.width_pixel,
    )

    width = ccd.width_charge_diffusion(wavelength_fit)
    # width_aia = ccd_aia.width_charge_diffusion(rays, normal)

    with astropy.visualization.quantity_support():
        fig, ax = plt.subplots(
            nrows=2,
            sharex=True,
            figsize=(aastex.column_width_inches, 3),
            constrained_layout=True,
        )
        ax1, ax2 = ax
        ax1_twin = ax1.twiny()
        ax2_twin = ax2.twiny()
        ax2_twin.sharex(ax1_twin)
        ax1_twin.invert_xaxis()
        ax2_twin.tick_params(labeltop=False)
        na.plt.scatter(
            wavelength_measured,
            mcc_measured,
            ax=ax1,
            label="measured",
            s=10,
        )
        na.plt.plot(
            wavelength_fit,
            mcc_fit,
            ax=ax1,
            label="fit",
        )
        na.plt.plot(
            energy_fit,
            mcc_fit,
            ax=ax1_twin,
            linestyle="None",
        )
        na.plt.plot(
            wavelength_fit,
            width,
            ax=ax2,
        )
        # na.plt.plot(
        #     wavelength_fit,
        #     width_aia,
        #     ax=ax2,
        #     label="Boerner et al. (2012)",
        # )

        ax1.set_xscale("log")
        ax1_twin.set_xscale("log")
        ax2.set_xlabel(f"wavelength ({ax2.get_xlabel()})")
        ax1_twin.set_xlabel(f"energy ({ax1_twin.get_xlabel()})", labelpad=8)
        ax1.set_ylabel("MCC")
        ax2.set_ylabel(f"width ({ax2.get_ylabel()})")
        ax1.legend()

        result = aastex.Figure("chargeDiffusion", position="htb!")
        # result.append(aastex.NoEscape(r"\vspace{5pt}"))
        result.add_fig(fig, width=None)

        result.add_caption(aastex.NoEscape(r"""
The top panel plots the MCC measured by \citet{Stern2004} and the fit
of our model.
The bottom panel shows the corresponding standard deviation of the charge
diffusion kernel for the \citet{Heymes2020} sensor.
    """))

        return result
