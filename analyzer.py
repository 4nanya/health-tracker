def calculate_correlations(merged_data):
    """
    Calculate the main metric for the challenge:
    Average calories burned on days where sleep < 6 hours
    """
    results = {}
    
    # Filter days with complete data
    complete_days = []
    for day in merged_data:
        if day['sleep_hours'] is not None and day['total_calories'] > 0:
            complete_days.append(day)
    
    # Days with low sleep (< 6 hours)
    low_sleep_days = []
    for day in complete_days:
        if day['sleep_hours'] < 6.0:
            low_sleep_days.append(day)
    
    
    if low_sleep_days:
        avg_calories = sum(d['total_calories'] for d in low_sleep_days) / len(low_sleep_days)
        results['avg_calories_on_low_sleep_days'] = f"{avg_calories:.2f} calories"
        results['low_sleep_day_count'] = len(low_sleep_days)
    else:
        results['avg_calories_on_low_sleep_days'] = "No days with < 6 hours sleep"
        results['low_sleep_day_count'] = 0
    
    # Days with normal sleep (>= 6 hours) for comparison
    normal_sleep_days = [
        day for day in complete_days 
        if day['sleep_hours'] >= 6.0
    ]
    
    if normal_sleep_days:
        avg_calories = sum(d['total_calories'] for d in normal_sleep_days) / len(normal_sleep_days)
        results['avg_calories_on_normal_sleep_days'] = f"{avg_calories:.2f} calories"
        results['normal_sleep_day_count'] = len(normal_sleep_days)
    else:
        results['avg_calories_on_normal_sleep_days'] = "No days with >= 6 hours sleep"
        results['normal_sleep_day_count'] = 0
    
    return results