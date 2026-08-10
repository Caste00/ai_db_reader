## PROSSIMI PASSI
1.1) Controllo della description quando non viene generata
1.2) Tarare distance_threshold
1.3) llm/providers/chat.py -> tutto il modello che risponde a una domanda
1.4) Mettere i prompt nel file prompts.yaml per poterli modificare velocemente senza accedere al codice
2) Uso di un interfaccia comune per poter usare più providers come llm
3) Controllo correttezza query effettuato usando una libreria 
4) Salvataggio di conversazioni e chat 
5) Uso di permessi per decidere a quali dati ogni utente ha accesso
6) Frontend usando React e FastAPI
7) Deployment su docker


## STRUTTURA DEL PROGETTO

```
project/
├── backend/
│   └── src/
│       ├── main.py                        [MODIFICATO]
│       ├── api/                           [NUOVO]
│       │   ├── app.py                     crea FastAPI app, CORS, include router
│       │   ├── deps.py                    dependency injection (utente corrente, sessione)
│       │   ├── schemas/                   pydantic request/response
│       │   │   ├── chat.py
│       │   │   ├── auth.py
│       │   │   └── admin.py
│       │   └── routes/
│       │       ├── chat.py                POST /chat, /chat/stream (SSE)
│       │       ├── chats.py               CRUD cronologia (wrappa memory/crud.py)
│       │       ├── auth.py                login, JWT
│       │       ├── admin.py               gestione permessi ruolo↔tabella
│       │       └── index.py               trigger indicizzazione (background task)
│       ├── auth/                          [NUOVO]
│       │   ├── security.py                hashing password, creazione/verifica JWT
│       │   └── permissions.py             check permessi ruolo/tabella
│       ├── cli/
│       │   └── terminal.py                [INVARIATO — non più avviato da main.py]
│       ├── config/
│       │   ├── config.yaml                [MODIFICATO]
│       │   └── prompts.yaml               [INVARIATO]
│       ├── database/
│       │   ├── connection.py              [MODIFICATO]
│       │   ├── sqlalchemy_connector.py    [NUOVO — sostituisce sqlite_connector.py]
│       │   ├── database_connector_abc.py  [INVARIATO o leggermente MODIFICATO]
│       │   ├── query_executor.py          [MODIFICATO — poco]
│       │   ├── query_validator.py         [MODIFICATO — va scritto sul serio]
│       │   └── query_result.py            [INVARIATO]
│       ├── database/sqlite_connector.py   [RIMOSSO]
│       ├── llm/
│       │   ├── base.py                    [NUOVO] interfaccia comune (generate/embed)
│       │   ├── providers/
│       │   │   ├── ollama_provider.py     [SPOSTATO da llm/ollama.py]
│       │   │   ├── openai_provider.py     [NUOVO, opzionale]
│       │   │   └── claude_provider.py     [NUOVO, opzionale]
│       │   └── chat.py                    [MODIFICATO — ask() streaming]
│       ├── llm/ollama.py                  [RIMOSSO come file, contenuto spostato]
│       ├── memory/                        [INVARIATI, tranne conversation.py/summarizer.py da implementare]
│       ├── models/                        [INVARIATI, vedi nota sotto]
│       ├── rag/                           [INVARIATO]
│       ├── utils/                         [INVARIATO]
│       └── scripts/
│           ├── init_db.py                 [INVARIATO]
│           └── init_vector_db.py          [MODIFICATO — ha 2 bug: `chormadb`, `PersistenClient`]
│   ├── requirements.txt / pyproject.toml  [MODIFICATO]
│   └── Dockerfile                         [NUOVO]
├── frontend/                              [NUOVO — Next.js]
│   ├── app/
│   ├── components/
│   ├── lib/                               client API, gestione token
│   └── Dockerfile
└── docker-compose.yaml                    [NUOVO/MODIFICATO]
```

## TODO
* Creare una tabella e il sistema per estrarre i dati con i permessi degli utenti rispetto alle tabelle del database
* Durante la query_validation controllare se l'utente ha il permesso di vedere i dati di una certa tabella
* Cambiare la parte llm/ollama -> generate, invece che importarlo da li devo fare come ho fatto per i database in modo da poter usare altre fonti senza modificare il codice, implementare un' interfaccia comune 
* Interfaccia grafica online (il server che ospita ollama mette in rete anche un'interfaccia web per interagire con l'ia)
* In build_schema_context posso usare la distanza per scartare le tabelle pescate non pertinenti, sotto una certa soglia le scarto automaticamente



## LIMITI DA RISOLVERE
In rag/retriever se la ricerca di una query trova una colonna rilevante ma la tabella a cui appartiene non è tra quelle più simili, la tabella viene esclusa nonostante il campo all'interno sarebbe stato simili alla domanda utente. Il motivo è che il ciclo finale itera solo su table_meta. Quello che devo fare è promuovere le tabelle che sono trovato solo via colonna
