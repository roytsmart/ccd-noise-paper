"""
Refit the diffusion model to every track and rewrite ``data/iris_fits.csv``.

Run with ``python -m ccd_snr.tracks``.
"""

import ccd_snr.tracks

if __name__ == "__main__":
    ccd_snr.tracks.save(ccd_snr.tracks.fit_all(ccd_snr.tracks.load()))
