from collections import defaultdict

def merge_datasets(sleep_data, workout_data):
    """
    Merge sleep and workout data by local date.
    """
    # Group sleep by date
    sleep_by_date = defaultdict(list)
    for record in sleep_data:
        date_key = record['local_date'].isoformat()
        sleep_by_date[date_key] = record
    
    # Group workouts by date
    workouts_by_date = defaultdict(list)
    for record in workout_data:
        date_key = record['local_date'].isoformat()
        # workouts_by_date[date_key] = workouts_by_date[date_key] + record['duration']

        workouts_by_date[date_key].append(record)
    
    # Get all dates
    all_dates = set(sleep_by_date.keys()).union(set(workouts_by_date.keys())) 
    
    # Merge
    merged = []
    for date_str in sorted(all_dates):
        daily = {'date': date_str}
        
        # Add sleep data; assume one sleep per day
        if date_str in sleep_by_date:
            sleep = sleep_by_date[date_str]
            daily['sleep_hours'] = sleep.get('hours')
            daily['sleep_quality'] = sleep.get('quality')
        else:
            daily['sleep_hours'] = None
            daily['sleep_quality'] = None
        
        # Add workout data
        if date_str in workouts_by_date:
            workouts = workouts_by_date[date_str]
           # Assume multiple workout per day and sum up the calories and the duration.
            daily['total_calories'] = sum(w.get('calories', 0) for w in workouts)
            daily['workout_count'] = len(workouts)
            daily['workout_time'] = sum(w.get('duration', 0) for w in workouts)
        else:
            # daily['workouts'] = []
            daily['total_calories'] = 0
            daily['workout_count'] = 0
            daily['workout_time'] = 0
        
        merged.append(daily)
    
    return merged