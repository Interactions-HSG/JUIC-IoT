from openai import OpenAI
import os
import time

class ChatInteraction:
    def __init__(self, model="g", temperature=0.2, api_key="", base_url=""):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.temperature = temperature

    def _load_messages(self, user_message, prompt_path, conversation_folder):
        """
        Load and construct a sequence of messages from the given prompt and conversation files.
        """
        def read_file(file_path, encoding='utf-8'):
            if not os.path.exists(file_path):
                print(f"Error: File not found - {file_path}")
                return None
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read().strip()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                return None

        # Load prompt
        prompt = read_file(prompt_path)
        if prompt is None:
            return None

        # Load all conversation messages
        conversation_files = [
            os.path.join(conversation_folder, f)
            for f in os.listdir(conversation_folder) if f.endswith('.txt')
        ]
        conversation_files.sort()  # Ensure messages are processed in order

        conversation_messages = []
        for i, file_path in enumerate(conversation_files):
            content = read_file(file_path)
            if content is None:
                print(f"Warning: Skipping unreadable file {file_path}")
                continue
            role = "user" if i % 2 == 0 else "assistant"
            conversation_messages.append({"role": role, "content": content})

        # Append the current user message
        conversation_messages.append({"role": "user", "content": user_message})

        # Add the system prompt at the beginning
        messages = [{"role": "system", "content": prompt}] + conversation_messages
        return messages

    def run_interaction(self, user_message, prompt_path, conversation_folder):
        """
        Run a chat interaction using the given user message, prompt, and conversation history.
        """
        # Load the message history
        messages = self._load_messages(user_message, prompt_path, conversation_folder)
        if messages is None:
            print("Error: Could not load messages.")
            return None, None

        # Make the request to the API
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )
            end_time = time.time()

            response_content = response.choices[0].message.content
            response_time = end_time - start_time
            return response_content, response_time

        except Exception as e:
            print(f"Error during interaction: {e}")
            return None, None
