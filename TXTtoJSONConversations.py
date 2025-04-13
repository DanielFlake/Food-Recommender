import json
import os

directory_root = "conversations"
output_file = "datasetConversation.json"

conversations = []

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_conversation = []
    current_speaker = None
    message_buffer = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("User:"):
            if current_speaker == "assistant" and message_buffer:
                current_conversation.append({"assistant": " ".join(message_buffer).strip()})
                message_buffer = []
            current_speaker = "user"
            message_buffer.append(line[len("User:"):].strip())
        elif line.startswith("Assistant:"):
            if current_speaker == "user" and message_buffer:
                current_conversation.append({"user": " ".join(message_buffer).strip()})
                message_buffer = []
            current_speaker = "assistant"
            message_buffer.append(line[len("Assistant:"):].strip())
        else:
            message_buffer.append(line)

    if current_speaker and message_buffer:
        current_conversation.append({current_speaker: " ".join(message_buffer).strip()})

    if current_conversation:
        conversations.append(current_conversation)

def process_folder(folder):
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isdir(filepath):
            process_folder(filepath)
        elif filename.endswith("conversation.txt"):
            print(f"📂 Elaborando file: {filepath}")
            process_file(filepath)

if os.path.exists(directory_root):
    process_folder(directory_root)
else:
    print(f"❌ Errore: La cartella '{directory_root}' non esiste.")
    exit()

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(conversations, f, ensure_ascii=False, indent=4)

print(f"✅ Conversione completata! {len(conversations)} conversazioni salvate in '{output_file}'.")