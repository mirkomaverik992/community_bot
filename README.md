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
export DISCORD_BOT_TOKEN="IL_TUO_TOKEN"
python main.py

Su Windows (PowerShell):
**## Comandi

- `!level` – mostra il tuo livello e gli XP.  
- `!top` – mostra la top 10 del server.  
- `!profilo @utente` – profilo di un utente.  
- `!creastanza <nome>` – crea una stanza vocale temporanea.  
- `!chiudistanza` – chiude la stanza vocale in cui sei.  
- `!comandi` – mostra la lista dei comandi.

## Hosting su Replit (consigliato)

- Importa il progetto su Replit e imposta `main.py` come entrypoint.  
- Metti il token in **Secrets** con chiave `DISCORD_BOT_TOKEN`.  
- Avvia il Repl e il bot andrà online nel tuo server.

## Link utili

- Pagina del bot su top.gg: *(aggiungi qui l’URL di top.gg quando è approvato)*  
- Documentazione Discord Developer Portal: https://discord.com/developers/docs/intro**
