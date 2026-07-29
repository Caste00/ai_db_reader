## PROSSIMI PASSI
1) fare la parte per estrarre le configurazioni dal documento 
2) database sqlite
3) database chormadb
4) funzioni cosine_similarity


## STRUTTURA DEL PROGETTO

```
src/
├── main.py
├── cli/
├── config/
├── database/
├── llm/
├── rag/
├── memory/
├── models/
├── utils/
├── scripts/
└── test/
```
-------------

## `main.py`
Entry point dell'applicazione. Inizializza configurazione, provider LLM,
vector store e avvia l'interfaccia (CLI per ora).

## `cli/`
Interfaccia a riga di comando per interagire col chatbot durante lo sviluppo.
- `terminal.py` — loop di input/output da terminale.

## `config/`
Configurazione statica dell'applicazione, non codice.
- `config.yaml` — provider LLM attivo (ollama/openai/claude), credenziali
  db, path del vector store, parametri di retrieval (es. top-k).
- `prompts.yaml` — template dei prompt (system prompt, prompt di
  generazione SQL, prompt di correzione errori).

## `database/`
Tutto ciò che riguarda la connessione e l'esecuzione sicura sul database
relazionale dell'utente (punti 3-4 del flusso: verifica ed esecuzione query).
- `connection.py` — apertura/gestione della connessione (es. SQLAlchemy).
- `query_validator.py` — validazione sintattica (`EXPLAIN`), whitelist dei
  comandi (solo `SELECT` in questa fase), blocco di DDL/DML non autorizzati.
- `query_executor.py` — esecuzione con utente a permessi limitati,
  `LIMIT` forzato, timeout, gestione errori da rimandare al LLM per
  autocorrezione.

## `llm/`
Astrazione sui provider LLM, in modo che il resto del codice non sappia se
sta parlando con Ollama, OpenAI o Claude.
- `base.py` — interfaccia comune (`generate`, `embed`, ecc.) che ogni
  provider implementa.
- `ollama_provider.py`, `openai_provider.py`, `claude_provider.py` —
  implementazioni specifiche.
- `chat.py` — orchestrazione della conversazione: riceve la domanda,
  chiama il retriever, costruisce il prompt, chiama il provider, gestisce
  il loop di autocorrezione della query.
- `prompts.py` — funzioni che assemblano i prompt a partire dai template
  in `config/prompts.yaml` e dal contesto recuperato.

## `rag/`
Tutto ciò che riguarda il recupero delle tabelle rilevanti (punto 1-2 del
flusso: indicizzazione offline e retrieval a runtime).
- `indexer.py` — genera il riassunto arricchito di ogni tabella (schema,
  FK, esempi di valori) e lo salva embeddato nel vector store. Eseguito
  offline/batch, non ad ogni messaggio.
- `vector_store.py` — wrapper attorno a ChromaDB (o pgvector in futuro):
  `add`, `query`, `delete`.
- `retriever.py` — data la domanda utente, calcola l'embedding e recupera
  le top-k tabelle più simili (cosine similarity).
- `context_builder.py` — assembla il contesto finale (riassunti delle
  tabelle selezionate) da passare al prompt di generazione SQL.

## `memory/`
Stato e storico della conversazione (contesto multi-turno, non RAG sul db).
- `conversation.py` — stato della sessione corrente (domande/risposte,
  tabelle già selezionate nei turni precedenti).
- `history.py` — persistenza dello storico su disco/db.
- `summarizer.py` — riassume conversazioni lunghe per non far esplodere
  il context window.

## `models/`
Strutture dati (dataclass/pydantic), nessuna logica di business.
- `table.py` — rappresentazione di una tabella del db e del suo riassunto.
- `message.py` — rappresentazione di un messaggio della chat.
- `document.py` — rappresentazione generica di un documento indicizzato
  nel vector store.

## `utils/`
Funzioni di supporto trasversali, senza logica di dominio.
- `config.py` — caricamento e validazione di `config.yaml`.
- `logger.py` — configurazione logging.
- `embedding.py` — chiamata di basso livello per generare un embedding
  (oggi via Ollama); usata sia da `rag/indexer.py` che da
  `rag/retriever.py`, così il modello di embedding è garantito identico
  in entrambe le fasi.

## `scripts/`
Script eseguibili una tantum, non importati dal resto del codice.
- `init_vector_db.py` — crea/inizializza la collection su ChromaDB.
- `import_schema.py` — estrae lo schema dal database e lancia
  `rag/indexer.py` per popolare il vector store.

## `test/`
Test automatici (unit test su validator, retriever, ecc.). Da popolare.

---

## Storico decisioni

- **`data/` rimossa**: conteneva `embeddings.py`, `conversations.py`,
  `schemas.py`, `cache.py` che duplicavano rispettivamente `rag/`,
  `memory/`, `models/` e (in parte) `utils/`. Mantenere un'unica cartella
  responsabile per ciascun concetto evita di doversi chiedere "dove sta
  il codice che gestisce X" tra due posti diversi.
- **`vector_store/` rimossa**: cartella vuota che duplicava concettualmente
  `rag/vector_store.py`.
