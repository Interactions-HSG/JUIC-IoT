import json
from json_repair_helper import repair_and_parse_json

def measure_completeness(response_content, reference_content):
    """
    Measure completeness by comparing the components (numeration, name, uiComponent, valueMAX, valueMIN)
    in both response and reference content. Completeness is calculated based on component weights within
    the nested objects, with a malus applied at the end if any items are missing in the response.
    """
    components_with_weights = {
        "numeration": 0.3,
        "name": 0.1,
        "uiComponent": 0.05,
        "valueMAX": 0.5,
        "valueMIN": 0.5
    }

    def compare_components(components, response, reference, level="root"):
        total_weight = 0.0
        matched_weight = 0.0
        component_mismatch = False  # Track if there's a significant mismatch

        for component, weight in components.items():
            response_value = response.get(component)
            reference_value = reference.get(component)
            total_weight += weight

            # Debugging logs
            print(f"Debug: Comparing '{component}' at level '{level}'")
            print(f"  Response value: {response_value}")
            print(f"  Reference value: {reference_value}")

            # Handle exact match, including when both are None
            if response_value == reference_value:
                matched_weight += weight
                print(f"  Debug: Exact match for '{component}' at level '{level}'")
            # Partial match (both values exist but are different)
            elif response_value is not None and reference_value is not None:
                matched_weight += weight * 0.5
                print(f"  Debug: Partial match for '{component}' at level '{level}'")
            else:
                # Component mismatch or missing value
                component_mismatch = True
                print(f"  Debug: Mismatch or missing component '{component}' at level '{level}'")

        return matched_weight / total_weight if total_weight > 0 else 0.0, component_mismatch

    try:
        response_json = repair_and_parse_json(response_content)
        reference_json = repair_and_parse_json(reference_content)

        if response_json is None or reference_json is None:
            print("Error: One of the JSON inputs is invalid.")
            return 0.0

        response_list = list(response_json.values())[0]
        reference_list = list(reference_json.values())[0]

        if not isinstance(response_list, list) or not isinstance(reference_list, list):
            print(f"Error: One of the lists (response or reference) is not a list.")
            return 0.0

        total_completeness = 0.0
        malus_applied = False

        for i in range(len(reference_list)):
            if i < len(response_list):
                item_completeness, component_mismatch = compare_components(components_with_weights, response_list[i], reference_list[i], f"root[{i}]")
                if component_mismatch:
                    malus_applied = True  # Apply malus for missing/mismatched components
            else:
                item_completeness = 0.0
                malus_applied = True
                print(f"Debug: Missing item in response at index {i}, setting completeness to 0.0")

            total_completeness += item_completeness

        average_completeness = total_completeness / len(reference_list) if len(reference_list) > 0 else 1.0

        # Apply malus only if significant components were mismatched or missing
        if malus_applied:
            average_completeness = max(average_completeness - 0.1, 0.0)

        print(f"Debug: Final completeness score after malus: {average_completeness}")
        return average_completeness

    except Exception as e:
        print(f"Error processing JSON: {e}")
        return 0.0
