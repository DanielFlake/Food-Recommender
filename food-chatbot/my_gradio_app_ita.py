import gradio as gr
from huggingface_hub import login
import torch
from torch.version import cuda
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from guidance import models, gen
import json
import re
from json import dumps
import emoji
import string
import random
import ast
import gradio as gr
import webbrowser
import csv

# Definizione di una variabile globale
model_name="swap-uniba/LLaMAntino-3-ANITA-8B-Inst-DPO-ITA"
inizio_sequenza = "<|begin_of_text|>"
fine_sequenza = "<|eot_id|>"
inizio_intestazione = "<|start_header_id|>"
fine_intestazione = "<|end_header_id|>"

def sostituisci_cibi_con_emoji(testo):
    # Dizionario di mapping tra cibi e emoji
    mappatura_emoji_cibi = {
        "pane": ":bread:", "formaggio": ":cheese:","pollo": ":poultry_leg:", "pesce": ":fish:",
        "trota": ":fish:", "hamburger": ":hamburger:","gelato": ":ice_cream:",
        "insalata": ":green_salad:", "roquette":":green_salad:","carota": ":carrot:", "pomodoro": ":tomato:",
        "patata": ":potato:", "zucca": ":jack_o_lantern:", "limone": ":lemon:", "latte": ":milk_glass:",
        "cipolla": ":onion:", "funghi": ":mushroom:", "carne": ":meat_on_bone:", "miele": ":honey_pot:",
        "uova": ":egg:", "mozzarella": ":cheese:", "aglio": ":garlic:", "panino": ":sandwich:",
        "rucola": ":leafy_green:", "spinaci": ":leafy_green:"
    }

    # Sostituzione delle parole chiave aggiungendo l'emoji alla fine
    for cibo, cod_emoji in mappatura_emoji_cibi.items():
        testo = testo.replace(cibo, f"{cibo}{emoji.emojize(cod_emoji)}")

    return testo

def pulizia_testo(testo):
    cleaned_text = re.sub(r'<.*?>', '', text)
    return cleaned_text


def cambia_schermata():
    return gr.update(visible=False), gr.update(visible=False),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True), gr.update(visible=True),gr.update(visible=True),gr.update(visible=True)

def aggiorna_id_utente(username):
    return username

def invia_questionario( q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24):
    # Raccogliere tutti i dati in un dizionario
    dati = {
        "ID Utente": q1,
        "Genere": q2,
        "Fascia di età": q3,
        "Livello di istruzione": q4,
        "Impiego attuale": q5,
        "Valutazione": q6,
        "Valutazione": q7,
        "Frequenza di utilizzo": q8,
        "Interesse per il cibo": q9,
        "Interesse per sostenibilità e salute": q10,
        "Facilità d'uso": q11,
        "Controllo": q12,
        "Adeguatezza dell'interazione": q13,
        "Precisione della raccomandazione": q14,
        "Trasparenza/Precisione della spiegazione": q15,
        "Precisione della risposta alle domande": q16,
        "Persuasione": q17,
        "Precisione del confronto delle ricette": q18,
        "Precisione delle ricette alternative": q19,
        "Adeguatezza dell'interazione": q20,
        "Affidabilità": q21,
        "Fiducia": q22,
        "Soddisfazione generale": q23,
        "Intenzioni d'uso": q24
    }
    dati1=[
      [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22,q23,q24]
    ]
    nome_file="./Test/"+ str(q1) + ".txt"
    with open(nome_file, 'a') as file:
        file.write("\nQuestionario di valutazione\n")
        json.dump(dati, file, indent=4)
    with open('Report_questionari.csv', mode='a', newline='') as file:
       writer = csv.writer(file)
       writer.writerows(dati1)
    return gr.update(visible=True), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

