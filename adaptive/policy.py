import pandas as pd

from adaptive.scoring import calculate_importance_score
from adaptive.resolution import assign_resolution


def apply_adaptive_resolution(
    map_2_5d: pd.DataFrame,
) -> pd.DataFrame:
    """
    Apply the complete adaptive-resolution policy.

    Processing steps:
    1. Calculate importance scores.
    2. Assign resolution levels.
    3. Assign resolution values in meters.

    Returns
    -------
    pd.DataFrame
        2.5D map with adaptive-resolution information.
    """

    scored_map = calculate_importance_score(map_2_5d)

    adaptive_map = assign_resolution(scored_map)

    return adaptive_map