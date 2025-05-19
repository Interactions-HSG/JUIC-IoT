import json
from json_repair_helper import repair_and_parse_json

def measure_reliability(json_string):
    def check_json_validity(json_string):
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            return False

    # Check if the original JSON string is valid
    valid = check_json_validity(json_string)
    
    if valid:
        score = 1  # Full score if the JSON is valid
    else:
        # Handle cases where the repair function might return one or two values
        result = repair_and_parse_json(json_string)
        
        if isinstance(result, tuple) and len(result) == 2:
            repaired_json, _ = result  # Unpack the repaired JSON and any additional information
        else:
            repaired_json = result  # If only one value is returned

        # If the JSON was successfully repaired, give partial credit
        if repaired_json:
            score = 0.5
        else:
            score = 0  # No score if the JSON could not be repaired

    return score
