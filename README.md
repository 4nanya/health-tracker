# health-tracker


**Palo Alto Networks Intern Challenge - Option 3** 
---
### For my case study, I chose Option 3: Personal Health Data Aggregator. This project takes 2 distinct datasets whose data doesn't necessarily match. It merges them into 1 dataset on their date -- after making them both UTC. Further analysis of the data can then be done to learn more about how someone sleeps/works out.
---
### Challenge Requirements Met
- [x] **Data Simulation:** I generated 2 json files: workouts.json and sleep.json. They both have different attributes (eg the logged date being under "date" vs "timestamp"), different formatting for the date itself (eg "2023-10-01 14:00:00 PST" vs "2023-10-01T06:00:00Z"), along with their own unique attributes that described the activity (eg "calories" for workouts vs "quality" for sleep)
- [x] **Normalization & Merge:** In normalizer.py, I convert both datasets to UTC by parsing through the date using the dateutil module to easily convert timezones, which fully accounts for things like daylight savings and other edge cases. After I have 2 normalized datasets, I then merge them under the same date. 
- [x] **The Critical Edge Case:** To account for the critical edge case of "day boundary" logic, I just saved the local date from the original dataset, and put this value into a new attribute of the normalized dataset under "date". I use this attribute to correctly merge the 2 datasets by the same day they were done. 
- [x] **Correlation Logic:** In analyzer.py, I use aggregate functions to figure out average calories on high and low sleep days, simply by iterating through the values in the merged dataset.

---
### Methodology & AI Usage Disclosure
### AI Tools Used
I used Claude.ai to help with initial code architecture and understanding timezone edge cases. I also used Claude.ai to generate first the test case but wrote the rest myself.
### How I Validated AI Output
1. **Manual Code Review**: I read through every line of AI-generated code to understand what it does, tweaking as I saw fit to match my vision
2. **Edge Case Testing**: I created test data with the 11 PM workout scenario to verify day boundary logic works correctly
3. **Output Verification**: I initially manually calculated what the expected results were going to be and then I and compared against actual output to ensure that I was on right track
4. **Test Cases**: I then created test cases for various scenarios and uses them to test functionality and the changes
---

### Key Considerations

### Why dateutil for parsing?
The challenge requires handling messy date formats. `dateutil.parser.parse()` automatically detects and parses any date string format without manually specifying patterns. This makes the code resilient to variations to the format. The standard library methods like datetime.strptime() and datetime.fromisoformat() are not able to handle fuzzy or ambiguous parsing.

### Why pytz instead of manual timezone math?
Manual timezone calculations can be really prone to errors which is what I wanted to avoid. This includes things like Daylight saving time transitions depending on what day in the year the workout/sleep fell on and historical timezone changes, and anticipating future potential changes to time-zoning. pytz is really good at simply handling all these edge cases automatically.

---

## Edge Cases Handled

### 1. **Day Boundary Crossing** (Most Critical)
*A user in California logs a workout at 11:00 PM on Tuesday. This is 7:00 AM on Wednesday in UTC. Which day should we attribute this workout to?*

**How I approached this**

I decided to use the local timezone that the user provided as input to classify the date, so in the example above, although it would be logged as 7 AM UTC, it would be classified under Tuesday, as this is more understandable to the user. 
```python
# In normalizer.py
dt_local = tz.localize(dt)  # Keep in original timezone
dt_utc = dt_local.astimezone(pytz.UTC)  # Then convert to UTC
# CRITICAL: USE LOCAL DATE below
local_date = dt_local.date()  # Tuesday (correct!)
# NOT: dt_utc.date()  # Would give Wednesday since dt_utc is local date converted
```

**Test Cases:**
- `test_day_boundary_edge_case()`
- `test_day_boundary_edge_case_leap_year()`
- `test_day_boundary_edge_case_leap_year_2()`
- `test_day_boundary_edge_case_different_date_format_1()`
- `test_day_boundary_edge_case_different_date_format_2()`
- `test_day_boundary_edge_case_different_date_format_3()`
- `test_day_boundary_edge_case_different_date_format_4()`


