# ccd-noise-paper

[![tests](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/tests.yml/badge.svg)](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/roytsmart/ccd-noise-paper/graph/badge.svg?token=tBcex8q72g)](https://codecov.io/gh/roytsmart/ccd-noise-paper)
[![Black](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/black.yml/badge.svg)](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/black.yml)
[![Ruff](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/ruff.yml/badge.svg)](https://github.com/roytsmart/ccd-noise-paper/actions/workflows/ruff.yml)
[![Documentation Status](https://readthedocs.org/projects/ccd-euv-snr/badge/?version=latest)](https://ccd-euv-snr.readthedocs.io/en/latest/?badge=latest)

**The Noise on Ultraviolet Astronomical Images Captured by Back-illuminated Silicon Sensors**

Roy T. Smart, Charles C. Kankelborg, and Jacob D. Parker  
*Montana State University, Department of Physics*

📄 **[Read the article (pdf)](https://roytsmart.github.io/ccd-noise-paper/ccd-euv-snr.pdf)**

## What this is

Ultraviolet astronomy relies on back-illuminated silicon sensors, and the noise
in those sensors is usually assumed to be dominated by photon shot noise.
Measurements from HST's Wide Field Camera 3 and from IRIS disagree: the noise
measured in the ultraviolet is systematically *lower* than that assumption
predicts.

This article argues that the discrepancy is caused by **partial charge
collection**, in which a fraction of the photogenerated electron-hole pairs
recombine near the back surface before they can be measured. Because the
electrons liberated by a single photon share an absorption depth, they share a
recombination probability, and their losses are therefore correlated rather
than independent. Partial charge collection consequently changes the variance
of the measured signal as well as its mean. We present a model valid from
1 Å to 10000 Å which incorporates this effect and shows better agreement with both instruments,
and which implies that the achievable signal-to-noise ratio in the ultraviolet
is higher than previously understood.

## This repository *is* the article

The repository is not a library that supports a paper. It is the paper. Every
figure, every table, and every numeric value quoted in the prose is computed
from the model at build time, so the text cannot drift away from the physics.
Calling

```python
import ccd_snr
ccd_snr.pdf()
```

runs the model, renders the figures, typesets the LaTeX, and produces
`ccd-euv-snr.pdf`.

Numbers reach the prose as `aastex.Variable` macros rather than as literals. A
sentence in the discussion is written `\modeledIrisRatio`, not `1.19`, and that
macro is defined by the code that computes it. Changing the sensor model
changes the sentence.

## Layout

| path | contents |
|---|---|
| `_document.py` | assembles the article and renders the pdf |
| `sections/` | the prose, as LaTeX strings, one module per section |
| `figures/` | one module per figure, each returning an `aastex.Figure` |
| `tables/` | one module per table |
| `_variables.py` | the `aastex.Variable` macros quoted in the prose |
| `_acronyms.py` | acronym definitions used as `\ACRONYM` macros |
| `_ccd.py` | the sensor model, an `optika` back-illuminated silicon material |
| `instruments/` | per-instrument parameters for AIA, IRIS, MUSE, and WFC3 |
| `simulations.py` | the Monte Carlo pixel-grid simulation |
| `diffusion.py` | the charge-diffusion kernel used by the kernel figure |
| `_vmr.py`, `_wavelength.py` | the Stern variance-to-mean model and the wavelength grid |
| `sources.bib` | the bibliography |
| `sources/` | pdfs of the primary references |

The sensor physics lives in [`optika`](https://github.com/sun-data/optika),
which models absorption, pair creation, partial charge collection, and charge
diffusion. The LaTeX is generated through
[`aastex`](https://github.com/sun-data/aastex), a Python wrapper around the AAS
journal classes.

## Building

Requires Python 3.12 or newer and a LaTeX installation. On Ubuntu:

```bash
sudo apt-get install latexmk texlive-publishers texlive-science cm-super libcairo2-dev
```

`latexmk` is not optional. Without it `pylatex` falls back to a single
`pdflatex` pass, which silently produces an article with no bibliography and
every citation rendered as `(?)`.

```bash
pip install -e .[test]
pytest                       # builds and validates the pdf
python -c "import ccd_snr; ccd_snr.pdf()"
```

A full build takes roughly two minutes locally and ten to fifteen on a CI
runner. Most of that is `matplotlib`'s `usetex` mode, which invokes LaTeX once
per text element in every figure.

Formatting and linting, both enforced in CI:

```bash
black ccd_snr
ruff check
```

## Continuous integration

Every push runs the test suite on Python 3.12, 3.13, and 3.14, which includes
building the article and checking that the reference list is present and that
no citation or cross-reference is left unresolved. Coverage is required to stay
at 100%.

Pushes to `main` publish the article to the link above. Pull requests get their
own rendered preview at `…/pr/<number>/ccd-euv-snr.pdf`, posted as a comment on
the pull request and removed when it closes.

## Status

The model reproduces the WFC3 measurement closely and accounts for most of the
IRIS discrepancy, though it overcorrects there. The remaining disagreement is
localized to the charge-diffusion treatment; see
[issue #15](https://github.com/roytsmart/ccd-noise-paper/issues/15) for the open
questions and what has already been ruled out.
