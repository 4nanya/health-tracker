import json
import sys


def load_json_data(filepath):
    """
    Load JSON data from a file with error handling.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Parsed JSON data (list or dict)
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file {filepath}")
        raise

