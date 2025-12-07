from tabulate import tabulate
from analyzer import calculate_correlations
from loader import load_json_data
from merger import merge_datasets
from normalizer import normalize_to_utc
import typer


app = typer.Typer (
    name="healthtracker",
    help="personal health data aggregator for palo alto networks"

)
sleep = load_json_data('sleep.json')
workouts = load_json_data('workouts.json')

norm_sleep = normalize_to_utc(sleep, 'UTC')
norm_workouts = normalize_to_utc(workouts, 'America/Los_Angeles')

merged = merge_datasets(norm_sleep, norm_workouts)



@app.command()
def showbyday(
):
    print(tabulate(merged, headers="firstrow", tablefmt="grid"))

@app.command()
def showSummary(
):
    results = calculate_correlations(merged)
    print(results)

if __name__ == '__main__':
    app()