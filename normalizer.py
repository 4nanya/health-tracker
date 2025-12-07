from datetime import datetime
import pytz
from dateutil import parser


def normalize_to_utc(data, source_tz):
    """
    Convert all timestamps to UTC and store the local date.
    
    This is THE CRITICAL function for the challenge. It ensures that
    health events are associated with the correct calendar day in the
    user's local timezone, while also storing UTC time for consistency.
    
    Args:
        data (list): List of health records (sleep or workout data)
        source_tz (str): IANA timezone name (e.g., 'UTC', 'America/Los_Angeles')
    
    Returns:
        list: Records with added 'utc_datetime' and 'local_date' fields
    
    Example:
        Input record:  {'timestamp': '2024-12-07T23:30:00', ...}
        With timezone: 'America/Los_Angeles'
        Output adds:   {'utc_datetime': <2024-12-08 07:30 UTC>,
                       'local_date': <2024-12-07>, ...}
    """
    # Get the timezone object for the source data
    # UTC is a special case - use the pytz.UTC constant
    if source_tz == 'UTC':
        tz = pytz.UTC
    else:
        # Convert IANA timezone string to pytz timezone object
        tz = pytz.timezone(source_tz)
    
    normalized = []
    
    # Process each health record
    for record in data:
        # Create a copy to avoid modifying the original data
        new_record = record.copy()
        
        # Extract timestamp field
        # Different data sources may use 'date' or 'timestamp' as the field name
        if 'date' in record:
            timestamp_str = record['date']
        else:
            timestamp_str = record['timestamp']
        
        # Parse the timestamp string into a datetime object
        # dateutil.parser can handle many date/time formats automatically
        dt = parser.parse(timestamp_str)
        
        # Make the datetime timezone-aware
        # Two cases to handle:
        
        # Case 1: Naive datetime (no timezone info)
        # Localize it to the source timezone
        if dt.tzinfo is None:
            dt_local = tz.localize(dt)
        
        # Case 2: Timezone-aware datetime
        # Convert it to the source timezone
        else:
            dt_local = dt.astimezone(tz)
        
        # Convert to UTC for standardized storage
        # All times stored in UTC for easy comparison across timezones
        dt_utc = dt_local.astimezone(pytz.UTC)
        
        # THE KEY PART: Store the LOCAL date
        # This ensures activities are counted on the correct calendar day
        # in the user's timezone, not in UTC
        # Example: 11 PM Dec 7 in LA = 7 AM Dec 8 UTC, but should count as Dec 7
        local_date = dt_local.date()
        
        # Add the normalized timestamp and local date to the record
        new_record['utc_datetime'] = dt_utc
        new_record['local_date'] = local_date
        
        normalized.append(new_record)
    
    return normalized