"""Matplotlib chart functions for CityBike analytics."""

from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D


FIGURES_DIR = Path("output") / "figures"
COLOR_PALETTE = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
]

plt.style.use("seaborn-v0_8-whitegrid")


def _ensure_dir(output_dir: Path) -> Path:
    directory = Path(output_dir) if output_dir else FIGURES_DIR
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_figure(fig: plt.Figure, filename: str, output_dir: Path = FIGURES_DIR) -> str:
    """Save figure to the output directory and close it."""

    directory = _ensure_dir(output_dir)
    filepath = directory / filename
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return str(filepath)


def plot_trips_per_station(
    trips_df: pd.DataFrame,
    stations_df: Optional[pd.DataFrame] = None,
    output_dir: Path = FIGURES_DIR,
    top_n: int = 10,
) -> Optional[str]:
    """Create a bar chart showing the busiest start stations."""

    if trips_df is None or trips_df.empty or "start_station_id" not in trips_df:
        return None

    counts = (
        trips_df["start_station_id"]
        .value_counts()
        .head(top_n)
        .rename_axis("station_id")
        .reset_index(name="trip_count")
    )

    if stations_df is not None and not stations_df.empty and "station_id" in stations_df:
        name_map = stations_df.set_index("station_id")["station_name"]
        counts["station_name"] = counts["station_id"].map(name_map).fillna(counts["station_id"])
    else:
        counts["station_name"] = counts["station_id"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(counts["station_name"], counts["trip_count"], color=COLOR_PALETTE[0], label="Trips")
    ax.set_title("Top Start Stations by Trip Volume")
    ax.set_xlabel("Station")
    ax.set_ylabel("Trips (count)")
    ax.legend()
    ax.tick_params(axis="x", rotation=45, ha="right")
    fig.tight_layout()
    return save_figure(fig, "bar_trips_per_station.png", output_dir)


def plot_monthly_trip_trend(
    trips_df: pd.DataFrame,
    output_dir: Path = FIGURES_DIR,
) -> Optional[str]:
    """Create a line chart showing the monthly trip volume trend."""

    if trips_df is None or trips_df.empty or "start_time" not in trips_df:
        return None

    trend = (
        trips_df.assign(year_month=trips_df["start_time"].dt.to_period("M"))
        .groupby("year_month")
        .size()
        .reset_index(name="trip_count")
        .sort_values("year_month")
    )

    if trend.empty:
        return None

    trend["year_month"] = trend["year_month"].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        trend["year_month"],
        trend["trip_count"],
        marker="o",
        color=COLOR_PALETTE[1],
        label="Trips per Month",
    )
    ax.set_title("Monthly Trip Volume Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Trips (count)")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    return save_figure(fig, "line_monthly_trip_trend.png", output_dir)


def plot_trip_duration_histogram(
    trips_df: pd.DataFrame,
    output_dir: Path = FIGURES_DIR,
    bins: int = 30,
) -> Optional[str]:
    """Create a histogram for trip duration distribution."""

    if trips_df is None or trips_df.empty or "duration_minutes" not in trips_df:
        return None

    values = trips_df["duration_minutes"].dropna()
    if values.empty:
        return None

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(values, bins=bins, color=COLOR_PALETTE[2], alpha=0.85, label="Trip Duration")
    ax.set_title("Trip Duration Distribution")
    ax.set_xlabel("Duration (minutes)")
    ax.set_ylabel("Trips (count)")
    ax.legend()
    fig.tight_layout()
    return save_figure(fig, "hist_trip_duration.png", output_dir)


def plot_duration_boxplot_by_user_type(
    trips_df: pd.DataFrame,
    output_dir: Path = FIGURES_DIR,
) -> Optional[str]:
    """Create a box plot comparing trip durations across user types."""

    required = {"duration_minutes", "user_type"}
    if trips_df is None or trips_df.empty or not required.issubset(trips_df.columns):
        return None

    groups: List[pd.Series] = []
    labels: List[str] = []
    for user_type, subset in trips_df.groupby("user_type"):
        series = subset["duration_minutes"].dropna()
        if series.empty:
            continue
        groups.append(series)
        labels.append(str(user_type).title())

    if not groups:
        return None

    fig, ax = plt.subplots(figsize=(9, 5))
    box = ax.boxplot(groups, labels=labels, patch_artist=True)

    colors = COLOR_PALETTE * ((len(labels) // len(COLOR_PALETTE)) + 1)
    for patch, color in zip(box["boxes"], colors):
        patch.set(facecolor=color, alpha=0.6)

    handles = [Line2D([0], [0], color=color, lw=4) for color in colors[: len(labels)]]
    ax.legend(handles, labels, title="User Type", loc="upper right")
    ax.set_title("Trip Duration by User Type")
    ax.set_xlabel("User Type")
    ax.set_ylabel("Duration (minutes)")
    fig.tight_layout()
    return save_figure(fig, "box_trip_duration_by_user_type.png", output_dir)


def plot_benchmark_comparison(
    benchmark_results: Dict[str, float],
    output_dir: Path = FIGURES_DIR,
) -> Optional[str]:
    """Plot a bar chart comparing algorithm runtimes in seconds."""

    if not benchmark_results:
        return None

    labels = list(benchmark_results.keys())
    times = [benchmark_results[label] for label in labels]
    colors = COLOR_PALETTE * ((len(labels) // len(COLOR_PALETTE)) + 1)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(labels, times, color=colors[: len(labels)])
    ax.set_title("Algorithm Performance Comparison")
    ax.set_xlabel("Algorithm")
    ax.set_ylabel("Average Time (seconds)")
    ax.set_ylim(0, max(times) * 1.15)

    for bar, value in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.4f}s",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    fig.tight_layout()
    return save_figure(fig, "bar_algorithm_benchmark.png", output_dir)


# Backward-compatible helpers ----------------------------------------------------
def plot_usage_trends(trips_df, output_dir: Path = FIGURES_DIR):
    """Alias for the monthly trip trend line chart."""

    return plot_monthly_trip_trend(trips_df, output_dir=output_dir)


def plot_station_popularity(trips_df, stations_df, output_dir: Path = FIGURES_DIR):
    """Alias for the trips per station bar chart."""

    return plot_trips_per_station(trips_df, stations_df, output_dir=output_dir)


def plot_trip_distribution(trips_df, output_dir: Path = FIGURES_DIR):
    """Alias for the trip duration histogram."""

    return plot_trip_duration_histogram(trips_df, output_dir=output_dir)


def plot_heatmap(trips_df, output_dir: Path = FIGURES_DIR):
    """Alias for the user-type duration box plot (legacy name)."""

    return plot_duration_boxplot_by_user_type(trips_df, output_dir=output_dir)
