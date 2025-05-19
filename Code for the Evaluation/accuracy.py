import json
from json_repair_helper import repair_and_parse_json

# Define a category for similar UI components
DISPLAY_COMPONENTS_CATEGORY = {"Text Display", "Value Horizontal Display", "Value Vertical Display"}
PARTIAL_MATCH_COMPONENTS = {"Input Form", "Slider"}  # Components that count as 0.5 match

def measure_accuracy(response_content, reference_content):
    """
    Measure accuracy by comparing the 'uiComponent' in both response and reference content.
    Includes partial credit (0.5) if the response is in the same category of display components
    or if the components are in the PARTIAL_MATCH_COMPONENTS category.
    """
    def compare_ui_component(response, reference):
        response_value = response.get('uiComponent', None)
        reference_value = reference.get('uiComponent', None)

        # Exact match
        if response_value == reference_value and response_value is not None:
            return 1.0

        # Partial match in the same category
        elif (
            response_value in DISPLAY_COMPONENTS_CATEGORY and reference_value in DISPLAY_COMPONENTS_CATEGORY
        ) or (
            response_value in PARTIAL_MATCH_COMPONENTS and reference_value in PARTIAL_MATCH_COMPONENTS
        ):
            return 0.5  # Partial match

        # No match or mismatch
        return 0.0

    try:
        if response_content is None or reference_content is None:
            print("Error: One of the input contents is None.")
            return 0.0

        response_json = repair_and_parse_json(response_content)
        reference_json = repair_and_parse_json(reference_content)

        if response_json is None or reference_json is None:
            print("Error: Failed to parse one of the JSON contents.")
            return 0.0

        # Extract lists of components from response and reference JSON
        response_list = list(response_json.values())[0] if len(response_json) > 0 else []
        reference_list = list(reference_json.values())[0] if len(reference_json) > 0 else []

        if not isinstance(response_list, list) or not isinstance(reference_list, list):
            print("Error: Expected lists in JSON structure.")
            return 0.0

        max_len = max(len(response_list), len(reference_list))
        total_accuracy = 0.0

        # Compare each item in response and reference lists
        for i in range(max_len):
            if i < len(response_list) and i < len(reference_list):
                item_accuracy = compare_ui_component(response_list[i], reference_list[i])
            else:
                item_accuracy = 0.0  # No component selected, accuracy is 0

            total_accuracy += item_accuracy

        # Return average accuracy
        return total_accuracy / max_len if max_len > 0 else 1.0

    except Exception as e:
        print(f"Error processing JSON: {e}")
        return 0.0