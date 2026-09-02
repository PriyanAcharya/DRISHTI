import pandas as pd


def normalize_series(series: pd.Series) -> pd.Series:
    """
    Normalize a pandas Series to the range 0.0 to 1.0.

    If all values are identical, return zeros.
    """
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(0.0, index=series.index)

    return (series - minimum) / (maximum - minimum)


def calculate_importance_score(
    map_2_5d: pd.DataFrame,
    density_weight: float = 0.5,
    complexity_weight: float = 0.5,
) -> pd.DataFrame:
    """
    Calculate an importance score for each 2.5D grid cell.

    Parameters
    ----------
    map_2_5d : pd.DataFrame
        2.5D LiDAR map.

    density_weight : float
        Weight assigned to point density.

    complexity_weight : float
        Weight assigned to elevation variation.

    Returns
    -------
    pd.DataFrame
        2.5D map with normalized features and importance score.
    """

    required_columns = [
        "grid_x",
        "grid_y",
        "height",
        "point_density",
        "elevation_variation",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in map_2_5d.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    if density_weight < 0 or complexity_weight < 0:
        raise ValueError(
            "Weights must be non-negative."
        )

    total_weight = density_weight + complexity_weight

    if total_weight == 0:
        raise ValueError(
            "At least one weight must be greater than zero."
        )

    result = map_2_5d.copy()

    result["density_score"] = normalize_series(
        result["point_density"]
    )

    result["complexity_score"] = normalize_series(
        result["elevation_variation"]
    )

    result["importance_score"] = (
        density_weight * result["density_score"]
        + complexity_weight * result["complexity_score"]
    ) / total_weight

    return result