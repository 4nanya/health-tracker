# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from loader import load_json_data
from datetime import date
from normalizer import normalize_to_utc
from merger import merge_datasets
from analyzer import calculate_correlations






# testing critical edge case
def test_day_boundary_edge_case():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "2025-12-07 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)
    
def test_day_boundary_edge_case_leap_year():
    # Testing a workout that occurs on a leap day in UTC
    data = [
        {"timestamp": "2000-2-28 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day Feb 29
    assert normalized[0]['utc_datetime'].day == 29
    # But local_date should still be Feb 28
    assert normalized[0]['local_date'] == date(2000, 2, 28)

def test_day_boundary_edge_case_leap_year_2():
    # Testing a workout that occurs on a leap day in UTC
    data = [
        {"timestamp": "2000-2-29 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day Mar 1
    assert normalized[0]['utc_datetime'].day == 1
    # But local_date should still be Feb 29
    assert normalized[0]['local_date'] == date(2000, 2, 29)

def test_day_boundary_edge_case_different_date_format_1():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "December 7 2025 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)
    
def test_day_boundary_edge_case_different_date_format_2():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "Dec 7, 2025 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)

def test_day_boundary_edge_case_different_date_format_3():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "12/7/2025 23:00:00 PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)

def test_day_boundary_edge_case_different_date_format_4():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "12/7/2025 11 PM PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)

def test_day_boundary_edge_case_different_date_format_5():
    # A workout at 11 PM PST on Dec 7
    data = [
        {"timestamp": "12/7/2025 11pm PST", "type": "gym", "calories": 250}
    ]
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # UTC time should be next day (Dec 8)
    assert normalized[0]['utc_datetime'].day == 8
    # But local_date should still be Dec 7 (the day user worked out)
    assert normalized[0]['local_date'] == date(2025, 12, 7)









#testing analyzer
def test_low_sleep():
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': 5.0, 'total_calories': 300, 'workout_count': 1},
        {'date': '2023-10-02', 'sleep_hours': 5.5, 'total_calories': 350, 'workout_count': 1},
        {'date': '2023-10-03', 'sleep_hours': 7.0, 'total_calories': 400, 'workout_count': 1}
    ]
    
    results = calculate_correlations(merged_data)
    
    # Should have 2 low sleep days
    assert results['low_sleep_day_count'] == 2
    # Should average 300 and 350 = 325
    assert results['avg_calories_on_low_sleep_days'] == '325.00 calories'


def test_no_low_sleep():
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': 7.0, 'total_calories': 300, 'workout_count': 1},
        {'date': '2023-10-02', 'sleep_hours': 8.0, 'total_calories': 350, 'workout_count': 1}
    ]
    
    results = calculate_correlations(merged_data)
    
    # Should have 0 low sleep days
    assert results['low_sleep_day_count'] == 0
    assert results['avg_calories_on_low_sleep_days'] == "No days with < 6 hours sleep"

def test_normal_sleep():
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': 5.0, 'total_calories': 300, 'workout_count': 1},
        {'date': '2023-10-02', 'sleep_hours': 5.5, 'total_calories': 350, 'workout_count': 1},
        {'date': '2023-10-03', 'sleep_hours': 7.0, 'total_calories': 400, 'workout_count': 1}
    ]
    
    results = calculate_correlations(merged_data)
    
    # Should have 1 normal sleep day
    assert results['normal_sleep_day_count'] == 1
    # Should just show the one day
    assert results['avg_calories_on_normal_sleep_days'] == '400.00 calories'


def test_no_normal_sleep():
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': 5.0, 'total_calories': 300, 'workout_count': 1},
        {'date': '2023-10-02', 'sleep_hours': 5.0, 'total_calories': 350, 'workout_count': 1}
    ]
    
    results = calculate_correlations(merged_data)
    
    # Should have 0 low sleep days
    assert results['normal_sleep_day_count'] == 0
    assert results['avg_calories_on_normal_sleep_days'] == "No days with >= 6 hours sleep"

def test_incomplete_data():
    # Test that days with missing data are excluded
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': None, 'total_calories': 300, 'workout_count': 1},  # No sleep
        {'date': '2023-10-02', 'sleep_hours': 5.0, 'total_calories': 0, 'workout_count': 0},     # No workout
        {'date': '2023-10-03', 'sleep_hours': 5.5, 'total_calories': 350, 'workout_count': 1}    # Only complete entry
    ]
    results = calculate_correlations(merged_data)
    
    # Should only count Oct 3
    assert results['low_sleep_day_count'] == 1
    assert results['avg_calories_on_low_sleep_days'] == '350.00 calories'


def test_empty_data():
    # Test that days with missing data are excluded
    merged_data = [
        {'date': '2023-10-01', 'sleep_hours': None, 'total_calories': 300, 'workout_count': 1},  # No sleep
        {'date': '2023-10-02', 'sleep_hours': 5.0, 'total_calories': 0, 'workout_count': 0},     # No workout
    ]
    results = calculate_correlations(merged_data)
    
    # Should only count Oct 3
    assert results['low_sleep_day_count'] == 0
    assert results['normal_sleep_day_count'] == 0









