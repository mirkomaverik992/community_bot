# Community Bot

Community Bot è un bot Discord in Python pensato per rendere i server più attivi, con sistema XP & livelli, classifiche utenti e stanze vocali temporanee per il gaming.

## Funzioni principali

- XP e livelli per messaggi in chat.
- Comandi per profilo e classifica (`!level`, `!top`, `!profilo`).
- Creazione di stanze vocali temporanee con `!creastanza`.
- Chiusura rapida delle stanze con `!chiudistanza`.
- Comando `!comandi` per mostrare l’help in embed.

## Requisiti

- Python 3.10+  
- Libreria `discord.py` installata  
- Un bot creato su Discord Developer Portal con token valido

## Configurazione

1. Crea un bot su Discord Developer Portal e copia il token.  
2. Crea una categoria vocale nel tuo server (es. "STANZE TEMPORANEE") e copia l’ID.  
3. Nel file `main.py` imposta:
   - la variabile `ROOM_CATEGORY_ID` con l’ID della categoria
   - il token tramite variabile d’ambiente `DISCORD_BOT_TOKEN`.

Esempio su macOS/Linux:

