import json
from json_repair import repair_json

def repair_and_parse_json(json_str):
    """
    Repair and parse malformed JSON using the json_repair package or basic fixes.
    
    Args:
        json_str (str or dict): The JSON string to be repaired and parsed. If a dict is passed, return it as is.

    Returns:
        dict or None: The repaired and parsed JSON as a dictionary, or None if parsing fails.
    """
    # If the input is already a dictionary, return it
    if isinstance(json_str, dict):
        return json_str

    # Ensure we're working with a string
    if not isinstance(json_str, str):
        print(f"Invalid input type: expected string, got {type(json_str)}")
        return None

    try:
        # Step 1: Replace problematic sequences globally (for all occurrences in the JSON string)
        # Be cautious to not overwrite valid "null" with actual "null" for empty fields.
        json_str = json_str.replace('valueMAX": ,', 'valueMAX": null,')
        json_str = json_str.replace('valueMIN": ,', 'valueMIN": null,')
        json_str = json_str.replace(',}', '}')
        json_str = json_str.replace(',]', ']')
        
        # Step 2: Handle trailing commas
        json_str = json_str.replace(",\n", "\n").replace(", }", " }").replace(", ]", " ]")

        # Step 3: Attempt to repair the JSON string using json_repair to catch remaining issues
        repaired_json_str = repair_json(json_str, return_objects=False)

        # Step 4: Parse the repaired JSON string into a dictionary
        repaired_json = json.loads(repaired_json_str)
        
        return repaired_json
    
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error decoding repaired JSON: {e}")
        return None
