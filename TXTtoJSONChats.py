import json
import os
import re

cartella_chats = "chats"
output_file = "datasetChats.json"

conversations = []

if not os.path.exists(cartella_chats):
    print(f"❌ Errore: La cartella '{cartella_chats}' non esiste.")
    exit()

for filename in os.listdir(cartella_chats):
    if filename.endswith(".txt"):
        filepath = os.path.join(cartella_chats, filename)
        print(f"📂 Elaborando file: {filename}")

        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        conversation = []
        current_speaker = None
        message_buffer = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] (\w+)", line)
            
            if match:
                if current_speaker and message_buffer:
                    full_message = " ".join(message_buffer).strip()
                    conversation.append({current_speaker: full_message})
                
                current_speaker = "user" if match.group(2) != "assistant" else "assistant"
                message_buffer = [line[len(match.group(0)):].strip()]
            else:
                message_buffer.append(line)

        if current_speaker and message_buffer:
            full_message = " ".join(message_buffer).strip()
            conversation.append({current_speaker: full_message})

        if conversation:
            conversations.append(conversation)

# Scrive il risultato in JSON come un unico array
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(conversations, f, ensure_ascii=False, indent=4)

print(f"✅ Conversione completata! {len(conversations)} conversazioni salvate in '{output_file}'.")