### 2. **Multiple Workouts Per Day**
Some days have 2+ workouts. The merger correctly:
- Counts all workouts
- Sums total calories
- Sums total duration
I decided to only show the aggregated results on the days with several workouts instead of displaying every workout that occured that day for a cleaner merged dataset.

**Test Cases:**
- `test_merge_multiple_workouts_same_day()` 
- `test_merge_multiple_workouts_different_days()`

### 3. **Missing Data**
The analyzer filters out incomplete days:
- If there are days with sleep but no workout, then this is just excluded from correlation
- Same goes for days with workout but no sleep
- Only analyze days with BOTH data points

**Test Cases:**
- `test_incomplete_data()`
- `test_empty_data()`
- `test_merge_no_sleep()`
- `test_merge_no_workout()`
- `test_merge_no_data()`

### 4. **Different Date Field Names + Format**
Sleep data uses `"date"`, workout data uses `"timestamp"`. Additionally, strings representing the current date can come in all kinds of forms, like "Dec 7 2025", "12/7/2025", "2025-12-07". The normalizer handles both:
```python
if 'date' in record:
    timestamp_str = record['date']
else:
    timestamp_str = record['timestamp']
```
The dateutil parser handles various date formats automatically.

**Test Cases:**
- `test_load_sleep_data()`
- `test_load_workout_data()`
- `test_day_boundary_edge_case_different_date_format_1()`
- `test_day_boundary_edge_case_different_date_format_2()`
- `test_day_boundary_edge_case_different_date_format_3()`
- `test_day_boundary_edge_case_different_date_format_4()`

### 5. **Daylight Saving Time Transitions and other Date Anomalies**
Daylight Savings can make UTC conversions differ throughout the year. For example, 6pm PST on October 1st is 1am UTC, but on Dec 7th is 2am UTC. The pytz library automatically handles DST transitions, ensuring correct UTC conversions year-round. I also tested leap year cases, which pytz also handles automatically.

**Test Cases:**
- `test_pst_normalization()` 
- `test_pst_normalization_daylight_savings()`
- `test_day_boundary_edge_case_leap_year()`
- `test_day_boundary_edge_case_leap_year_2()`
---
## Test Suite
I created a comprehensive test suite with 28 test cases covering every major functionality and edge case I could think of.
### Test Coverage by Module:
**Loader Tests (2 tests):**
- Loading sleep data with correct fields
- Loading workout data with correct fields

**Normalizer Tests (12 tests):**
- UTC to UTC conversion 
- PST to UTC conversion
- PST to UTC with daylight saving time
- Day boundary crossing with standard format
- Day boundary crossing with leap years (2 tests)
- Day boundary crossing with various date formats (5 tests)

**Merger Tests (5 tests):**
- Merging multiple workouts on same day
- Merging workouts on different days
- Handling missing sleep data
- Handling missing workout data
- Handling completely empty datasets

**Analyzer Tests (6 tests):**
- Calculating average calories on low sleep days
- Handling zero low sleep days
- Calculating average calories on normal sleep days
- Handling zero normal sleep days
- Handling incomplete data
- Handling completely empty data


---
## How to Run!

1. In terminal, run `pip3 install -r requirements.txt`
2. If you then type `python3 -m cli --help` you will be able to see the different commands you can run on the command line interface
    - **showbyday**: This returns the whole merged dataset
    - **showsummary**: This command will show you the data analysis done on the merged dataset
3. Running tests: `pytest test_health_tracker.py -v`

---

### What I Learned
I learned how to execute a whole case study in a short amount of time. I also learned details about modules such as ```pythondateutil.parser, pytz``` and how to work with CLI (typer) and testing frameworks in Python (pytest)