# Formatting function for the English message and chatbot history to construct a prompt to generate a response for the user
def format_message_ita(message: str, history: list, user_info, memory_limit: int = 1):
    """
    Formats the message and history to costruct a prompt to generate a response for the user.

    Parameters:
        message (str): The message to which the user is expecting a reply.
        history (list): Past conversation history between the user and the system.
        user_info (dictionary): The Json with the user’s information and preferences.
        memory_limit (int): Limit on how many past interactions between the chatbot and the user to consider.

    Returns:
        str: Formatted message string.
    """
    missing_info = []
    for key in user_info:
      if user_info[key] is None:
           missing_info.append(key)
    

    system_message = inizio_intestazione + "<<SYS>>\n" \
         "Sei un assistente disponibile, rispettoso e onesto e un recommender di ricette esperto in salute e sostenibilità di nome ANITA " \
         "(Advanced Natural-based interaction for the ITAlian language)." \
         "Rispondi nella lingua italiana in modo chiaro, semplice ed esaustivo." \
         "Rispondi sempre nel modo piu' utile possibile, pur essendo sicuro. Lo stile delle tue risposte è persuasivo. " \
         "Nelle risposte elimina i suggerimenti di riposte che vorresti ottenere dall'utente."\
         "Prediligi risposte di massimo 3-5 righi."\
         "Se l'utente ti chiede chi sei, rispondi che sei un assistente virtuale che suggerisce ricette e dà consigli sulla salute e la sostenibilità. " \
         "Le risposte non devono includere contenuti dannosi, non etici, razzisti, sessisti, tossici, pericolosi o illegali. " \
         "Se non conosci la risposta a una domanda, non condividere informazioni false.\n" \
         "Le informazioni attualmente note sull'utente sono le seguenti: "+dumps(user_info)+"Fa all'utente domande sul suo nome, le sue allergie, le sue restrizioni alimentari"\
         "e i suoi ingredienti preferiti per conoscerlo meglio."\
         "<</SYS>>\n\n" \

# always keep len(history) <= memory_limit
    if len(history) > memory_limit:
        history = history[-memory_limit:]

    if len(history) == 0:
        return system_message + f"{message} {fine_intestazione}"

    formatted_message = system_message + f"{history[0][0]} {fine_intestazione} {history[0][1]} {fine_sequenza}"
    # Handle conversation history
    for user_msg, model_answer in history[1:]:
        formatted_message += f"{inizio_sequenza} {inizio_intestazione} {user_msg} {fine_intestazione} {model_answer} {fine_sequenza}"
    # Handle the current message
    formatted_message += f"{inizio_sequenza} {inizio_intestazione}  {message} {fine_intestazione}"

    return formatted_message

# Formatting function for the Italian json query
def format_json_message_ita(message: str, history: list, user_info):
    """
    Formats the message and history to costruct a prompt to generate the user Json.

    Parameters:
        message (str): The latest message that was submitted by the user.
        history (list): Past conversation history between the user and the system.
        user_info (dictionary): The Json with the user’s information and preferences.
    Returns:
        str: Formatted message string.
    """

    model_previous_answer=""
    system_message=""
    if len(history) > 0:
        history = history[-1:]
        for user_msg, model_answer in history[0:]:
          model_previous_answer = emoji.replace_emoji(model_answer)

    system_message = """Di seguito sono riportate le informazioni conosciute sull'utente in formato json: """ + dumps(user_info)+""" Per memorizzare le informazioni personali dell
        'utente, modificare il json iniziale se sono state fornite nuove informazioni esclusivamente nel messaggio dell'utente. Solo i campi per i quali è disponibile una nuova
         informazione devono essere modificati, gli altri campi vengono copiati dal json iniziale. Se nel messaggio dell'utente non vengono fornite nuove informazioni personali, il json
         iniziale rimane invariato. Scrivere solo il nuovo json senza ulteriori altre frasi o istruzioni."""
    json_formatted_message = f"""\{system_message} L'ultima risposta del modello è la seguente: '{model_previous_answer}'. Utilizzala solo per capire il contesto, assieme al messaggio
      utente corrente, per estrarre meglio le informazioni sull'utente. Il messaggio dell'utente da cui estrarre le nuove informazioni è il seguente: '{message}'. Il seguente è il
      nuovo profilo utente in formato JSON.
    Il json ha i campi 'nome' (rappresenta il nome dell'utente), 'età'(può assumere un valore numerico in base a quanto dichiarato), 'sesso'(se l'utente è un uomo o una donna o altro)
    , 'allergie alimentari', 'ingredienti preferiti'(ingredienti preferiti dall'utente), 'ingredienti non graditi', 'obiettivo di peso' (null di default, può assumere valori tra null,
    guadagnare, mantenere o perdere), 'malattie' (può assumere valori uno o più tra null, malattie cardiache, obesità, diabete), 'restrizioni alimentari' (Il valore di default è null,
    può assumere valori uno o più tra null, vegano, vegetariano, celiaco, senza latticini). Per costruirlo estrai le informazioni riguardo l'utente solo ed esclusivamente dal
    messaggio dell'utente se presenti, altrimenti i valori dei campi considerati rimane invariato. Se per esempio l'utente dicesse 'il mio $campo_json è $valore_campo_json',              aggiornare il json con il valore specificato dall'utente. Se l'utente manda un messaggio tipo 'ciao' o qualsiasi altro messaggio che non contenga nuove informazioni, non              aggiornare il json con informazioni fasulle e inventate. Fa in modo di generare un json corretto. Il json aggiornato è il seguente: ```json"""
    return json_formatted_message


