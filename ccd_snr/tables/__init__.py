"""
The tables used in this article.
"""

from ._ccd_models import ccd_models
from ._vmr_predicted import vmr_predicted
from ._vmr_measured import vmr_measured
from ._tracks import num_frames, tracks

__all__ = [
    "ccd_models",
    "vmr_predicted",
    "vmr_measured",
    "num_frames",
    "tracks",
]