#testing merger
def test_merge_multiple_workouts_same_day():
    sleep_data = [
        {'local_date': date(2023, 10, 1), 'hours': 7.5, 'quality': 'good'}
    ]
    
    workout_data = [
        {'local_date': date(2023, 10, 1), 'type': 'run', 'calories': 300, 'duration': 30},
        {'local_date': date(2023, 10, 1), 'type': 'gym', 'calories': 250, 'duration': 45}
    ]
    
    merged = merge_datasets(sleep_data, workout_data)
    
    # Should have 1 day
    assert len(merged) == 1
    # Should sum calories
    assert merged[0]['total_calories'] == 550
    # Should count workouts
    assert merged[0]['workout_count'] == 2
    # Should sum duration
    assert merged[0]['workout_time'] == 75

def test_merge_multiple_workouts_different_days():
    sleep_data = [
        {'local_date': date(2023, 10, 1), 'hours': 7.5, 'quality': 'good'}
    ]
    
    workout_data = [
        {'local_date': date(2023, 10, 2), 'type': 'run', 'calories': 300, 'duration': 30},
        {'local_date': date(2023, 10, 1), 'type': 'gym', 'calories': 250, 'duration': 45}
    ]
    
    merged = merge_datasets(sleep_data, workout_data)
    
    # Should have 2 days
    assert len(merged) == 2
    # Should only show first day
    assert merged[0]['total_calories'] == 250
    assert merged[0]['workout_count'] == 1
    assert merged[0]['workout_time'] == 45
    assert merged[1]['total_calories'] == 300
    assert merged[1]['workout_count'] == 1
    assert merged[1]['workout_time'] == 30

def test_merge_no_sleep():
    sleep_data = []
    workout_data = [
        {'local_date': date(2023, 10, 1), 'type': 'run', 'calories': 300, 'duration': 30}
    ]
    
    merged = merge_datasets(sleep_data, workout_data)
    
    assert len(merged) == 1
    assert merged[0]['date'] == "2023-10-01"
    assert merged[0]['sleep_hours'] is None
    assert merged[0]['total_calories'] == 300

def test_merge_no_workout():
    sleep_data = [
        {'local_date': date(2023, 10, 1), 'hours': 7.5, 'quality': 'good'}
    ]
    workout_data = []
    
    merged = merge_datasets(sleep_data, workout_data)
    
    assert len(merged) == 1
    assert merged[0]['date'] == "2023-10-01"
    assert merged[0]['sleep_hours'] == 7.5
    assert merged[0]['total_calories'] == 0
    assert merged[0]['workout_count'] == 0
    assert merged[0]['workout_time'] == 0

def test_merge_no_data():
    sleep_data = []
    workout_data = []
    
    merged = merge_datasets(sleep_data, workout_data)

    assert len(merged) == 0






#testing normalization
def test_utc_normalization():
    #testing utc --> utc conversion
    data = [{"date": "2023-10-01T06:00:00Z", "hours": 7.5}]
    
    normalized = normalize_to_utc(data, 'UTC')
    # time should stay the same 
    assert normalized[0]['utc_datetime'].hour == 6
    assert normalized[0]['utc_datetime'].day == 1
    assert normalized[0]['local_date'] == date(2023, 10, 1)

def test_pst_normalization():
    #testing pst --> utc conversion
    data = [{"date": "2023-10-01 6pm PST", "hours": 7.5}]
    
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # should be next day at 1am
    assert normalized[0]['utc_datetime'].hour == 1
    assert normalized[0]['utc_datetime'].day == 2
    assert normalized[0]['local_date'] == date(2023, 10, 1)

def test_pst_normalization_daylight_savings():
    #testing pst --> utc conversion
    data = [{"date": "2025-12-07 6pm PST", "hours": 7.5}]
    
    normalized = normalize_to_utc(data, 'America/Los_Angeles')
    # should be next day at 2am bc of daylight savings
    assert normalized[0]['utc_datetime'].hour == 2
    assert normalized[0]['utc_datetime'].day == 8
    assert normalized[0]['local_date'] == date(2025, 12, 7)








#testing loader
def test_load_sleep_data():
    data = load_json_data('data/sleep.json')
    
    # Check that we got a list
    assert isinstance(data, list)
    
    # Check that it's not empty
    assert len(data) > 0
    
    # Check first record has required fields
    assert 'date' in data[0]
    assert 'hours' in data[0]
    assert 'quality' in data[0]

def test_load_workout_data():
    data = load_json_data('data/workouts.json')
    
    # Check that we got a list
    assert isinstance(data, list)
    
    # Check that it's not empty
    assert len(data) > 0
    
    # Check first record has required fields
    assert 'timestamp' in data[0]
    assert 'date' not in data[0]
    assert 'calories' in data[0]
    assert 'duration' in data[0]