if __name__ == "__main__":
    print(torch.cuda.is_available())
    bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
    dictionary = {"nome": None, "età": None, "sesso": None, "allergie alimentari": None, "ingredienti preferiti": None, "ingredienti non graditi": None, "obiettivo di peso": None,        "malattie": None, "restrizioni alimentari": None}
    # Define the pipeline
    llama_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        temperature=0.7,
        top_p=0.95,
        repetition_penalty=1.15
    )
    # load a model (could be Transformers, LlamaCpp, VertexAI, OpenAI...)
    llama2 = models.Transformers(model, tokenizer, device_map='cuda')
    
    callback = gr.CSVLogger()
    with gr.Blocks() as FoodLLM:
      with gr.Row(visible=True) as principale1 :
          history = gr.Chatbot(scale=3,height=460)
          instructions = gr.Textbox(value="Comincia la conversazione con il chatbot salutandolo e presentandoti fornendogli qualche informazione personale su di te. Il chatbot può porre ulteriori domande riguardo il tuo stato di salute, le tue allergie e le tue preferenze alimentari. \nCosa si può fare: \n- fare domande al sistema su piatti e ingredienti \n- chiedere di suggerire ricette \n- chiedere di spiegare le ragioni dietro un certo consiglio \n- chiedere al sistema di convincervi a provare una certa ricetta \n- chiedere di confrontare ricette tra loro \n- chiedere di suggerire ricette alternative simili a un piatto specifico \nN.B.: \n- assicurati di fornire al sistema il maggior numero di informazioni possibili su di te \n- assicurati di arricchire i tuoi messaggi con il tuo feedback riguardo le risposte del sistema \n- il tempo di risposta del sistema può variare, si prega di portare pazienza",label="Istruzioni del chatbot",scale=1,interactive=False)
      
      with gr.Row(visible=True) as principale2 :
        message = gr.Textbox(label="Scrivi il tuo messaggio per il chatbot qui!",scale=3)
        username = gr.Textbox(label="ID Utente (fare in modo di annotarselo)",interactive=False,scale=0.5)
        quiz = gr.Button("Termina chat ed inizia il questionario")

      json_file = gr.JSON(value=dictionary,visible=False)
      latest_interaction = gr.Textbox(visible=False)
      callback.setup([latest_interaction, username], "Italian_chatbot_log")
    # Gruppo 1: Domanda 1
      with gr.Group(visible=False) as gruppo1:
        gr.Markdown("**1: Si prega di specificare il proprio ID utente**")
        q1 = gr.Textbox(label="ID Utente", value="")
      username.change(fn=aggiorna_id_utente, inputs=username, outputs=q1)
    
    # Gruppo 2: Domanda 2
      with gr.Group(visible=False) as gruppo2:
        gr.Markdown("**2: Si prega di scegliere il proprio genere**")
        q2 = gr.Radio(choices=["Maschio", "Femmina", "Altro"],label="Genere")
    
    # Gruppo 3: Domanda 3
      with gr.Group(visible=False) as gruppo3:
        gr.Markdown("**3: Si prega di selezionare la fascia di età**")
        q3 = gr.Radio(choices=["-20", "21-30", "31-40", "41-50", "51-60", "61+"], label="Fascia di età")
    
    # Gruppo 4: Domanda 4
      with gr.Group(visible=False) as gruppo4:
        gr.Markdown("**4: Si prega di scegliere il livello di istruzione**")
        q4 = gr.Radio(choices=["Scuola primaria", "Scuola media", "Università", "Scuola di specializzazione", "Dottorato di ricerca"],label="Livello di istruzione")
    
    # Gruppo 5: Domanda 5
      with gr.Group(visible=False) as gruppo5:
        gr.Markdown("**5: Si prega di indicare il proprio impiego attuale**")
        q5 = gr.Radio(choices=["Studente", "Dipendente pubblico", "Dipendente di azienda privata", "Lavoratore autonomo", "Disoccupato"],label="Impiego attuale")
    
    # Gruppo 6: Domanda 6
      with gr.Group(visible=False) as gruppo6:
        gr.Markdown("**6: Come si valuterebbe come utente di computer?**")
        q6 = gr.Radio(choices=["Nessuna esperienza", "Principiante", "Medio", "Avanzato"],label="Valutazione")
    
    # Gruppo 7: Domanda 7
      with gr.Group(visible=False) as gruppo7:
        gr.Markdown("**7: Ha mai usato un chatbot prima d'ora?**")
        q7 = gr.Radio(choices=["Sì", "No", "Forse/Non so"], label="Uso pregresso")
    
    # Gruppo 8: Domanda 8
      with gr.Group(visible=False) as gruppo8:
        gr.Markdown("**8: Con quale frequenza ha utilizzato chatbot e assistenti digitali?**")
        q8 = gr.Radio(choices=["Mai", "Molto raramente (pochi casi complessivi)", "Raramente (pochi casi al mese)", "Moderatamente (1-3 volte a settimana)", "Regolarmente (giornalmente)"], label="Frequenza di utilizzo")
    
    # Gruppo 9: Domanda 9
      with gr.Group(visible=False) as gruppo9:
        gr.Markdown("**9: Quanto è interessato al cibo?**")
        q9 = gr.Radio(choices=["Basso", "Medio", "Alto"], label="Interesse per il cibo")
    
    # Gruppo 10: Domanda 10
      with gr.Group(visible=False) as gruppo10:
        gr.Markdown("**10: Quanto è interessato alla sostenibilità e alla salute?**")
        q10 = gr.Radio(choices=["Basso", "Medio", "Alto"], label="Interesse per sostenibilità e salute")
    
    # Gruppo 11: Domanda 11
      with gr.Group(visible=False) as gruppo11:
        gr.Markdown("**11: È stato facile per me capire come funzionava il chatbot**")
        q11 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Facilità d'uso")
    
    # Gruppo 12: Domanda 12
      with gr.Group(visible=False) as gruppo12:
        gr.Markdown("**12: Mi sento in grado di esprimere le mie preferenze reali**")
        q12 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Controllo")
    
    # Gruppo 13: Domanda 13
      with gr.Group(visible=False) as gruppo13:
        gr.Markdown("**13: Ho trovato facile comunicare al sistema**")
        q13 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Adeguatezza dell'interazione")

    # Gruppo 14: Domanda 14
      with gr.Group(visible=False) as gruppo14:
        gr.Markdown("**14: Le ricette raccomandate corrispondono ai miei gusti e bisogni**")
        q14 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Precisione della raccomandazione")

    # Gruppo 15: Domanda 15
      with gr.Group(visible=False) as gruppo15:
        gr.Markdown("**15: Ho capito perché le ricette mi sono state raccomandate**")
        q15 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Trasparenza/Precisione della spiegazione")
    
    # Gruppo 16: Domanda 16
      with gr.Group(visible=False) as gruppo16:
        gr.Markdown("**16: Il chatbot ha risposto in modo soddisfacente alle mie domande**")
        q16 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Precisione della risposta alle domande")
    
    # Gruppo 17: Domanda 17
      with gr.Group(visible=False) as gruppo17:
        gr.Markdown("**17: Il chatbot mi ha convinto a provare nuove ricette** ")
        q17 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Persuasione")
    
    # Gruppo 18: Domanda 18
      with gr.Group(visible=False) as gruppo18:
        gr.Markdown("**18: Sono soddisfatto della funzione di confronto delle ricette del chatbot** ")
        q18 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Precisione del confronto delle ricette")

    # Gruppo 19: Domanda 19
      with gr.Group(visible=False) as gruppo19:
        gr.Markdown("**19: Sono soddisfatto delle ricette alternative proposte dal chatbot**")
        q19 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Precisione delle ricette alternative")
    
    # Gruppo 20: Domanda 20
      with gr.Group(visible=False) as gruppo20:
        gr.Markdown("**20: Il chatbot comprende facilmente le richieste**")
        q20 =gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Adeguatezza dell'interazione 2")
    
    # Gruppo 21: Domanda 21
      with gr.Group(visible=False) as gruppo21:
        gr.Markdown("**21: Il chatbot è affidabile**")
        q21 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Affidabilità")
    
    # Gruppo 22: Domanda 22
      with gr.Group(visible=False) as gruppo22:
        gr.Markdown("**22: Il chatbot è degno di fiducia**")
        q22 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Fiducia")
    
    # Gruppo 23: Domanda 23
      with gr.Group(visible=False) as gruppo23:
        gr.Markdown("**23: Sono soddisfatto della mia esperienza complessiva con il chatbot**")
        q23 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Soddisfazione generale")
    
    # Gruppo 24: Domanda 24
      with gr.Group(visible=False) as gruppo24:
        gr.Markdown("**24: Userei di nuovo il chatbot** (Intenzioni d'uso)")
        q24 = gr.Radio(choices=["Fortemente in disaccordo", "In disaccordo", "Non so", "D'accordo", "Fortemente d'accordo"], label="Intenzioni d'uso")

      with gr.Group(visible=False) as gruppo25:
            invia_btn = gr.Button("Conferma Questionario")

      with gr.Group(visible=False) as pop_up:
            gr.Markdown("***Grazie per aver completato il questionario.***")

      quiz.click(cambia_schermata,[],[principale1,principale2,gruppo1,gruppo2,gruppo3,gruppo4,gruppo5,gruppo6,gruppo7,gruppo8,gruppo9,gruppo10,gruppo11,gruppo12,gruppo13,gruppo14,gruppo15,gruppo16,gruppo17,gruppo18,gruppo19,gruppo20,gruppo21,gruppo22,gruppo23,gruppo24, gruppo25])
      invia_btn.click(invia_questionario,[ q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24],[pop_up,gruppo1,gruppo2,gruppo3,gruppo4,gruppo5,gruppo6,gruppo7,gruppo8,gruppo9,gruppo10,gruppo11,gruppo12,gruppo13,gruppo14,gruppo15,gruppo16,gruppo17,gruppo18,gruppo19,gruppo20,gruppo21,gruppo22,gruppo23,gruppo24, gruppo25])

      def get_llamantino_response(message: str, history: list,json_file,username,latest_interaction):
        """
        Generates a conversational response from the Llamantino model and updates
        the JSON with the user's personal information.
  
        Parameters:
            message (str): User's input message.
            history (list): Past conversation history.
  
        Returns:
            str: Generated response from the Llamantino model.
        """
        if(username==""):
          username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        query = format_message_ita(message, history, json_file)
        json_query = format_json_message_ita(message, history, json_file)
        response = ""
  
        sequences = llama_pipeline(
            query,
            eos_token_id =tokenizer.eos_token_id,
            max_new_tokens=512,
        )
        torch.cuda.empty_cache()
        generated_text = sequences[0]['generated_text']
        response = generated_text[len(query):]  # Remove the prompt from the output

        lm = llama2 + json_query + gen(name="json", temperature=0.01, max_tokens=128, stop='```')
        try:
            json_file = json.loads(re.search('({.+})', lm['json']).group(0).replace("'", '"'))
        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare il Json:{e}")
        except AttributeError as e:
            print(f"Errore nel decodificare il Json:{e}")
        print(json_file)
        torch.cuda.empty_cache()
        testo = pulizia_testo(response.strip())
        testo_con_emoji=sostituisci_cibi_con_emoji(testo)
        history.append(("Utente: "+message, "Chatbot: "+testo_con_emoji))
        nome_file ="./Test/"+ str(username) + ".txt"
        with open(nome_file, 'a', encoding='utf-8') as file:
            file.write("\n\nUtente: "+message +"\n")
            file.write("Chatbot: "+testo +"\n")
        latest_interaction = "Utente: "+message+" Chatbot: "+response.strip()
        return "", history, json_file,username,latest_interaction
  
      message.submit(get_llamantino_response, [message, history, json_file,username,latest_interaction], [message, history, json_file,username,latest_interaction])
      history.change(lambda *args: callback.flag(args), [latest_interaction,username], None, preprocess=False)
    FoodLLM.launch(share=True)