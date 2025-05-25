# Realizzazione di un Web Server minimale in Python

## Obiettivo
Creare un semplice server HTTP locale capace di servire file statici HTML/CSS.

## Funzionalità principali
- Porta 8080 su localhost
- Gestione richieste GET
- Risposta 200 con contenuto file
- Risposta 404 per file mancanti
- Supporto MIME types (.html, .css, .jpg, ...)
- Logging console delle richieste

## Struttura progetto
- `server.py`: server HTTP minimale
- `www/`: directory con file HTML/CSS statici

## Uso
1. Esegui `python3 server.py`
2. Visita `http://localhost:8080` nel browser

## Estensioni opzionali implementate
✅ MIME Types  
✅ Logging richieste  
✅ Layout responsive base (con CSS)
