# Versione Linux

In questa cartella trovi il programma sorgente in Python per l'ambiente Linux e tutti i file necessari per generare l'eseguibile (`.AppImage`).
A causa dei limiti di dimensione di GitHub, l'eseguibile `.AppImage` già compilato non è incluso direttamente in questa repository.

## 🚀 Esecuzione diretta su Linux

Puoi avviare il programma direttamente, utilizzando il suo launcher:

```bash
chmod +x run_AI-Desktop-Launcher.sh
./run_AI-Desktop-Launcher.sh
```

## 📦 Creazione dell'AppImage in locale

Se preferisci avere un unico file eseguibile (`.AppImage`), la cartella contiene anche lo script bash appropriato:

```bash
chmod +x crea_appimage_linux.sh
./crea_appimage_linux.sh
```

*Assicurati che `python3` e `wget` siano installati.*

---

### 🤖 Generazione Automatica tramite Intelligenza Artificiale

**Nota bene:** Se non vuoi compilare nulla manualmente, ti basta fornire i file presenti in questa cartella (il file `.py`, `.sh`, `.spec`, `.desktop` e `requirements.txt`) o il solo link a questa repository a un'Intelligenza Artificiale come **Claude** o **Antigravity**.

Chiedi loro: *"Generami un eseguibile AppImage a partire da questi file"*, e l'assistente si occuperà automaticamente della compilazione, fornendoti l'eseguibile finale già pronto per essere scaricato!
