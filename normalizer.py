from datetime import datetime
import pytz
from dateutil import parser

def normalize_to_utc(data, source_tz):
    """
    Convert all timestamps to UTC and store the local date.
    
    This is THE CRITICAL function for the challenge.
    """
    # Get the timezone object
    if source_tz == 'UTC':
        tz = pytz.UTC
    else:
        tz = pytz.timezone(source_tz)
    
    normalized = []
    
    for record in data:
        new_record = record.copy()
        
        # Get the timestamp (could be 'date' or 'timestamp')
        if 'date' in record:
            timestamp_str = record['date']
        else:
            timestamp_str = record['timestamp']
        
        # Parse the timestamp string
        dt = parser.parse(timestamp_str)
        # print(timestamp_str)
        
        # Make it timezone-aware
       
        if dt.tzinfo is None:
            dt_local = tz.localize(dt) # 21
        
        else:
            dt_local = dt.astimezone(tz) # 18
        
        # Convert to UTC
        dt_utc = dt_local.astimezone(pytz.UTC)
        print(dt_utc, timestamp_str)

        # THE KEY PART: Store the LOCAL date
        local_date = dt_local.date()
        
        # Add these to the record
        new_record['utc_datetime'] = dt_utc
        new_record['local_date'] = local_date
        
        normalized.append(new_record)
    
    return normalized