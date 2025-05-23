# JUIC-Iot
This repository contains resources and tools for evaluating responses from LLMs to evaluate JUIC-IoT interface. It includes example Thing Descriptions (TDs) in both JSON-LD and Turtle formats, prompt templates, evaluation scripts nad evaluation data.

## 📁 Repository Structure

- [**Code for the Evaluation**](./Code%20for%20the%20Evaluation/)<br>
  Contains Python scripts used to evaluate responses based on *Accuracy*, *Completeness*, *Reliability* and *Response Time*.

- [**TD_Blinds.jsonld**](./TD_Blinds.jsonld)<br>
TD for an automated blinds device (JSON-LD).

- [**TD_Lights.jsonld**](./TD_Lights.jsonld)<br>
TD for a smart lighting device (JSON-LD).

- [**TD_Tractorbot.jsonld**](./TD_Tractorbot.jsonld)<br>
TD for the Tractorbot robot (JSON-LD).

- [**TD_Cherrybot.ttl**](./TD_Cherrybot.ttl)<br>
TD for the Cherrybot (Turtle/TTL format).

  ---

### Inside [`Code for the Evaluation`](./Code%20for%20the%20Evaluation/)<br>

- [**Blinds/**](./Code%20for%20the%20Evaluation/Blinds/)<br>
Contains evaluation results and LLM responses for the Blinds device.

- [**Lights/**](./Code%20for%20the%20Evaluation/Lights/)<br>
Contains evaluation results and LLM responses for the Lights device.

- [**Tractorbot/**](./Code%20for%20the%20Evaluation/Tractorbot/)<br>
Contains evaluation results and LLM responses for the Tractorbot device.

- [**Roboticarm/**](./Code%20for%20the%20Evaluation/Roboticarm/)<br>
Contains evaluation results and LLM responses for the Roboticarm.

- [**TXTFiles/**](./Code%20for%20the%20Evaluation/TXTFiles/)<br>
Contains supporting files for evaluation:
  - Background messages (brief interaction histories) to provide context for the LLM.
  - Human benchmark responses used as ground truth for comparison.
  - TDs split by affordance for each device (Blinds, Lights, Robotic Arm, and Tractorbot).

- [**accuracy.py**](./Code%20for%20the%20Evaluation/accuracy.py)<br>
Computes the accuracy of LLM Responses.

- [**completeness.py**](./Code%20for%20the%20Evaluation/completeness.py)<br>
Computes the completeness of LLM responses.

- [**reliability.py**](./Code%20for%20the%20Evaluation/reliability.py)<br>
Computes the reliability of LLM responses.

- [**chat_interaction.py**](./Code%20for%20the%20Evaluation/chat_interaction.py)<br>
Handles communication with the LLM, including sending prompts and receiving responses.

- [**json_repair_helper.py**](./Code%20for%20the%20Evaluation/json_repair_helper.py)<br>
Utility for validating and repairing JSON outputs generated by the LLM.

- [**main.py**](./Code%20for%20the%20Evaluation/main.py)<br>
Entry point script for executing the full evaluation pipeline.
