#!/usr/bin/env python3
import os
import re
from datetime import datetime
from llama_cpp import Llama


def get_next_file_number(archive_dir):
    """
    Check the archive folder for files that match the pattern and return
    the next three-digit file number as a string (e.g., '001', '002', etc.).
    """
    files = os.listdir(archive_dir)
    max_num = 0
    for f in files:
        match = re.match(r"(\d{3})_.*\.txt", f)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    return f"{max_num + 1:03d}"


def generate_title(conversation):
    """
    Generate a title for the conversation based on the first user prompt.
    Uses the first five words (after 'User:') and replaces spaces with underscores.
    """
    lines = conversation.splitlines()
    for line in lines:
        if line.startswith("User:"):
            words = line.split()[1:]  # remove the "User:" tag
            title = " ".join(words[:5])
            return title.replace(" ", "_")
    return "Conversation"


def archive_conversation(conversation, archive_dir="archive"):
    """
    Save the conversation to a text file in the archive folder. The file is named
    based on the next available sequential number, a title from the conversation,
    and a timestamp.
    """
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
    file_number = get_next_file_number(archive_dir)
    title = generate_title(conversation)
    # Timestamp for additional uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{file_number}_{title}_{timestamp}.txt"
    file_path = os.path.join(archive_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(conversation)
    print(f"Conversation archived as {file_path}")


def main():
    # Update this path to the location of your DeepSeek GGUF model file.
    model_path = "models/deepseek-llm-7b-chat.Q8_0.gguf"  # change as needed

    # Initialize the model.
    # You can adjust n_ctx (context size) and n_threads (number of CPU threads) as needed.
    llm = Llama(model_path=model_path, n_ctx=512, n_threads=4)

    conversation_context = ""
    print("DeepSeek Chat Session - Type 'exit' to quit.\n")
    try:
        while True:
            user_input = input("User: ")
            if user_input.strip().lower() == "exit":
                break
            conversation_context += f"User: {user_input}\n"

            # Build a prompt including conversation history, expecting the assistant's answer next.
            prompt = conversation_context + "Assistant: "

            # Generate a response with the model.
            # Adjust max_tokens, temperature, and stop tokens as needed.
            response = llm(
                prompt=prompt, max_tokens=256, temperature=0.7, stop=["User:"]
            )

            # Extract and print the assistant's answer.
            assistant_response = response["choices"][0]["text"].strip()
            print("Assistant:", assistant_response)
            conversation_context += f"Assistant: {assistant_response}\n"
    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
    finally:
        print("Exiting. Archiving conversation...")
        archive_conversation(conversation_context)


if __name__ == "__main__":
    main()
