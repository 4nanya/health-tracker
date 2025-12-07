"""
Health Tracker CLI Application

Command-line interface for analyzing personal health data.
Loads sleep and workout data, normalizes timestamps, and provides analysis commands.
"""

import typer
from typing import Annotated
from tabulate import tabulate
from analyzer import calculate_correlations
from loader import load_json_data
from merger import merge_datasets
from normalizer import normalize_to_utc

# Initialize CLI app
app = typer.Typer(
    name="healthtracker",
    help="Personal health data aggregator for Palo Alto Networks"
)

# Shared parameter definitions to reduce duplication
SleepFile = Annotated[str, typer.Option(help="Path to sleep data JSON file")]
WorkoutsFile = Annotated[str, typer.Option(help="Path to workouts data JSON file")]
LocalTimeZone = Annotated[str, typer.Option(help="IANA timezone for workout data")]


def load_and_merge_data(
    sleep_json_file: str,
    workouts_json_file: str,
    local_time_zone: str
) -> list:
    """
    Load, normalize, and merge health data from JSON files.
    """
    sleep = load_json_data(sleep_json_file)
    workouts = load_json_data(workouts_json_file)
    
    norm_sleep = normalize_to_utc(sleep, 'UTC')
    norm_workouts = normalize_to_utc(workouts, local_time_zone)
    
    return merge_datasets(norm_sleep, norm_workouts)


@app.command()
def showbyday(
    sleep_json_file: SleepFile = "data/sleep.json",
    workouts_json_file: WorkoutsFile = "data/workouts.json",
    local_time_zone: LocalTimeZone = "America/Los_Angeles",
):
    """Display merged health data in a day-by-day tabular format."""
    merged = load_and_merge_data(sleep_json_file, workouts_json_file, local_time_zone)
    print(tabulate(merged, headers="keys", tablefmt="grid"))


@app.command()
def showSummary(
    sleep_json_file: SleepFile = "data/sleep.json",
    workouts_json_file: WorkoutsFile = "data/workouts.json",
    local_time_zone: LocalTimeZone = "America/Los_Angeles",
):
    """Display summary statistics and correlations between sleep and activity."""
    merged = load_and_merge_data(sleep_json_file, workouts_json_file, local_time_zone)
    results = calculate_correlations(merged)
    table_data = list(results.items())
    print(tabulate(table_data, headers=["Metric", "Value"], tablefmt="grid"))


if __name__ == '__main__':
    app()