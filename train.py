from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
from datasets import Dataset
import torch
from peft import LoraConfig, get_peft_model
import json

# Carica il dataset formattato
with open("dataset.json") as f:
    conversations = json.load(f)

# Carica il tokenizer della formattazione
model_name = "unsloth/Llama-3.2-1B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Verifica e aggiungi il token di padding se necessario
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({"pad_token": "<pad>"})

system_prompt = """
Sei un assistente disponibile, rispettoso e onesto e un recommender di ricette esperto in salute e sostenibilità di nome ANITA 
(Advanced Natural-based interaction for the ITAlian language).
Rispondi nella lingua italiana in modo chiaro, semplice ed esaustivo.
Rispondi sempre nel modo più utile possibile, pur essendo sicuro. Lo stile delle tue risposte è persuasivo.
Nelle risposte elimina i suggerimenti di riposte che vorresti ottenere dall'utente.
Prediligi risposte di massimo 3-5 righi.
Se l'utente ti chiede chi sei, rispondi che sei un assistente virtuale che suggerisce ricette e dà consigli sulla salute e la sostenibilità.
Le risposte non devono includere contenuti dannosi, non etici, razzisti, sessisti, tossici, pericolosi o illegali.
Se non conosci la risposta a una domanda, non condividere informazioni false.
Fa all'utente domande sul suo nome, le sue allergie, le sue restrizioni alimentari e i suoi ingredienti preferiti per conoscerlo meglio.
"""

# Formatta i dati utilizzando il chat template del tokenizer
formatted_data = []
for conv in conversations:
    messages = [{"role": "system", "content": system_prompt}]
    for turn in conv:
        if "user" in turn:
            messages.append({"role": "user", "content": turn["user"]})
        elif "assistant" in turn:
            messages.append({"role": "assistant", "content": turn["assistant"]})
    
    # Applica il chat template integrato
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=False 
    )
    formatted_data.append({"text": text})

# Converti in un oggetto Dataset
dataset = Dataset.from_dict({"text": [d["text"] for d in formatted_data]})

# Dividi il dataset in training e test set
tokenized_dataset = dataset.train_test_split(test_size=0.1)

# Carica il modello con precisione mista e quantizzazione 4-bit
bnb_config = None
if torch.cuda.is_available():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
    quantization_config=bnb_config
)

# Ridimensiona gli embedding del modello se sono stati aggiunti nuovi token
model.resize_token_embeddings(len(tokenizer))

# Applica LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Tokenizzazione del dataset
def preprocess(example):
    tokenized = tokenizer(
        example["text"],
        truncation=True,
        max_length=512,
        padding="max_length"
    )
    tokenized["labels"] = tokenized["input_ids"].copy()
    return tokenized

tokenized_dataset = tokenized_dataset.map(preprocess, batched=True)

# Configurazione e training
training_args = TrainingArguments(
    output_dir="./llama-1b-finetuned",
    per_device_train_batch_size=2,       # Train Batch Size
    per_device_eval_batch_size=2,        # Eval Batch Size
    gradient_accumulation_steps=2,       # Gradient Accumulation
    num_train_epochs=10,                 # Numero Epoche
    learning_rate=2e-5,                  # Learning Rate basso per un fine-tuning stabile
    optim="adamw_torch",                 # Usa un ottimizzatore più efficiente
    weight_decay=0.01,                   # Contrasta l'overfitting
    eval_strategy="epoch",               # Valuta ogni N passi
    eval_steps=200,                      # Valutazione intermedia ogni 200 passi
    load_best_model_at_end=True,         # Carica automaticamente il modello migliore
    metric_for_best_model="eval_loss",   # Criterio per selezionare il modello migliore
    logging_dir="./logs",                # Directory di logging
    logging_steps=50,                    # Frequenza di logging
    save_strategy="epoch",               # Salva il modello alla fine di ogni epoca
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
)

trainer.train()
trainer.save_model("./llama-1b-finetuned")
tokenizer.save_pretrained("./llama-1b-finetuned")