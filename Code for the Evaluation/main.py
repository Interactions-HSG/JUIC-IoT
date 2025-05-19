import json
import os
import time
from chat_interaction import ChatInteraction
from accuracy import measure_accuracy
from reliability import measure_reliability
from completeness import measure_completeness
from json_repair_helper import repair_and_parse_json

def main():
    print("Starting the script...")

    # Initialize ChatInteraction instance
    interaction = ChatInteraction()

    # Define folder paths
    prompts_folder = r"C:\Users\lucie\OneDrive\Desktop\Testing UI Selection\TXTFiles\Prompts"
    affordances_folder = r"C:\Users\lucie\OneDrive\Desktop\Testing UI Selection\TXTFiles\Affordances\Blinds\Affordances"
    references_folder = r"C:\Users\lucie\OneDrive\Desktop\Testing UI Selection\TXTFiles\Affordances\Blinds\HB"
    conversation_folder = r"C:\\Users\\lucie\\OneDrive\\Desktop\\Testing UI Selection\\TXTFiles\\Conversation"  # Add this path
    results_folder = r"C:\Users\lucie\OneDrive\Desktop\Testing UI Selection\Blinds\GPT 4"

    print("Defined folder paths.")

    # Ensure the results folder exists
    os.makedirs(results_folder, exist_ok=True)

    # Check file paths
    try:
        print("Checking prompt files...")
        prompt_files = [os.path.join(prompts_folder, f) for f in os.listdir(prompts_folder) if f.endswith('.txt')]
        print(f"Found prompt files: {prompt_files}")

        print("Checking affordance files...")
        affordance_files = [os.path.join(affordances_folder, f) for f in os.listdir(affordances_folder) if f.endswith('.txt')]
        print(f"Found affordance files: {affordance_files}")

        print("Checking reference files...")
        reference_files = {
            os.path.basename(f): os.path.join(references_folder, f)
            for f in os.listdir(references_folder) if f.endswith('.txt')
        }
        print(f"Found reference files: {reference_files}")
    except Exception as e:
        print(f"Error accessing files: {e}")
        return

    # Iterate over each prompt file
    for prompt_file in prompt_files:
        print(f"Processing prompt: {prompt_file}")

        prompt_name = os.path.splitext(os.path.basename(prompt_file))[0]
        result_file_path = os.path.join(results_folder, f"{prompt_name}_results.txt")
        print(f"Result file path: {result_file_path}")

        overall_accuracy = []
        overall_reliability = []
        overall_completeness = []
        overall_response_times = []

        # Load prompt content
        try:
            with open(prompt_file, 'r') as file:
                prompt_content = file.read().strip()
                print(f"Loaded prompt content: {prompt_content}")
        except Exception as e:
            print(f"Error reading prompt file {prompt_file}: {e}")
            continue

        # Process each affordance file for the current prompt
        for affordance_file in affordance_files:
            affordance_name = os.path.basename(affordance_file)
            reference_file_path = reference_files.get(affordance_name)

            if not reference_file_path or not os.path.exists(reference_file_path):
                print(f"Warning: No reference file found for {affordance_name}")
                continue

            # Load the reference content
            with open(reference_file_path, 'r') as ref_file:
                try:
                    reference_content = json.load(ref_file)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON from reference file {reference_file_path}: {e}")
                    continue

            # Perform 10 iterations for each affordance
            for i in range(10):
                with open(affordance_file, 'r') as aff_file:
                    user_message = aff_file.read().strip()

                # Run the interaction
                response_content, response_time = interaction.run_interaction(
                    user_message, prompt_path=prompt_file, conversation_folder=conversation_folder
                )

                # Handle response content
                if isinstance(response_content, str):
                    response_json = repair_and_parse_json(response_content)
                else:
                    print(f"Warning: Unexpected response type for {affordance_name}")
                    continue

                if response_json is None:
                    continue

                # Measure metrics
                accuracy = measure_accuracy(response_json, reference_content)
                reliability = measure_reliability(response_content)
                completeness = measure_completeness(response_json, reference_content)

                # Store metrics for final summary
                overall_accuracy.append(accuracy)
                overall_reliability.append(reliability)
                overall_completeness.append(completeness)
                overall_response_times.append(response_time)

                # Store iteration results
                iteration_result = {
                    "iteration": i + 1,
                    "response_time": response_time,
                    "accuracy": accuracy,
                    "reliability": reliability,
                    "completeness": completeness,
                    "response_content": response_json
                }

                # Write iteration results to the result file
                with open(result_file_path, 'a') as result_file:
                    result_file.write(f"[{affordance_name} - Iteration {iteration_result['iteration']}]\n")
                    result_file.write(f"Response Time: {iteration_result['response_time']:.2f} seconds\n")
                    result_file.write(f"Accuracy: {iteration_result['accuracy']:.2f}\n")
                    result_file.write(f"Reliability: {iteration_result['reliability']:.2f}\n")
                    result_file.write(f"Completeness: {iteration_result['completeness']:.2f}\n")
                    result_file.write("\n--- Response Content ---\n")
                    result_file.write(f"{json.dumps(iteration_result['response_content'], indent=2)}\n")
                    result_file.write("\n" + "=" * 50 + "\n\n")

        # Calculate final averages for the prompt
        if overall_accuracy:
            avg_accuracy = sum(overall_accuracy) / len(overall_accuracy)
            avg_reliability = sum(overall_reliability) / len(overall_reliability)
            avg_completeness = sum(overall_completeness) / len(overall_completeness)
            avg_response_time = sum(overall_response_times) / len(overall_response_times)

            # Write final results summary for this prompt
            with open(result_file_path, 'a') as result_file:
                result_file.write("Final Results Summary:\n")
                result_file.write(f"Average Accuracy: {avg_accuracy:.2f}\n")
                result_file.write(f"Average Reliability: {avg_reliability:.2f}\n")
                result_file.write(f"Average Completeness: {avg_completeness:.2f}\n")
                result_file.write(f"Average Response Time: {avg_response_time:.2f} seconds\n")
                result_file.write("\n" + "=" * 50 + "\n\n")

if __name__ == "__main__":
    main()