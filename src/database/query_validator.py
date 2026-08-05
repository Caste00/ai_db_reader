# whitelist select, blocco ddl/dml, explain prima di eseguire e sempre qui controllo se un utente ha il permesso di accedere a una certa area del db
"""
```json
{
  "queries": [
    "SELECT Name FROM Artist ORDER BY COUNT(TrackId) DESC LIMIT 1"
  ],
  "explanation": "Risultato: Il cantante più famoso è elenco di tutti gli artisti con il numero massimo di tracce associati, quindi il primo nome nell'elenco."
}
"""