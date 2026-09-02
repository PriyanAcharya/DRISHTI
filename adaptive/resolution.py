import pandas as pd


def assign_resolution(
    map_with_scores: pd.DataFrame,
) -> pd.DataFrame:
    """
    Assign an adaptive resolution level to each grid cell.

    Resolution is selected from the cell's importance score.

    Importance < 0.3:
        LOW resolution, 1.0 m

    Importance 0.3 to < 0.7:
        MEDIUM resolution, 0.5 m

    Importance >= 0.7:
        HIGH resolution, 0.2 m
    """

    if "importance_score" not in map_with_scores.columns:
        raise ValueError(
            "importance_score column is required."
        )

    result = map_with_scores.copy()

    result["resolution_level"] = pd.cut(
        result["importance_score"],
        bins=[-float("inf"), 0.3, 0.7, float("inf")],
        labels=["LOW", "MEDIUM", "HIGH"],
        right=False,
    )

    result["resolution_m"] = result["resolution_level"].map({
        "LOW": 1.0,
        "MEDIUM": 0.5,
        "HIGH": 0.2,
    })

    return result