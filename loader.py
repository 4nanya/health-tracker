import json

def load_json_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

# def load_sleep_data(filepath):
#     return load_json_data(filepath)

# def load_workout_data(filepath):
#     return load_json_data(filepath)