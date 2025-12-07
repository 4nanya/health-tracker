"""
Health Tracker CLI Application

Command-line interface for analyzing personal health data.
Loads sleep and workout data, normalizes timestamps, and provides analysis commands.
"""

import typer
from tabulate import tabulate
from analyzer import calculate_correlations
from loader import load_json_data
from merger import merge_datasets
from normalizer import normalize_to_utc


app = typer.Typer(
    name="healthtracker",
    help="Personal health data aggregator for Palo Alto Networks"
)


def load_and_merge_data(
    sleep_json_file: str,
    workouts_json_file: str,
    local_time_zone: str
) -> list:
    """
    Load, normalize, and merge health data from JSON files.
    
    Args:
        sleep_json_file: Path to sleep data JSON file
        workouts_json_file: Path to workout data JSON file
        local_time_zone: IANA timezone for workout data (e.g., 'America/Los_Angeles')
        
    Returns:
        Merged dataset with daily health metrics
    """
    # Load raw data
    sleep = load_json_data(sleep_json_file)
    workouts = load_json_data(workouts_json_file)
    
    # Normalize timestamps to UTC while preserving local dates
    norm_sleep = normalize_to_utc(sleep, 'UTC')
    norm_workouts = normalize_to_utc(workouts, local_time_zone)
    
    # Merge datasets by local date
    return merge_datasets(norm_sleep, norm_workouts)


@app.command()
def showbyday(
    sleep_json_file: str = typer.Option("sleep.json", help="Path to sleep data JSON file"),
    workouts_json_file: str = typer.Option("workouts.json", help="Path to workouts data JSON file"),
    local_time_zone: str = typer.Option("America/Los_Angeles", help="IANA timezone for workout data"),
):
    """Display merged health data in a day-by-day tabular format."""
    merged = load_and_merge_data(sleep_json_file, workouts_json_file, local_time_zone)
    print(tabulate(merged, headers="firstrow", tablefmt="grid"))


@app.command()
def showSummary(
    sleep_json_file: str = typer.Option("sleep.json", help="Path to sleep data JSON file"),
    workouts_json_file: str = typer.Option("workouts.json", help="Path to workouts data JSON file"),
    local_time_zone: str = typer.Option("America/Los_Angeles", help="IANA timezone for workout data"),
):
    """Display summary statistics and correlations between sleep and activity."""
    merged = load_and_merge_data(sleep_json_file, workouts_json_file, local_time_zone)
    results = calculate_correlations(merged)
    print(results)


if __name__ == '__main__':
    app()