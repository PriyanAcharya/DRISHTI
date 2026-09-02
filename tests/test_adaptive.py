import pandas as pd
from adaptive.resolution import assign_resolution
from adaptive.policy import apply_adaptive_resolution
from adaptive.scoring import (
    normalize_series,
    calculate_importance_score,
)


def test_normalize_series():
    series = pd.Series([10, 20, 30])

    result = normalize_series(series)

    assert result.iloc[0] == 0.0
    assert result.iloc[1] == 0.5
    assert result.iloc[2] == 1.0


def test_calculate_importance_score():
    map_2_5d = pd.DataFrame({
        "grid_x": [0, 1, 2],
        "grid_y": [0, 1, 2],
        "height": [1.0, 2.0, 3.0],
        "point_density": [2, 5, 10],
        "elevation_variation": [0.1, 0.5, 1.0],
    })

    result = calculate_importance_score(map_2_5d)

    assert "density_score" in result.columns
    assert "complexity_score" in result.columns
    assert "importance_score" in result.columns

    assert result["importance_score"].min() >= 0.0
    assert result["importance_score"].max() <= 1.0

    assert (
        result.iloc[0]["importance_score"]
        < result.iloc[1]["importance_score"]
        < result.iloc[2]["importance_score"]
    )
def test_assign_resolution():
    map_with_scores = pd.DataFrame({
        "grid_x": [0, 1, 2],
        "grid_y": [0, 1, 2],
        "height": [1.0, 2.0, 3.0],
        "point_density": [2, 5, 10],
        "elevation_variation": [0.1, 0.5, 1.0],
        "importance_score": [0.2, 0.5, 0.8],
    })

    result = assign_resolution(map_with_scores)

    assert list(result["resolution_level"].astype(str)) == [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    assert list(result["resolution_m"]) == [
        1.0,
        0.5,
        0.2,
    ]
def test_apply_adaptive_resolution():
    map_2_5d = pd.DataFrame({
        "grid_x": [0, 1, 2],
        "grid_y": [0, 1, 2],
        "height": [1.0, 2.0, 3.0],
        "point_density": [2, 5, 10],
        "elevation_variation": [0.1, 0.5, 1.0],
    })

    result = apply_adaptive_resolution(map_2_5d)

    assert "importance_score" in result.columns
    assert "resolution_level" in result.columns
    assert "resolution_m" in result.columns

    assert list(result["resolution_level"].astype(str)) == [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    assert list(result["resolution_m"]) == [
        1.0,
        0.5,
        0.2,
    ]
def test_calculate_importance_score_with_custom_weights():
    map_2_5d = pd.DataFrame({
        "grid_x": [0, 1],
        "grid_y": [0, 1],
        "height": [1.0, 2.0],
        "point_density": [2, 10],
        "elevation_variation": [0.1, 1.0],
    })

    result = calculate_importance_score(
        map_2_5d,
        density_weight=0.8,
        complexity_weight=0.2,
    )

    assert result["importance_score"].min() >= 0.0
    assert result["importance_score"].max() <= 1.0

    assert result.iloc[0]["importance_score"] == 0.0
    assert result.iloc[1]["importance_score"] == 1.0
def test_calculate_importance_score_missing_column():
    map_2_5d = pd.DataFrame({
        "grid_x": [0, 1],
        "grid_y": [0, 1],
        "height": [1.0, 2.0],
        "point_density": [2, 10],
    })

    try:
        calculate_importance_score(map_2_5d)
        assert False
    except ValueError as error:
        assert "elevation_variation" in str(error)


def test_calculate_importance_score_zero_weights():
    map_2_5d = pd.DataFrame({
        "grid_x": [0],
        "grid_y": [0],
        "height": [1.0],
        "point_density": [2],
        "elevation_variation": [0.1],
    })

    try:
        calculate_importance_score(
            map_2_5d,
            density_weight=0.0,
            complexity_weight=0.0,
        )
        assert False
    except ValueError as error:
        assert "weight" in str(error).lower()