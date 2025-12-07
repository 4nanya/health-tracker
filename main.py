from analyzer import calculate_correlations
from loader import load_json_data
from merger import merge_datasets
from normalizer import normalize_to_utc
from tabulate import tabulate
from cli import app
# sleep = load_json_data('sleep.json')
# workouts = load_json_data('workouts.json')

# norm_sleep = normalize_to_utc(sleep, 'UTC')
# norm_workouts = normalize_to_utc(workouts, 'America/Los_Angeles')

# merged = merge_datasets(norm_sleep, norm_workouts)
# results = calculate_correlations(merged)

# print(tabulate(merged, headers="firstrow", tablefmt="grid"))

# #print(merged)
# print(results)

if __name__ == "__main__":
    app()