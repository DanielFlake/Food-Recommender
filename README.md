# Agente conversazionale per la raccomandazione di ricette
Agente conversazionale per la raccomandazione di ricette in italiano ed utilizzo dei Large Language Models per la generazione del dialogo.Il large Language Model utilizzato è Llamantino3 un ottimizzzazione per la lingua italiana del modello LlaMa3 di MetaAi.
## Come configurare il progetto per eseguire il codice su una macchina Windows (se stai già utilizzando una macchina con Ubuntu-20.04, salta i passaggi seguenti)
* Assicurati che i driver NVIDIA e CUDA siano installati sulla macchina.(Se non li hai,https://developer.nvidia.com/cuda-12-3-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local e https://www.nvidia.com/download/index.aspx)
* Apri le Funzionalità di Windows
* Abilita l'opzione "Sottosistema Windows per Linux"
* Apri il prompt dei comandi come amministratore
* Esegui il seguente comando: "wsl --install -d Ubuntu-20.04"
* Apri Ubuntu-20.04
* Configura un nome utente e una password
## Per configurare Ubuntu 20.04 per i driver NVIDIA e CUDA
* Digita "sudo apt-key del 7fa2af80" per rimuovere la vecchia chiave GPG.
* Digita "wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin".
* Digita "sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600".
* Digita "wget https://developer.download.nvidia.com/compute/cuda/12.3.2/local_installers/cuda-repo-wsl-ubuntu-12-3-local_12.3.2-1_amd64.deb".
* Digita "sudo dpkg -i cuda-repo-wsl-ubuntu-12-3-local_12.3.2-1_amd64.deb".
* Digita "sudo cp /var/cuda-repo-wsl-ubuntu-12-3-local/cuda-*-keyring.gpg /usr/share/keyrings/".
* Digita "sudo apt-get update".
* Digita "sudo apt-get -y install cuda-toolkit-12-3".
## Come creare una nuova sessione con un ambiente Python 3.8
* Digita tmux new-session -t llamantino
* Digita sudo apt install python3.8-venv
* Digita python3 -m venv llamantinoENV (questo comando installerà probabilmente l'ambiente nel percorso "\home\tuo_nome_utente_linux")
* Digita source llamantinoENV/bin/activate
## Come installare le librerie
Installare tutte le librerie contenute nel file requirements.txt con le relative versioni.
## Come impostare il codice
* Copia la directory "food_chatbot"e "Italian_chatbot_log"  all'interno della directory "\home\tuo_nome_utente_linux".
## Come eseguire l'agente conversazionale
* Digita tmux attach-session -t llamantino se non sei già all'interno della sessione.
* Digita il comando python "/home/tuo_nome_utente_linux/food-chatbot/my_gradio_app_ita.py".
